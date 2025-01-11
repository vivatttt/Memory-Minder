from backend.app.db.gateway import ImageGateway
from backend.app.db.gateway import ImageMemoryStatGateway
from backend.app.db.gateway import ViewedImageGateway
from backend.app.db.connection import get_session
from backend.app.services.games.names_memory.const import images_in_round, asking_in_round, get_site

import random

from sqlalchemy.ext.asyncio import AsyncSession

async def get_images(session: AsyncSession, user_id: int) -> list[tuple[int, str, str]]:

    res = await ImageMemoryStatGateway.count_rounds(
        session=session,
        user_id_in=user_id
    )

    res = await ImageGateway.get_images(
        session=session,
        filter_id=res*images_in_round,
        images_in_round=images_in_round
    )

    arr = [(i.id, get_site + i.key, i.name_image) for i in res]

    # site = 'https://i.postimg.cc/'
    # arr = [(site + 'ZqxV778J/yiannis-tsaroychis-p308-1.jpg', '1'),
    #        (site + 'mr5ZQ3mV/edward-hopper-summertime.jpg', 'ffff'),
    #        (site + 'PqxrpVQP/edward-hopper-sunday.jpg', '7'),
    #        (site + 'gJLz4w5p/george-luks-frank-crane.jpg', '8'),
    #        (site + 'QCLXz8GT/george-luks-girl-with-doll.jpg', '9'),
    #        (site + 'D0q2k9nY/george-luks-havana-cuba-1896.jpg', '10'),
    #        (site + 'v898VVfL/george-luks-hitch-team-1916.jpg', '11'),
    #        ]
    print(arr)

    return arr

