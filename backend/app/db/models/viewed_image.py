from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, BIGINT

from backend.app.db import DeclarativeBase

class Viewed_Image(DeclarativeBase):
    __tablename__ = 'viewed_images'

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    user_id = Column(BIGINT(), nullable=False)
    image_id = Column(INTEGER(), nullable=False)
    used_in_game = Column(INTEGER(), nullable=False)
    correct = Column(INTEGER(), nullable=False)