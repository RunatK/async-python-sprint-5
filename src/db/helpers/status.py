from core.config import PG_DSN
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


async def status() -> str:
    try:
        engine = create_async_engine(PG_DSN, echo=True, future=True)
        async with AsyncSession(engine):
            return "Database is working"
    except Exception as ex:
        return f"Database is not working: {ex}"
