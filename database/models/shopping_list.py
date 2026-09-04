from datetime import datetime
import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.models_base import Base

if TYPE_CHECKING:
    from database.models.shopping_list_entry import ShoppingListEntryModel
    from database.models.changelog import ChangelogModel


class ShoppingListModel(Base):
    __tablename__ = "shopping_lists"

    # Fields without default values
    title: Mapped[str] = mapped_column(String(330), unique=True)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Fields with default values
    id: Mapped[str] = mapped_column(
        String(128), primary_key=True, default_factory=lambda: str(uuid.uuid4()), init=False
    )

    # Relations
    items: Mapped[List["ShoppingListEntryModel"]] = relationship(back_populates="shopping_list", init=False)
    changelog_entries: Mapped[List["ChangelogModel"]] = relationship(back_populates="shopping_list", init=False)