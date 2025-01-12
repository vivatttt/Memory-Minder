from backend.app.db.gateway import ImageGateway
from backend.app.db.gateway import ImageMemoryStatGateway
from backend.app.db.gateway import ViewedImageGateway
from backend.app.db.connection import get_session
from backend.app.services.games.names_memory.const import images_in_round, asking_in_round
from datetime import datetime
import matplotlib.pyplot as plt
import io
import re

from sqlalchemy.ext.asyncio import AsyncSession

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

    return [rounds, correct, incorrect, round(correct / (correct + incorrect), 2) * 100, unique_day]

