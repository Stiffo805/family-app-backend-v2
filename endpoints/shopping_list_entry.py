from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from dao.changelog_dao import ChangelogDao
from dao.shopping_list_entry_dao import ShoppingListEntryDao
from database.db import get_db
from database.models.changelog import ChangelogModel
from database.models.shopping_list_entry import ShoppingListEntryModel
from util.types import CheckShoppingListEntryRequest, CreateShoppingListEntryRequest, EditShoppingListEntryRequest

router = APIRouter(tags=["Shopping lists entries"])

@router.post("/")
def create_new_shopping_list_entry(request: CreateShoppingListEntryRequest):
    with get_db() as db_session:
        shopping_list_entry_dao = ShoppingListEntryDao(db_session)
        changelog_dao = ChangelogDao(db_session)

        new_shopping_list_entry = ShoppingListEntryModel(
            shopping_list_id=request.shopping_list_id,
            product_id=request.product_id,
            quantity=request.quantity,
            unit=request.unit,
            extra_notes=request.extra_notes,
            last_updated_at=datetime.now(),
            is_checked=False
        )

        shopping_list_entry_dao.save(new_shopping_list_entry)

        changelog_entry = ChangelogModel(
            author=request.username,
            change_title='Dodano produkt do listy',
            product_id=request.product_id,
            shopping_list_id=request.shopping_list_id,
            created_at=datetime.now()
        )

        changelog_dao.save(changelog_entry)

@router.put("/")
def edit_shopping_list_entry(request: EditShoppingListEntryRequest):
    with get_db() as db_session:
        shopping_list_entry_dao = ShoppingListEntryDao(db_session)
        changelog_dao = ChangelogDao(db_session)

        entry = shopping_list_entry_dao.find_by_id(request.entry_id)
        
        if entry is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        entry.product_id = request.product_id
        entry.quantity = request.quantity
        entry.unit = request.unit
        entry.extra_notes = request.extra_notes

        shopping_list_entry_dao.save(entry)

        changelog_entry = ChangelogModel(
            author=request.username,
            change_title='Edytowano produkt na liście',
            product_id=request.product_id,
            shopping_list_id=entry.shopping_list_id,
            created_at=datetime.now()
        )

        changelog_dao.save(changelog_entry)

@router.patch("/check")
def check_shopping_list_entry(request: CheckShoppingListEntryRequest):
    with get_db() as db_session:
        shopping_list_entry_dao = ShoppingListEntryDao(db_session)
        changelog_dao = ChangelogDao(db_session)

        entry = shopping_list_entry_dao.find_by_id(request.entry_id)

        if entry is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        entry.is_checked = request.checked

        shopping_list_entry_dao.save(entry)

        changelog_entry = ChangelogModel(
            author=request.username,
            change_title='Kupiono' if request.checked else 'Do kupienia',
            product_id=entry.product_id,
            shopping_list_id=entry.shopping_list_id,
            created_at=datetime.now()
        )

        changelog_dao.save(changelog_entry)

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(entry_id: str, username: str):
    with get_db() as db_session:
        shopping_list_entry_dao = ShoppingListEntryDao(db_session)
        changelog_dao = ChangelogDao(db_session)

        entry = shopping_list_entry_dao.find_by_id(entry_id)

        shopping_list_entry_dao.delete_by_id(entry_id)

        changelog_entry = ChangelogModel(
            author=username,
            change_title='Usunięto produkt z listy',
            product_id=entry.product_id,
            shopping_list_id=entry.shopping_list_id,
            created_at=datetime.now()
        )

        changelog_dao.save(changelog_entry)
