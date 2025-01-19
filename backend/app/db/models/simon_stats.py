from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, DATE, BIGINT

from backend.app.db import DeclarativeBase

class SimonStat(DeclarativeBase):
    __tablename__ = 'simon_stats'

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    user_id = Column(BIGINT(), nullable=False)
    played_at = Column(DATE(), nullable=False)
    all_length = Column(INTEGER(), nullable=False)