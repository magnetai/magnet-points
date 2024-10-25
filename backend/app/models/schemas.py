from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class HistoryRecord(BaseModel):
    user_id: str
    session: str
    message: str
    record_id: int
    timestamp: int

class HourlyGroup(BaseModel):
    hour_timestamp: int
    count: int
    records: List[HistoryRecord]

class HistoryResponse(BaseModel):
    total: int
    start_time: Optional[int]
    end_time: int
    data: List[HourlyGroup]
    error: Optional[str] = None

class UserPoint(BaseModel):
    user_id: str
    point: int
    rank: int
    # message_count: int
    # last_message_time: int

class LeaderboardResponse(BaseModel):
    total_users: int
    leaderboard: List[UserPoint]
    user_rank: Optional[UserPoint] = None  # Ranking information of current query user

class UserScoreResponse(BaseModel):
    user_id: str
    score: int
    message_count: int
    last_message_time: int

class UserPoints(BaseModel):
    user_id: str
    points: int