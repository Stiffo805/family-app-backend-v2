import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from database.models.models_base import Base

if TYPE_CHECKING:
    from database.models.shopping_list_entry import ShoppingListEntryModel
    from database.models.changelog import ChangelogModel

class ProductModel(Base):
    __tablename__ = "products"

    # Fields without default values
    name: Mapped[str] = mapped_column(String(330), unique=True)

    # Fields with default values
    id: Mapped[str] = mapped_column(
        String(128), primary_key=True, default_factory=lambda: str(uuid.uuid4()), init=False
    )

    # Relations
    entries: Mapped[List["ShoppingListEntryModel"]] = relationship(back_populates="product", init=False)
    changelog_entries: Mapped[List["ChangelogModel"]] = relationship(back_populates="product", init=False)

    @validates("name")
    def validate_name(self, key: str, value: str) -> str:
        if value:
            return value.strip().capitalize()
        return value