import uuid

from backend.app.schemas.internal_objects.base import BaseObject


class UserObject(BaseObject):
    id: uuid.UUID
    name: str
    is_admin: bool
