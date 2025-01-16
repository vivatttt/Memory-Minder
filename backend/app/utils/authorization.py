from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.gateway.user import UserGateway
from backend.app.schemas.internal_objects import UserObject


async def check_if_user_authorized(id_: int, session: AsyncSession) -> bool:
    user = await UserGateway.get_by_id(session=session, id_=id_)
    return user is not None

async def authorize_user(user: UserObject, session: AsyncSession) -> None:
    await UserGateway.add_user(
        session=session,
        id_=user.id,
        name=user.name,
        username=user.username,
        is_admin=user.is_admin
    )
