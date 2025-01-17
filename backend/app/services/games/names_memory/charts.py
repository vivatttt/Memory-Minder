from backend.app.db.gateway import ImageMemoryStatGateway
from backend.app.db.gateway import ViewedImageGateway
from backend.app.db.connection import get_session
from backend.app.services.games.names_memory.const import images_in_round, asking_in_round
from datetime import datetime
# import matplotlib.pyplot as plt
import io
import re

import matplotlib.pyplot as plt


from sqlalchemy.ext.asyncio import AsyncSession

async def scores_answers(session: AsyncSession, user_id: int):

    correct, incorrect = await ImageMemoryStatGateway.score_answers(
        session=session,
        user_id_in=user_id)

    labels = ['Правильные ответы', 'Неравильные ответы']
    sizes = [correct, incorrect]
    colors = ['#8dca89', '#ff9474']
    plt.figure(figsize=(8, 6))

    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=140
    )

    centre_circle = plt.Circle(
        (0, 0),
        0.70,
        fc='white'
    )
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.axis('equal')
    buf_file_path = 'backend/app/db/data/media/scores_answers.png'

    plt.savefig(buf_file_path, format='png', bbox_inches='tight')
    plt.close()

    return buf_file_path


async def date_game(session: AsyncSession, user_id: int):

    unique_days_count = await ImageMemoryStatGateway.get_unique_played_at_dates(
        session=session,
        user_id_in=user_id)

    dates = list(unique_days_count.keys())
    counts = list(unique_days_count.values())

    plt.figure(figsize=(10, 6))

    plt.bar(dates, counts, color='#8dca89')
    plt.xlabel('Даты')
    plt.ylabel('Количество раундов')
    plt.title('Игры по датам')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.axis('equal')
    buf_file_path = 'backend/app/db/data/media/date_game.png'

    plt.savefig(buf_file_path, format='png', bbox_inches='tight')
    plt.close()

    return buf_file_path


async def scores(session: AsyncSession, user_id: int):

    rounds = await ImageMemoryStatGateway.count_rounds(
        session=session,
        user_id_in=user_id)

    correct, incorrect = await ImageMemoryStatGateway.score_answers(
        session=session,
        user_id_in=user_id)

    unique_day = await ImageMemoryStatGateway.count_unique_played_at(
        session=session,
        user_id_in=user_id)

    return [rounds, round(correct / (correct + incorrect), 2) * 100, unique_day]


