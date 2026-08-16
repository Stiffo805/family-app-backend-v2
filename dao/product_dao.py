
from typing import List, Optional

from sqlalchemy import or_, select

from dao.dao import Dao
from database.models.product import ProductModel


class ProductDao(Dao):

    def get_by_id(self, product_id: str) -> Optional[ProductModel]:
        stmt = select(ProductModel).where(ProductModel.id == product_id)
        return self.db.scalar(stmt)

    def search(self, search_query: str) -> List[ProductModel]:
        stmt = select(ProductModel).where(or_(ProductModel.name.ilike(f"{search_query}%"), ProductModel.name.ilike(f"% {search_query}%")))

        return list(self.db.scalars(stmt))

    def save(self, product: ProductModel) -> ProductModel:
        self.db.add(product)
        self.db.flush()
        return product