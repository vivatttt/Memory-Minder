from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.gateway import FalseStateStatsGateway


async def write_stats(session: AsyncSession, user_id: int, won: bool) -> None:
    await FalseStateStatsGateway.create_record(session=session, user_id=user_id, won=won)

async def get_game_stats(session: AsyncSession, user_id: int) -> tuple[int]:
    won_count = await FalseStateStatsGateway.get_records_count(session=session, user_id=user_id, won=True)
    lost_count = await FalseStateStatsGateway.get_records_count(session=session, user_id=user_id, won=False)
    return won_count, lost_count




