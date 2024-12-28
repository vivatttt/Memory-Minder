import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, UUID, BOOLEAN

from backend.app.db import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    name = Column(TEXT())
    is_admin = Column(BOOLEAN())