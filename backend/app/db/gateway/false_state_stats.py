from datetime import datetime

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import models
from backend.app.db.gateway.base import Gateway
from backend.app.schemas import internal_objects


class FalseStateStatsGateway(Gateway[models.FalseStateStats, internal_objects.FalseStateStatsObject]):
    model = models.FalseStateStats
    object = internal_objects.FalseStateStatsObject

    @classmethod
    async def create_record(
        cls,
        session: AsyncSession,
        user_id: int,
        won: bool,
        played_at: datetime = None,
        level: int = 1
    ):
        session.add(
            cls.model(
                user_id=user_id,
                played_at=played_at or datetime.now(),
                won=won,
                level=level,
            )
        )
        await session.commit()

    @classmethod
    async def get_records_count(cls, session: AsyncSession, user_id: int, won: bool) -> int:
        count = await session.execute(
            select(func.count()).filter(
                and_(
                    cls.model.user_id == user_id,
                    cls.model.won == won
                )
            )
        )
        return count.scalar()
