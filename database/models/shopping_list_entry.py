from datetime import datetime
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.enums.custom_unit import CustomUnit
from database.models.models_base import Base

if TYPE_CHECKING:
    from database.models.product import ProductModel
    from database.models.shopping_list import ShoppingListModel


class ShoppingListEntryModel(Base):
    __tablename__ = "shopping_list_entries"

    # Fields without default values
    shopping_list_id: Mapped[str] = mapped_column(
        String(128), ForeignKey("shopping_lists.id")
    )
    product_id: Mapped[str] = mapped_column(
        String(128), ForeignKey("products.id")
    )
    quantity: Mapped[Optional[float]] = mapped_column(
        Numeric
    )
    unit: Mapped[Optional[CustomUnit]] = mapped_column(
        Enum('szt.', 'opakowania', 'kg', 'g', 'l', 'ml', '', name='custom_unit_enum')
    )
    extra_notes: Mapped[Optional[str]] = mapped_column(
        String(120)
    )
    last_updated_at: Mapped[datetime] = mapped_column(DateTime)

    # Fields with default values
    id: Mapped[str] = mapped_column(
        String(128), primary_key=True, default_factory=lambda: str(uuid.uuid4()), init=False
    )
    is_checked: Mapped[bool] = mapped_column(
        Boolean(), default=False
    )

    # Relations
    product: Mapped["ProductModel"] = relationship(back_populates="entries", init=False)
    shopping_list: Mapped["ShoppingListModel"] = relationship(back_populates="items", init=False)