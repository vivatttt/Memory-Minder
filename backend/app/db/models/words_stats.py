from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, DATE, BIGINT

from backend.app.db import DeclarativeBase

class WordsStat(DeclarativeBase):
    __tablename__ = 'words_stats'

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    user_id = Column(BIGINT(), nullable=False)
    played_at = Column(DATE(), nullable=False)
    correct_answers = Column(INTEGER(), nullable=False)
    all_answers = Column(INTEGER(), nullable=False)