from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import models
from backend.app.db.gateway.base import Gateway
from backend.app.schemas import internal_objects


class ViewedImageGateway(Gateway[models.Viewed_Image, internal_objects.ViewedImageObject]):
    model = models.Viewed_Image
    object = internal_objects.ViewedImageObject

    @classmethod
    async def add_not_guessed_image(cls, session: AsyncSession, user_id: int, image_id: int):
        session.add(
            cls.model(
                user_id=user_id,
                image_id=image_id
            )
        )
        await session.commit()

    @classmethod
    async def count_poor_guessed_image(cls, session: AsyncSession, user_id_in: int):
        total_images_count = await session.scalar(
            select(func.count()).select_from(cls.model).where(cls.model.user_id == user_id_in)
        )

        return total_images_count

    @classmethod
    async def delete_viewed_images_by_user(cls, session: AsyncSession, user_id: int):
        records_to_delete = await session.execute(
            select(cls.model).filter(cls.model.user_id == user_id)
        )
        records_to_delete = records_to_delete.scalars().all()

        if records_to_delete:
            for record in records_to_delete:
                await session.delete(record)
            await session.commit()

    @classmethod
    async def image_ids(cls, session: AsyncSession, user_id: int):
        result = await session.execute(
            select(cls.model.image_id).where(cls.model.user_id == user_id)
        )
        return result.scalars().all()

    @classmethod
    async def delete_image_ids(cls, session: AsyncSession, user_id: int):
        await session.execute(
            delete(cls.model).where(cls.model.user_id == user_id)
        )
        await session.commit()