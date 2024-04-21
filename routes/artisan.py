from fastapi import APIRouter
from core import SESSION_DEP

artisan = APIRouter(prefix="/artisan", tags=["artisans"])


@artisan.post(path="/new")
async def create_profile():
    pass


@artisan.get(path="/all")
async def get_all(db_access: SESSION_DEP):
    pass
