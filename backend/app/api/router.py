# app/api/router.py
from fastapi import APIRouter
from app.api.endpoints import point

router = APIRouter()
router.include_router(point.router, tags=["score"])