жйЖЙfrom sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import models
from backend.app.db.gateway.base import Gateway
from backend.app.schemas import internal_objects


class ImageGateway(Gateway[models.Image, internal_objects.ImageObject]):
    model = models.Image
    object = internal_objects.ImageObject

    @classmethod
    async def title_for_game(cls, session: AsyncSession, image_id: int):
        image_name = await session.scalar(
            select(cls.model.name_image).where(cls.model.id == image_id)
        )

        return image_name

    @classmethod
    async def add_image(cls, session: AsyncSession, key: str, name_image: str):
        session.add(
            cls.model(
                key=key,
                name_image=name_image
            )
        )
        await session.commit()

    @classmethod
    async def count_images(cls, session: AsyncSession):
        total_images_count = await session.scalar(
            select(func.count()).select_from(cls.model)
        )

        return total_images_count

    # @classmethod
    # async def get_images(cls, session: AsyncSession, filter_id: int, images_in_round: int):
    #     result = await session.execute(
    #         select(cls.model)
    #         .filter(cls.model.id >= filter_id)
    #         .limit(images_in_round)
    #     )
    #     guessed_images = result.scalars().all()
    #
    #     return cls.object.model_validate(guessed_images)

    async def get_images(cls, session: AsyncSession, filter_id: int, images_in_round: int):
        result = await session.execute(
            select(cls.model)
            .filter(cls.model.id >= filter_id)
            .limit(images_in_round)
        )
        guessed_images = result.scalars().all()

        # Преобразуем каждый объект в словарь вручную
        image_dicts = [
            {
                'id': image.id,  # Предположим, что у вашего объекта есть атрибут id
                'key': image.key,  # Замените на ваши реальные атрибуты
                'name_image': image.name_image,  # Замените на ваши реальные атрибуты
                # Добавьте другие необходимые поля
            }
            for image in guessed_images
        ]

        # Теперь передаем список словарей в модель валидации
        validated_images = [cls.object.model_validate(image_dict) for image_dict in image_dicts]

        return validated_images