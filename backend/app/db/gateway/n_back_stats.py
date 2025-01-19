from datetime import datetime

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import models
from backend.app.db.gateway.base import Gateway
from backend.app.schemas import internal_objects


class NBackStatsGateway(Gateway[models.NBackStat, internal_objects.NBackStatsObject]):
    model = models.NBackStat
    object = internal_objects.NBackStatsObject

    @classmethod
    async def create_scores(
        cls,
        session: AsyncSession,
        user_id: int,
        played_at: datetime,
        correct_answers: int,
        wrong_answers: int,
        percentage: int,
        n_level: int,
    ):
        session.add(
            cls.model(
                user_id=user_id,
                played_at=played_at,
                correct_answers=correct_answers,
                wrong_answers=wrong_answers,
                percentage=percentage,
                n_level=n_level,
            )
        )
        await session.commit()

    @classmethod
    async def get_average_percentage(cls, session: AsyncSession, user_id: int):
        result = await session.execute(
            select(
                cls.model.n_level,
                func.avg(cls.model.percentage).label('average_percentage')
            ).filter(
                cls.model.user_id == user_id
            ).group_by(
                cls.model.n_level
            )
        )

        average_percentage_dict = {row[0]: int(row[1]) for row in result.all()}
        return average_percentage_dict

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

    @classmethod
    async def score_answers(cls, session: AsyncSession, user_id_in: int):
        correct = await session.execute(
            select(
                func.sum(cls.model.correct_answers)
            )
            .where(
                cls.model.user_id == user_id_in
            )
        )
        wrong = await session.execute(
            select(
                func.sum(cls.model.wrong_answers)
            ).where(
                cls.model.user_id == user_id_in
            )
        )

        correct_sum = correct.scalar() or 0
        wrong_sum = wrong.scalar() or 0

        return correct_sum, wrong_sum