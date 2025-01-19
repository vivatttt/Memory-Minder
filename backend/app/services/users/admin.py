from backend.app.db.gateway import UserGateway

async def check_info(session, id):
    return await UserGateway.get_admin(session=session, id=id)

async def get_id(session):
    return await UserGateway.get_telegram_ids(session=session)