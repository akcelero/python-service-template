from datetime import UTC, datetime, timedelta
from uuid import UUID

from pydantic import BaseModel, Field


class JwtClaims(BaseModel):
    sub: UUID
    exp: int = Field(default_factory=lambda: int((datetime.now(UTC) + timedelta(days=1)).timestamp()))
    iat: int = Field(default_factory=lambda: int(datetime.now(UTC).timestamp()))
