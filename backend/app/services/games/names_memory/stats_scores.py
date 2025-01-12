from backend.app.db.gateway import ImageGateway
from backend.app.db.gateway import ImageMemoryStatGateway
from backend.app.db.gateway import ViewedImageGateway
from backend.app.db.connection import get_session
from backend.app.services.games.names_memory.const import images_in_round, asking_in_round
from datetime import datetime
import re

from sqlalchemy.ext.asyncio import AsyncSession


# async def write_stats(session: AsyncSession, user_id: int, won: bool) -> None:
#     await FalseStateStatsGateway.create_record(session=session, user_id=user_id, won=won)
#
# async def get_game_stats(session: AsyncSession, user_id: int) -> tuple[int]:
#     won_count = await FalseStateStatsGateway.get_records_count(session=session, user_id=user_id, won=True)
#     lost_count = await FalseStateStatsGateway.get_records_count(session=session, user_id=user_id, won=False)
#     return won_count, lost_count

async def rounds(session: AsyncSession, user_id: int) -> int:

    res = await ImageMemoryStatGateway.count_rounds(
        session=session,
        user_id_in=user_id)

    return res

async def get_results_round(session: AsyncSession, user_id: int, images: list[tuple], answers: list[str]) -> int:
    result = 0

    for i, y in zip(images, answers):
        cleaned_image_name = ''.join(re.findall(r'[a-zA-Zа-яА-Я0-9]', i[2].lower()))
        cleaned_expected_name = ''.join(re.findall(r'[a-zA-Zа-яА-Я0-9]', y.lower()))
        if cleaned_image_name == cleaned_expected_name:
            result += 1
        else:
            continue
            # await ViewedImageGateway.add_not_guessed_image(session=session, user_id=user_id, image_id=i[0], used_in_game=5, correct=2)

    await ImageMemoryStatGateway.add_stat(
        session=session,
        user_id=user_id,
        played_at=datetime.today(),
        correct_answers=result,
        wrong_answers=asking_in_round()-result
    )

    arr = [images[i][2] for i in range(asking_in_round())]

    return result, arr