import json

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from dao.changelog_dao import ChangelogDao
from dao.shopping_list_dao import ShoppingListDao
from database.db import get_db
from database.models.changelog import ChangelogModel
from database.models.shopping_list import ShoppingListModel
from util.types import CreateShoppingListRequest, EditShoppingListRequest, ShoppingListResponse

from datetime import datetime

router = APIRouter(tags=["Shopping lists"])

@router.get("/")
def get_all_shopping_lists():
    with get_db() as db_session:
        shopping_list_dao = ShoppingListDao(db_session)

        items = [ShoppingListResponse.model_validate(item) for item in shopping_list_dao.get_all()]

        return JSONResponse(content=jsonable_encoder({"items": items}))

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_shopping_list(request: CreateShoppingListRequest):
    with get_db() as db_session:
        shopping_list_dao = ShoppingListDao(db_session) 
        changelog_dao = ChangelogDao(db_session)

        new_shopping_list = ShoppingListModel(
            title=request.title,
            last_updated_at=datetime.now()
        )

        shopping_list_dao.save(new_shopping_list)

        changelog_entry = ChangelogModel(
            author=request.username,
            change_title='Utworzono listę zakupów',
            shopping_list_id=new_shopping_list.id,
            created_at=datetime.now(),
            product_id=None
        )

        changelog_dao.save(changelog_entry)

@router.put("/{shopping_list_id}", status_code=status.HTTP_200_OK)
def edit_shopping_list(shopping_list_id: str, request: EditShoppingListRequest):
    with get_db() as db_session:
        shopping_list_dao = ShoppingListDao(db_session) 
        changelog_dao = ChangelogDao(db_session)

        shopping_list = shopping_list_dao.get_by_id(shopping_list_id)

        if shopping_list is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        shopping_list.title = request.title

        shopping_list_dao.save(shopping_list)

        changelog_entry = ChangelogModel(
            author=request.username,
            change_title='Zmieniono nazwę listy zakupów',
            shopping_list_id=shopping_list.id,
            created_at=datetime.now(),
            product_id=None
        )

        changelog_dao.save(changelog_entry)

@router.get("/{shopping_list_id}")
def get_shopping_list_by_id(shopping_list_id: str):
    with get_db() as db_session:
        shopping_list_dao = ShoppingListDao(db_session)

        shopping_list = shopping_list_dao.get_by_id(shopping_list_id) 

        if shopping_list is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        item = ShoppingListResponse.model_validate(shopping_list)

        return JSONResponse(content=jsonable_encoder(item))