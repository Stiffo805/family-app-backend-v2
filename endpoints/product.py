from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from dao.product_dao import ProductDao
from database.db import get_db
from database.models.product import ProductModel
from util.types import CreateProductRequest, ProductResponse

router = APIRouter(tags=["Products"])

@router.get("/search")
def search_products(search_query: str = Query("", alias="searchQuery")):
    with get_db() as db_session:
        product_dao = ProductDao(db_session)

        items = [ProductResponse.model_validate(item) for item in product_dao.search(search_query)]

        return JSONResponse(content=jsonable_encoder({"items": items})) 

@router.post("/")
def create_new_product(request: CreateProductRequest):
    with get_db() as db_session:
        product_dao = ProductDao(db_session)

        new_product = ProductModel(name=request.name)

        created_product = ProductResponse.model_validate(product_dao.save(new_product))

        return JSONResponse(content=jsonable_encoder({"item": created_product})) 

@router.get("/{product_id}")
def get_product_by_id(product_id: str):
    with get_db() as db_session:
        product_dao = ProductDao(db_session)

        product = product_dao.get_by_id(product_id)

        item = ProductResponse.model_validate(product)

        return JSONResponse(content=jsonable_encoder({"item": item})) 