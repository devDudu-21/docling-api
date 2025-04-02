from fastapi import APIRouter
from .endpoints import convert

router = APIRouter()
router.include_router(convert.router, prefix="/convert", tags=["convert"])
