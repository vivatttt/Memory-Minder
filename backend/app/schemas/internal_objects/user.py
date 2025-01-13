from backend.app.schemas.internal_objects.base import BaseObject


class UserObject(BaseObject):
    id: int
    name: str
    username: str | None
    is_admin: bool
