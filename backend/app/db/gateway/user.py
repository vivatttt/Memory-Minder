from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import models
from backend.app.db.gateway.base import Gateway
from backend.app.schemas import internal_objects


class UserGateway(Gateway[models.User, internal_objects.UserObject]):
    model = models.User
    object = internal_objects.UserObject

    @classmethod
    async def get_by_name(cls, session: AsyncSession, name: str):
        data_from_db = await session.scalar(
            select(cls.model).where(cls.model.name == name)
        )
        return cls.object.model_validate(data_from_db)

    @classmethod
    async def add_user(cls, session: AsyncSession, id_: int, name: str, username: str, is_admin: bool):
        session.add(
            cls.model(
                id=id_,
                name=name,
                username=username,
                is_admin=is_admin
            )
        )
        await session.commit()

    @classmethod
    async def get_admin(cls, session: AsyncSession, id: int):
        data_from_db = await session.scalar(
            select(cls.model.is_admin).where(cls.model.id == id)
        )
        return data_from_db

    @classmethod
    async def get_telegram_ids(cls, session: AsyncSession):
        result = await session.execute(
            select(cls.model.id).where(cls.model.is_admin == False)
        )

        telegram_ids = result.scalars().all()
        return telegram_ids