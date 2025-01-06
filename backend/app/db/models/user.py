from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BOOLEAN, TEXT, INTEGER

from backend.app.db import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(INTEGER(), primary_key=True, autoincrement=False)
    name = Column(TEXT())
    username = Column(TEXT())
    is_admin = Column(BOOLEAN())