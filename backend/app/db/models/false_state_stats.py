from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import BOOLEAN, TEXT, INTEGER

from backend.app.db import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(INTEGER(), primary_key=True)
    user_id = Column(INTEGER(), ForeignKey('users.id'))
    
    user = relationship("User", back_populates="images")