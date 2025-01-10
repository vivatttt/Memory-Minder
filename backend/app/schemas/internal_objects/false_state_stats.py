from datetime import datetime

from backend.app.schemas.internal_objects.base import BaseObject


class FalseStateStatsObject(BaseObject):
    id: int
    user_id: int
    played_at: datetime
    won: bool
    level: int = 1
