from collections.abc import AsyncGenerator
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from joserfc import jwt
from joserfc.errors import ExpiredTokenError, JoseError
from joserfc.jwk import ECKey
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.services.errors import InvalidAuthorizationTokenError
from src.services.models.user import User
from src.settings import Settings, get_settings

SettingsDependency = Annotated[Settings, Depends(get_settings)]


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession]:
    async_session_local = request.app.state.AsyncSessionLocal
    async with async_session_local() as session:

        yield session


DbSessionDependency = Annotated[AsyncSession, Depends(get_db_session)]
CredentialsDependency = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]


async def get_user(
    settings: SettingsDependency,
    db_session: DbSessionDependency,
    credentials: CredentialsDependency,
) -> User:
    pub_key = ECKey.import_key(settings.jwt_public_key)
    claims_requests = jwt.JWTClaimsRegistry(exp={"essential": True})

    try:
        payload = jwt.decode(credentials.credentials, pub_key).claims
        claims_requests.validate(payload)
        user_id = UUID(payload.get("sub"))

        query = select(User).where(User.id == user_id)
        result = await db_session.execute(query)

        return result.scalar_one()

    except (ExpiredTokenError, JoseError, ValueError) as e:
        raise InvalidAuthorizationTokenError() from e

UserDependency = Annotated[User, Depends(get_user)]
