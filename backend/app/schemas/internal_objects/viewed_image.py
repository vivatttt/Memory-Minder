from backend.app.schemas.internal_objects.base import BaseObject


class ViewedImageObject(BaseObject):
    id: int
    user_id: int
    image_id: int
    used_in_game: int
    correct: int