from backend.app.schemas.internal_objects.base import BaseObject


class UserObject(BaseObject):
    id: int
    name: str
    username: str
    is_admin: bool
