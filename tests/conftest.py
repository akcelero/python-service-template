import secrets
from collections.abc import AsyncGenerator
from uuid import uuid4

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from joserfc import jwt
from joserfc.jwk import ECKey
from pytest_mock import MockFixture
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine

from src.app import app
from src.services.models.base import Base
from src.services.models.jwt_claims import JwtClaims
from src.services.models.user import User
from tests.settings import TestSettings


@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_settings(session_mocker: MockFixture) -> TestSettings:
    settings = TestSettings()
    session_mocker.patch(
        "src.settings.Settings",
        return_value=settings,
    )
    return settings


@pytest_asyncio.fixture(scope="session")
async def test_engine(test_settings: TestSettings, session_mocker: MockFixture) -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(test_settings.sqlite_dsn.encoded_string(), echo=False)

    session_mocker.patch(
        "src.lifespan.get_engine",
        return_value=engine,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession]:
    connection = await test_engine.connect()
    transaction = await connection.begin()

    test_session_local = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    try:
        async with test_session_local() as session:
            yield session

    finally:
        if transaction.is_active:
            await transaction.rollback()

        await connection.close()


@pytest_asyncio.fixture
async def user(db_session: AsyncSession) -> User:
    user = User(
        id=uuid4(),
        email="some@email.com",
        hashed_password=secrets.token_hex(),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.flush()

    return user


@pytest_asyncio.fixture
async def jwt_token(test_settings: TestSettings, user: User) -> str:
    claims = JwtClaims(sub=user.id)
    key = ECKey.import_key(test_settings.jwt_private_key)

    return jwt.encode(
        header={"alg": "ES256"},
        claims=claims.model_dump(mode="json"),
        key=key,
    )


@pytest_asyncio.fixture
async def test_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    transport = ASGITransport(app=app)
    base_url = "http://test.mock"

    async with (
        AsyncClient(transport=transport, base_url=base_url) as async_client,
        app.router.lifespan_context(app),
    ):
        yield async_client
