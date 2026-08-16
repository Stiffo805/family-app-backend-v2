from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from util.settings import settings_object
from fastapi.middleware.cors import CORSMiddleware

from endpoints.shopping_list import router as shopping_list_router
from endpoints.shopping_list_entry import router as shopping_list_entry_router
from endpoints.product import router as product_router
from endpoints.changelog import router as changelog_router
from endpoints.unit import router as unit_router
from endpoints.auth import router as auth_router

from util.settings import settings_object

from sqlalchemy.exc import IntegrityError

app = FastAPI()

origins = [settings_object.FRONTEND_URL]

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

api_key_scheme = APIKeyHeader(name="Authorization", scheme_name="FamilyPassword")

def verify_password(auth_header: str = Depends(api_key_scheme)):
    if auth_header and auth_header.startswith("FamilyPassword: "):
        password = auth_header.removeprefix("FamilyPassword: ").strip()
        
        if password == settings_object.PASSWORD: 
            return True
            
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized: Incorrect or missing password"
    )

@app.exception_handler(IntegrityError)
async def sqlalchemy_integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Data conflict. The record already exists or violates database constraints."}
    )

@app.get("/health")
def health():
    return {"Healthy": True}

api_router = APIRouter(dependencies=[Depends(verify_password)])

api_router.include_router(shopping_list_router, prefix="/shopping-lists")
api_router.include_router(shopping_list_entry_router, prefix="/shopping-list-entries")
api_router.include_router(product_router, prefix="/products")
api_router.include_router(changelog_router, prefix="/changelog")
api_router.include_router(unit_router, prefix="/units")
api_router.include_router(auth_router, prefix="/auth")

app.include_router(api_router)