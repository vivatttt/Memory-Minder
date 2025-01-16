from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, TIMESTAMP, BIGINT
from sqlalchemy.orm import relationship

from backend.app.db import DeclarativeBase


class FalseStateStats(DeclarativeBase):
    __tablename__ = "false_state_stats"

    id = Column(INTEGER(), primary_key=True)
    user_id = Column(BIGINT(), ForeignKey("users.id"))
    played_at = Column(TIMESTAMP(timezone=True), default=datetime.now)
    won = Column(BOOLEAN())
    level = Column(INTEGER(), default=1)

    user = relationship("User", back_populates="false_state_stats")
