from datetime import datetime

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import models
from backend.app.db.gateway.base import Gateway
from backend.app.schemas import internal_objects


class WordsStatsGateway(Gateway[models.WordsStat, internal_objects.WordsStatsObject]):
    model = models.WordsStat
    object = internal_objects.WordsStatsObject

    @classmethod
    async def create_scores(
        cls,
        session: AsyncSession,
        user_id: int,
        played_at: datetime,
        correct_answers: int,
        all_answers: int
    ):
        session.add(
            cls.model(
                user_id=user_id,
                played_at=played_at,
                correct_answers=correct_answers,
                all_answers=all_answers,
            )
        )
        await session.commit()

    @classmethod
    async def get_answers(cls, session: AsyncSession, user_id: int):
        result = await session.execute(
            select(
                cls.model.correct_answers,
                cls.model.all_answers
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
                func.count())
            .where(
                cls.model.user_id == user_id_in)
            .group_by(
                cls.model.played_at)
        )
        dates_count = {date: count for date, count in result}

        return dates_count