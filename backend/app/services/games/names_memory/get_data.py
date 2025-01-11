from backend.app.db.gateway import ImageGateway
from backend.app.db.gateway import ImageMemoryStatGateway
from backend.app.db.gateway import ViewedImageGateway
from backend.app.db.connection import get_session
from backend.app.services.games.names_memory.const import images_in_round, asking_in_round, get_site

import random

from sqlalchemy.ext.asyncio import AsyncSession

image = ImageGateway()

async def get_images(session: AsyncSession, user_id: int) -> list[tuple[int, str, str]]:

    res = await ImageMemoryStatGateway.count_rounds(
        session=session,
        user_id_in=user_id
    )

    if res % 5 == 0:

        print("nes")

        res = await image.get_images(
            session=session,
            filter_id=res*images_in_round(),
            images_in_round=images_in_round()
        )
    else:

        print("change")

        res = await image.get_images(
            session=session,
            filter_id=res * images_in_round(),
            images_in_round=images_in_round()
        )

    arr = [(i.id, get_site() + i.key, i.name_image) for i in res]
    return arr

