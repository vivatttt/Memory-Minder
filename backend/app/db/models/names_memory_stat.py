from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, DATE, BIGINT

from backend.app.db import DeclarativeBase

class Names_Memory_Stat(DeclarativeBase):
    __tablename__ = 'names_memory_stats'

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    user_id = Column(BIGINT(), nullable=False)
    played_at = Column(DATE(), nullable=False)
    correct_answers = Column(INTEGER(), nullable=False)
    wrong_answers = Column(INTEGER(), nullable=False)