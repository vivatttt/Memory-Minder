from backend.app.db.gateway import NBackStatsGateway

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import matplotlib.pyplot as plt

async def add_scores_n_back(
        session: AsyncSession,
        user_id: int,
        correct_answers: int,
        wrong_answers: int,
        percentage: int,
        n_level: int
    ):

    await NBackStatsGateway.create_scores(
        session=session,
        user_id=user_id,
        played_at=datetime.today(),
        correct_answers=correct_answers,
        wrong_answers=wrong_answers,
        percentage=percentage,
        n_level=n_level,
    )

async def scores_n_back(session: AsyncSession, user_id: int):

    n_results = await NBackStatsGateway.get_average_percentage(
        session=session,
        user_id=user_id
    )

    dates = list(n_results.keys())
    counts = list(n_results.values())

    plt.figure(figsize=(10, 6))

    plt.bar(dates, counts, color='#DA70D6')
    plt.xlabel('N - значение')
    plt.ylabel('Успех в процентах')
    plt.title('Анализ раундов')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.axis('equal')
    buf_file_path = 'backend/app/db/data/media/scores_answers.png'

    plt.savefig(buf_file_path, format='png', bbox_inches='tight')
    plt.close()

    return buf_file_path


async def date_n_back(session: AsyncSession, user_id: int):
    unique_days_count = await NBackStatsGateway.get_unique_played_at_dates(
        session=session,
        user_id_in=user_id
    )

    dates = list(unique_days_count.keys())
    counts = list(unique_days_count.values())

    plt.figure(figsize=(10, 6))

    plt.bar(dates, counts, color='#9370DB')
    plt.xlabel('Даты')
    plt.ylabel('Количество раундов')
    plt.title('Игры по датам')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.axis('equal')
    buf_file_path = 'backend/app/db/data/media/scores_answers.png'

    plt.savefig(buf_file_path, format='png', bbox_inches='tight')
    plt.close()

    return buf_file_path


async def answers_n_back(session: AsyncSession, user_id: int):
    correct, incorrect = await NBackStatsGateway.score_answers(
        session=session,
        user_id_in=user_id
    )


    labels = ['Правильные ответы', 'Неправильные ответы']
    sizes = [correct, incorrect]
    colors = ['#9370DB', '#DA70D6']
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
        0.30,
        fc='white'
    )

    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.axis('equal')
    buf_file_path = 'backend/app/db/data/media/scores_answers.png'

    plt.savefig(buf_file_path, format='png', bbox_inches='tight')
    plt.close()

    return buf_file_path