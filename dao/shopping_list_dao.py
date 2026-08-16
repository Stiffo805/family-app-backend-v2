from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from dao.dao import Dao
from database.models.product import ProductModel
from database.models.shopping_list import ShoppingListModel
from database.models.shopping_list_entry import ShoppingListEntryModel

class ShoppingListDao(Dao):
    def get_all(self) -> List[ShoppingListModel]:
        stmt = select(ShoppingListModel)

        return list(self.db.scalars(stmt).all())

    def get_by_id(self, shopping_list_id: str) -> Optional[ShoppingListModel]:
        stmt = select(ShoppingListModel).where(ShoppingListModel.id == shopping_list_id).options(
            selectinload(ShoppingListModel.items).options(
                selectinload(ShoppingListEntryModel.product)
            )
        )

        return self.db.scalar(stmt)

    def save(self, shopping_list: ShoppingListModel) -> ShoppingListModel:
        self.db.add(shopping_list)
        self.db.flush()
        return shopping_list