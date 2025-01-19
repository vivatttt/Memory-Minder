from datetime import datetime

from backend.app.schemas.internal_objects.base import BaseObject


class SimonStatsObject(BaseObject):
    id: int
    user_id: int
    played_at: datetime
    all_length: int
