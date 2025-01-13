from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, INTEGER

from backend.app.db import DeclarativeBase

class Image(DeclarativeBase):
    __tablename__ = 'images'

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    key = Column(TEXT(), nullable=False)
    name_image = Column(TEXT(), nullable=False)