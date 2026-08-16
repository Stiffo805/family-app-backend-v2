

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from dao.changelog_dao import ChangelogDao
from database.db import get_db
from util.types import ChangelogEntryResponse


router = APIRouter(tags=["Changelog"])

@router.get("/latest/limit/{limit}")
def get_lastest_entries(limit: int):
    with get_db() as db_session:
        changelog_dao = ChangelogDao(db_session)

        entries = changelog_dao.get_latest_entries_with_limit(limit)

        items = [ChangelogEntryResponse.model_validate(entry) for entry in entries]

        return JSONResponse(content=jsonable_encoder({"items": items}))

@router.get("/")
def get_all_entries():
    with get_db() as db_session:
        changelog_dao = ChangelogDao(db_session)

        entries = changelog_dao.get_all()
        
        items = [ChangelogEntryResponse.model_validate(entry) for entry in entries]

        return JSONResponse(content=jsonable_encoder({"items": items}))