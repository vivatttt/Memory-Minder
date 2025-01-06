import asyncio
from backend.app.db.gateway.user import UserGateway
from backend.app.db.connection import get_session

async def test():
    async for session in get_session():
        u_g = UserGateway()
        await u_g.add_user(session=session, id_=12345768, name="Ivan", username="@iivan", is_admin=False)
        u = await u_g.get_by_name(session, name="George")
        print(u)

if __name__ == "__main__":
    asyncio.run(test())