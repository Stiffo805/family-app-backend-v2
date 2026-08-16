from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.alias_generators import to_camel

from database.enums.custom_unit import CustomUnit

class CamelCaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

class UsernameRequest(CamelCaseSchema):
    username: str

class CheckPasswordRequest(UsernameRequest):
    password: str

class CreateShoppingListRequest(UsernameRequest):
    title: str

class EditShoppingListRequest(UsernameRequest):
    title: str

class CreateProductRequest(CamelCaseSchema):
    name: str

class CreateShoppingListEntryRequest(UsernameRequest):
    shopping_list_id: str
    product_id: str
    quantity: float
    unit: CustomUnit
    extra_notes: str

class EditShoppingListEntryRequest(UsernameRequest):
    entry_id: str
    product_id: str
    quantity: Optional[float]
    unit: CustomUnit
    extra_notes: Optional[str]

class CheckShoppingListEntryRequest(UsernameRequest):
    entry_id: str
    checked: bool

class ProductResponse(CamelCaseSchema):
    id: str
    name: str

class ShoppingListEntryResponse(CamelCaseSchema):
    id: str
    quantity: Optional[float]
    unit: CustomUnit
    extra_notes: Optional[str]
    is_checked: bool
    product: ProductResponse
    last_updated_at: datetime

class ShoppingListResponse(CamelCaseSchema):
    id: str
    title: str
    last_updated_at: datetime
    items: List[ShoppingListEntryResponse]

class ChangelogEntryResponse(CamelCaseSchema):
    id: str
    shopping_list: ShoppingListResponse
    product: Optional[ProductResponse]
    change_title: str
    created_at: datetime
    author: str
