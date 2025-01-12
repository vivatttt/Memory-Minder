import asyncio

from backend.app.db.connection import get_session
from backend.app.db.gateway.user import UserGateway
from backend.app.db.gateway import ImageMemoryStatGateway, ImageGateway, ViewedImageGateway
from datetime import datetime

async def test():
    async for session in get_session():
        stat = ImageMemoryStatGateway()
        #
        # await stat.add_stat(session=session, user_id=1, played_at=datetime.now(), correct_answers=2, wrong_answers=4)
        # await stat.add_stat(session=session, user_id=1, played_at=datetime.now(), correct_answers=3, wrong_answers=4)
        # await stat.add_stat(session=session, user_id=3, played_at=datetime.now(), correct_answers=2, wrong_answers=2)
        # res = await stat.count_rounds(session=session, user_id_in=1)
        # print(res)
        await stat.delete_stat(session=session, user_id=1297075691)
        # res = await stat.count_rounds(session=session, user_id_in=1)
        # print(res)
        # res = await stat.count_rounds(session=session, user_id_in=3)
        # print(res)
        #
        #
        # stat = ImageGateway()
        #
        # res = await stat.title_for_game(session=session, image_id=1)
        # print(res)
        # res = await stat.title_for_game(session=session, image_id=2)
        # print(res)
        # print('\n\n')
        #
        # res = await stat.count_images(session=session)
        # print(res)
        # print('\n\n')
        #
        # res = await stat.get_images(session=session, filter_id=3, images_in_round=5)
        # print(*res)
        # res = await stat.get_images(session=session, filter_id=1, images_in_round=5)
        # print('\n\n')
        # print([i.key for i in res])


        # stat = ViewedImageGateway()
        #
        # await stat.add_not_guessed_image(session=session, user_id=1, image_id=1, used_in_game=16, correct=2)
        # await stat.add_not_guessed_image(session=session, user_id=1, image_id=2, used_in_game=16, correct=2)
        # await stat.add_not_guessed_image(session=session, user_id=2, image_id=3, used_in_game=5, correct=2)
        # await stat.add_not_guessed_image(session=session, user_id=2, image_id=4, used_in_game=2, correct=2)
        #
        # res = await stat.count_poor_guessed_image(session=session, user_id_in=2)
        # print(res)
        # print('\n\n')
        #
        # await stat.delete_viewed_images_by_user(session=session, user_id=1)
        #
        # res = await stat.count_poor_guessed_image(session=session, user_id_in=1)
        # print(res)



if __name__ == "__main__":
    asyncio.run(test())
