from fastapi import APIRouter


router = APIRouter(tags=["Auth"])

@router.post("/check-pass")
def check_if_auth_middleware_passed():
    return {"auth": True}