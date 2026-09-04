from datetime import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.models_base import Base

if TYPE_CHECKING:
    from database.models.product import ProductModel
    from database.models.shopping_list import ShoppingListModel

class ChangelogModel(Base):
    __tablename__ = "changelog"

    # Fields without default values
    shopping_list_id: Mapped[Optional[str]] = mapped_column(
        String(128), ForeignKey("shopping_lists.id")
    )
    product_id: Mapped[Optional[str]] = mapped_column(
        String(128), ForeignKey("products.id")
    )
    change_title: Mapped[str] = mapped_column(
        String(120)
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    author: Mapped[Optional[str]] = mapped_column(
        String(120)
    )

    # Fields with default values
    id: Mapped[str] = mapped_column(
        String(128), primary_key=True, default_factory=lambda: str(uuid.uuid4()), init=False
    )

    product: Mapped[Optional["ProductModel"]] = relationship(back_populates="changelog_entries", init=False)
    shopping_list: Mapped[Optional["ShoppingListModel"]] = relationship(back_populates="changelog_entries", init=False)

