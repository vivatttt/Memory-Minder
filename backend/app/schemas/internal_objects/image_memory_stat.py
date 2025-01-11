from backend.app.schemas.internal_objects.base import BaseObject
from datetime import datetime


class ImageMemoryStatObject(BaseObject):
    id: int
    user_id: int
    played_at: datetime
    correct_answers: int
    wrong_answers: int