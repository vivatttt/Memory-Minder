from datetime import datetime

from backend.app.schemas.internal_objects.base import BaseObject


class WordsStatsObject(BaseObject):
    id: int
    user_id: int
    played_at: datetime
    correct_answers: int
    all_answers: int
