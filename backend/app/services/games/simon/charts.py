from backend.app.db.gateway import SimonStatsGateway

from datetime import datetime
import matplotlib.pyplot as plt
from sqlalchemy.ext.asyncio import AsyncSession

async def add_scores_simon(
        session: AsyncSession,
        user_id: int,
        all_length: int
    ):

    await SimonStatsGateway.create_scores(
        session=session,
        user_id=user_id,
        played_at=datetime.today(),
        all_length=all_length,
    )

async def scores_length(session: AsyncSession, user_id: int):
    length_results = await SimonStatsGateway.get_length(
        session=session,
        user_id=user_id
    )

    lengths = [result[0] for result in length_results]
    indices = list(range(1, len(lengths) + 1))

    plt.figure(figsize=(10, 6))

    plt.plot(indices, lengths, label='Длина', color='#D2691E', linewidth=2)

    plt.fill_between(indices, lengths, color='#F4A460', alpha=0.3)

    plt.xlabel('Раунд')
    plt.ylabel('Длина цепочки')
    plt.title('Анализ результатов')
    plt.xticks(indices)
    plt.legend()
    plt.tight_layout()

    plt.axis('equal')
    buf_file_path = 'backend/app/db/data/media/scores_answers.png'

    plt.savefig(buf_file_path, format='png', bbox_inches='tight')
    plt.close()

    return buf_file_path

async def date_simon(session: AsyncSession, user_id: int):
    unique_days_count = await SimonStatsGateway.get_unique_played_at_dates(
        session=session,
        user_id_in=user_id
    )

    dates = list(unique_days_count.keys())
    counts = list(unique_days_count.values())

    plt.figure(figsize=(10, 6))

    plt.barh(dates, counts, color='#D2691E')
    plt.xlabel('Количество раундов')
    plt.ylabel('Даты')
    plt.title('Игры по датам')
    plt.tight_layout()

    plt.axis('equal')
    buf_file_path = 'backend/app/db/data/media/scores_answers.png'

    plt.savefig(buf_file_path, format='png', bbox_inches='tight')
    plt.close()

    return buf_file_path