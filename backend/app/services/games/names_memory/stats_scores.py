from backend.app.db.gateway import ImageMemoryStatGateway
from backend.app.db.gateway import ViewedImageGateway
from backend.app.services.games.names_memory.const import images_in_round, asking_in_round
from datetime import datetime
import re

from sqlalchemy.ext.asyncio import AsyncSession


async def rounds(session: AsyncSession, user_id: int) -> int:

    res = await ImageMemoryStatGateway.count_rounds(
        session=session,
        user_id_in=user_id)

    return res

async def get_results_round(session: AsyncSession, user_id: int, images: list[tuple], answers: list[str]) -> int:
    result = 0

    for i, y in zip(images, answers):
        cleaned_image_name = ''.join(re.findall(r'[a-zA-Zа-яА-Я0-9]', i[2].lower().replace('ё', 'е')))
        cleaned_expected_name = ''.join(re.findall(r'[a-zA-Zа-яА-Я0-9]', y.lower().replace('ё', 'е')))
        if cleaned_image_name == cleaned_expected_name:
            result += 1
        else:
            await ViewedImageGateway.add_not_guessed_image(session=session, user_id=user_id, image_id=i[0])

    await ImageMemoryStatGateway.add_stat(
        session=session,
        user_id=user_id,
        played_at=datetime.today(),
        correct_answers=result,
        wrong_answers=asking_in_round()-result
    )

    arr = [images[i][2] for i in range(asking_in_round())]

    return result, arr