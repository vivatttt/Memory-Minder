from datetime import datetime

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import models
from backend.app.db.gateway.base import Gateway
from backend.app.schemas import internal_objects


class SimonStatsGateway(Gateway[models.SimonStat, internal_objects.SimonStatsObject]):
    model = models.SimonStat
    object = internal_objects.SimonStatsObject

    @classmethod
    async def create_scores(
        cls,
        session: AsyncSession,
        user_id: int,
        played_at: datetime,
        all_length: int
    ):
        session.add(
            cls.model(
                user_id=user_id,
                played_at=played_at,
                all_length=all_length
            )
        )
        await session.commit()

    @classmethod
    async def get_length(cls, session: AsyncSession, user_id: int):
        result = await session.execute(
            select(
                cls.model.all_length
            ).filter(
                cls.model.user_id == user_id
            )
        )

        return result.all()

    @classmethod
    async def get_unique_played_at_dates(cls, session: AsyncSession, user_id_in: int):
        result = await session.execute(
            select(
                cls.model.played_at,
                func.count()
            ).where(
                cls.model.user_id == user_id_in)
            .group_by(
                cls.model.played_at
            )
        )
        dates_count = {date: count for date, count in result}

        return dates_count