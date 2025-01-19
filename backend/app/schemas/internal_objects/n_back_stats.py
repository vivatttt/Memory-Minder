from datetime import datetime

from backend.app.schemas.internal_objects.base import BaseObject


class NBackStatsObject(BaseObject):
    id: int
    user_id: int
    played_at: datetime
    correct_answers: int
    wrong_answers: int
    percentage: int
    n_level: int
