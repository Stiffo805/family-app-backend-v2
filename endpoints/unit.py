from fastapi import APIRouter
from database.enums.custom_unit import all_units

router = APIRouter(tags=["Units"])

@router.get("/")
def get_all_units():
    return {"items": all_units}