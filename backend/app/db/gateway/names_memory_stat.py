from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from backend.app.db import models
from backend.app.db.gateway.base import Gateway
from backend.app.schemas import internal_objects


class ImageMemoryStatGateway(Gateway[models.Names_Memory_Stat, internal_objects.ImageMemoryStatObject]):
    model = models.Names_Memory_Stat
    object = internal_objects.ImageMemoryStatObject

    @classmethod
    async def add_stat(cls, session: AsyncSession, user_id: int, played_at: datetime, correct_answers: int, wrong_answers: int):
        session.add(
            cls.model(
                user_id=user_id,
                played_at=played_at,
                correct_answers=correct_answers,
                wrong_answers=wrong_answers
            )
        )
        await session.commit()

    @classmethod
    async def count_rounds(cls, session: AsyncSession, user_id_in: int):
        total_images_count = await session.scalar(
            select(func.count()).select_from(cls.model).where(cls.model.user_id == user_id_in)
        )

        return total_images_count

    @classmethod
    async def delete_stat(cls, session: AsyncSession, user_id: int):
        records_to_delete = await session.execute(
            select(cls.model).filter(cls.model.user_id == user_id)
        )
        records_to_delete = records_to_delete.scalars().all()

        if records_to_delete:
            for record in records_to_delete:
                await session.delete(record)
            await session.commit()


    @classmethod
    async def score_answers(cls, session: AsyncSession, user_id_in: int):
        correct = await session.execute(
            select(func.sum(cls.model.correct_answers)).where(cls.model.user_id == user_id_in)
        )
        wrong = await session.execute(
            select(func.sum(cls.model.wrong_answers)).where(cls.model.user_id == user_id_in)
        )

        correct_sum = correct.scalar() or 0
        wrong_sum = wrong.scalar() or 0

        return correct_sum, wrong_sum

    @classmethod
    async def count_unique_played_at(cls, session: AsyncSession, user_id_in: int):
        unique_played_at_count = await session.execute(
            select(func.count(func.distinct(cls.model.played_at))).where(cls.model.user_id == user_id_in)
        )

        return unique_played_at_count.scalar() or 0