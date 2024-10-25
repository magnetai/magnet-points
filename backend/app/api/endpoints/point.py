# app/api/endpoints/score.py
from fastapi import APIRouter, Query
from app.services.point_service import PointService
from app.models.schemas import LeaderboardResponse, UserPoints

router = APIRouter(prefix="/points")
point_service = PointService()
@router.get("/get_user_points")
async def get_user_points(user_id: str):
    return point_service.get_user_points(user_id)

@router.post("/init_t1_point")
async def init_t1_point(t1_points: list[UserPoints]):
    return point_service.init_t1_points(t1_points)

@router.post("/update")
async def update_point(user_points: list[UserPoints]):
    return point_service.update_user_point(user_points)

@router.get("/ardio_alpha/leaderboard", response_model=LeaderboardResponse)
async def get_ardio_alpha_leaderboard(
    page_index: int = Query(1, ge=1, description="Starting position"),
    page_size: int = Query(10, ge=1, le=100, description="Return quantity")
):
    """
    Get ardio alpha points leaderboard
    """
    return await point_service.get_ardio_alpha_leaderboard(page_index, page_size)

@router.get("/magnet_t1/leaderboard", response_model=LeaderboardResponse)
async def get_magnet_t1_leaderboard(
    page_index: int = Query(1, ge=1, description="Starting position"),
    page_size: int = Query(10, ge=1, le=100, description="Return quantity")
):
    """
    Get magnet t1 points leaderboard
    """
    return await point_service.get_magnet_t1_leaderboard(page_index, page_size)