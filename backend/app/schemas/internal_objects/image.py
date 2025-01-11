from backend.app.schemas.internal_objects.base import BaseObject


class ImageObject(BaseObject):
    id: int
    key: str
    name_image: str
