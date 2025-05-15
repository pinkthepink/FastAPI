from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost/client_management"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with AsyncSessionLocal() as session:
        yield session
        await session.close()