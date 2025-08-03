from enum import StrEnum

from pydantic import BaseModel
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE


class LivenessResponse(BaseModel):
    status: str = "alive"


class ConnectionStatus(StrEnum):
    OK = "OK"
    UNAVAILABLE = "UNAVAILABLE"


class HealthCheckResponse(BaseModel):
    third_party: ConnectionStatus

    def get_http_response_code(self) -> int:
        return HTTP_200_OK if self.third_party == ConnectionStatus.OK else HTTP_503_SERVICE_UNAVAILABLE
