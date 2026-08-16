from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from dao.dao import Dao
from database.models.shopping_list_entry import ShoppingListEntryModel

class ShoppingListEntryDao(Dao):

    def find_by_id(self, entry_id: str) -> Optional[ShoppingListEntryModel]:
        stmt = select(ShoppingListEntryModel).where(ShoppingListEntryModel.id == entry_id)
        return self.db.scalar(stmt)

    def delete_by_id(self, entry_id: str) -> None:
        stmt = delete(ShoppingListEntryModel).where(ShoppingListEntryModel.id == entry_id)
        self.db.execute(stmt)

    def save(self, shopping_list_entry: ShoppingListEntryModel) -> ShoppingListEntryModel:
        self.db.add(shopping_list_entry)
        self.db.flush()
        return shopping_list_entry