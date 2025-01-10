from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, TEXT
from sqlalchemy.orm import relationship

from backend.app.db import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(INTEGER(), primary_key=True, autoincrement=False)
    name = Column(TEXT())
    username = Column(TEXT())
    is_admin = Column(BOOLEAN())

    false_state_stats = relationship("FalseStateStats", back_populates="user")
