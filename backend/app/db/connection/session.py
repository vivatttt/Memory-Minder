from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from backend.config import get_settings


class SessionManager:
    
    def __init__(self) -> None:
        self.refresh()


    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def refresh(self) -> None:
        self.engine = create_async_engine(
            get_settings().database_uri,
            echo=get_settings().echo_enabled,
            future=True,
            connect_args={"server_settings": {"jit": "off"}},
        )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session


__all__ = [
    "get_session",
]
