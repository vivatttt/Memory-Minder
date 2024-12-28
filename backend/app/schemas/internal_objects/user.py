from backend.app.schemas.internal_objects.base import BaseObject
import uuid

class UserObject(BaseObject):
    id: uuid.UUID
    name: str
    is_admin: bool