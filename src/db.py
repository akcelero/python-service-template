from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.settings import Settings


def get_engine(settings: Settings) -> AsyncEngine:
    postgres_dsn = settings.postgres_dsn.encoded_string()
    return create_async_engine(postgres_dsn)


def get_async_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
