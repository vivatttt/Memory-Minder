from backend.app.db.gateway import WordsStatsGateway

from datetime import datetime
import matplotlib.pyplot as plt
from sqlalchemy.ext.asyncio import AsyncSession

async def add_scores_words(
        session: AsyncSession,
        user_id: int,
        correct_answers: int,
        all_answers: int
    ):

    await WordsStatsGateway.create_scores(
        session=session,
        user_id=user_id,
        played_at=datetime.today(),
        correct_answers=correct_answers,
        all_answers=all_answers,
    )


async def date_words(session: AsyncSession, user_id: int):
    unique_days_count = await WordsStatsGateway.get_unique_played_at_dates(
        session=session,
        user_id_in=user_id
    )

    dates = list(unique_days_count.keys())
    counts = list(unique_days_count.values())

    plt.figure(figsize=(10, 6))

    plt.barh(dates, counts, color='#8B0000')
    plt.xlabel('Количество раундов')
    plt.ylabel('Даты')
    plt.title('Игры по датам')
    plt.tight_layout()

    plt.axis('equal')
    buf_file_path = 'backend/app/db/data/media/scores_answers.png'

    plt.savefig(buf_file_path, format='png', bbox_inches='tight')
    plt.close()

    return buf_file_path

async def scores_words(session: AsyncSession, user_id: int):
    n_results = await WordsStatsGateway.get_answers(
        session=session,
        user_id=user_id
    )

    correct_counts = [result[0] for result in n_results]
    all_counts = [result[1] for result in n_results]
    indices = list(range(1, len(n_results) + 1))

    plt.figure(figsize=(10, 6))

    plt.bar(indices, all_counts, label='All', color='#FFDAB9', alpha=0.7)
    plt.bar(indices, correct_counts, label='Correct', color='#8B0000', alpha=0.7)

    plt.xlabel('Раунд')
    plt.ylabel('Количество')
    plt.title('Анализ результатов')
    plt.xticks(indices)
    plt.legend()
    plt.tight_layout()

    plt.axis('equal')
    buf_file_path = 'backend/app/db/data/media/scores_answers.png'

    plt.savefig(buf_file_path, format='png', bbox_inches='tight')
    plt.close()

    return buf_file_path
