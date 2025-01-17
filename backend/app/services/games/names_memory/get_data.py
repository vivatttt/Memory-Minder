from backend.app.db.gateway import ImageGateway
from backend.app.db.gateway import ImageMemoryStatGateway
from backend.app.db.gateway import ViewedImageGateway
from backend.app.services.games.names_memory.const import images_in_round, asking_in_round, get_site

import random
from sqlalchemy.ext.asyncio import AsyncSession

image = ImageGateway()


async def get_images(session: AsyncSession, user_id: int) -> tuple[list[tuple[int, str, str]], bool]:
    wrong_answers = await ViewedImageGateway.count_poor_guessed_image(
        session=session,
        user_id_in=user_id
    )

    entered_if = False

    if wrong_answers < images_in_round():
        entered_if = True
        res = await ImageMemoryStatGateway.count_rounds(
            session=session,
            user_id_in=user_id
        )

        check = await image.count_images(session=session)
        images_count = images_in_round()

        if (res * images_count + images_count) > check:
            res = ((res * images_count + images_count) % check) + 1

        res = await image.get_images(
            session=session,
            filter_id=res * images_count,
            images_in_round=images_count
        )
    else:
        res = []
        images = await ViewedImageGateway.image_ids(
            session=session,
            user_id=user_id
        )
        for id_image in images:
            img = await image.get_image_by_id(
                session=session,
                filter_id=id_image
            )
            res.append(img)
        await ViewedImageGateway.delete_image_ids(
            session=session,
            user_id=user_id
        )

    arr = [(i.id, get_site() + i.key, i.name_image) for i in res]
    return arr, entered_if


async def change_images(images: list[tuple]) -> list[tuple[int, str, str]]:
    for i in range(len(images) - 2, len(images)):
        images[i] = (images[i][0], images[i][1], "НЕ БЫЛО")
    random.shuffle(images)

    return images