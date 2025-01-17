import uuid
from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")
OBJ = TypeVar("OBJ")

class Gateway(Generic[T, OBJ]):
    model: Type[T] = None
    object: Type[OBJ] = None

    @classmethod
    async def get_by_id(
        cls, session: AsyncSession, id_: int | str | uuid.UUID
    ) -> OBJ | None:
        try:
            res = await session.get(cls.model, id_)
            return cls.object.model_validate(res)
        except Exception:
            return None
