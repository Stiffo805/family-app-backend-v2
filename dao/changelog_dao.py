from typing import List

from sqlalchemy import select

from dao.dao import Dao
from database.models.changelog import ChangelogModel

from sqlalchemy.orm import Session, selectinload

from database.models.shopping_list import ShoppingListModel


class ChangelogDao(Dao):

    def get_latest_entries_with_limit(self, limit: int) -> List[ChangelogModel]:
        stmt = select(ChangelogModel).order_by(ChangelogModel.created_at.desc()).limit(limit).options(
            selectinload(ChangelogModel.product),
            selectinload(ChangelogModel.shopping_list).options(
                selectinload(ShoppingListModel.items)
            )
        )
        return list(self.db.scalars(stmt).all())

    def get_all(self) -> List[ChangelogModel]:
        stmt = select(ChangelogModel).order_by(ChangelogModel.created_at.desc()).options(
            selectinload(ChangelogModel.product),
            selectinload(ChangelogModel.shopping_list)
        )
        return list(self.db.scalars(stmt).all())

    def save(self, changelog_item: ChangelogModel) -> ChangelogModel:
        self.db.add(changelog_item)
        self.db.flush()
        return changelog_item