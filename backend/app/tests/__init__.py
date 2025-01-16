import asyncio

from backend.app.db.connection import get_session
from backend.app.db.gateway.user import UserGateway
from backend.app.db.gateway import ImageMemoryStatGateway, ImageGateway, ViewedImageGateway
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import io
from PIL import Image

async def test():
    async for session in get_session():
        # stat = ImageMemoryStatGateway()
        #
        # await stat.add_stat(session=session, user_id=1, played_at=datetime.now(), correct_answers=2, wrong_answers=4)
        # await stat.add_stat(session=session, user_id=1, played_at=datetime.now(), correct_answers=3, wrong_answers=4)
        # await stat.add_stat(session=session, user_id=3, played_at=datetime.now(), correct_answers=2, wrong_answers=2)
        # res = await stat.count_rounds(session=session, user_id_in=1)
        # print(res)
        # await stat.delete_stat(session=session, user_id=1297075691)
        # cor, wro = await stat.score_answers(session=session, user_id_in=1297075691)
        # print(cor, wro)
        # res = await stat.count_rounds(session=session, user_id_in=3)
        # print(res)
        #
        #
        stat = ImageGateway()
        # res = await stat.delete_all(session=session)
        #
        # res = await stat.title_for_game(session=session, image_id=1)
        # print(res)
        # res = await stat.title_for_game(session=session, image_id=2)
        # print(res)
        # print('\n\n')
        #
        res = await stat.count_images(session=session)
        print(res)
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
        # # print(res)
        # correct, incorrect = await ImageMemoryStatGateway.score_answers(session=session, user_id_in=1297075691)
        # print(correct, incorrect )
        #
        # labels = ['Правильные', 'Неправильные']
        # sizes = [correct, incorrect]
        # colors = ['#4CAF50', '#FF5733']
        #
        # fig, ax = plt.subplots()
        # wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        #
        # # Создаем "дыру" в центре
        # centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        # fig.gca().add_artist(centre_circle)
        #
        # # Рисуем диаграмму
        # ax.axis('equal')  # Равные оси для круга
        # plt.title('Распределение ответов')
        #
        # # Сохраняем изображение в байтовом потоке
        # buf = io.BytesIO()
        # plt.savefig(buf, format='png')
        # buf.seek(0)
        # plt.close(fig)
        #
        # img = Image.open(buf)
        #
        # buffered_img = io.BytesIO()
        # img.save(buffered_img, format="PNG")
        # buffered_img.seek(0)
        #
        # buffered_img.read()
        # response = requests.post(url, files=files)
        #
        #
        # if response.status_code == 200:
        #     try:
        #         data = response.json()
        #         print('Изображение успешно загружено! URL:', data['url'])
        #     except ValueError as e:
        #         print('Ошибка при декодировании JSON:', e)
        #         print('Ответ сервера:', response.text)
        # else:
        #     print('Ошибка при загрузке изображения:', response.status_code, response.text)



if __name__ == "__main__":
    asyncio.run(test())
