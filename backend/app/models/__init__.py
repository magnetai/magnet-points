# app/models/__init__.py
from app.models.schemas import (
    HistoryRecord,
    HourlyGroup,
    HistoryResponse,
    UserPoints
)

__all__ = [
    'HistoryRecord',
    'HourlyGroup',
    'HistoryResponse',
    'UserPoints'
]