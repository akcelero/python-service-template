from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.requests import Request

from src.api.router import router_api
from src.lifespan import lifespan
from src.services.errors import InvalidAuthorizationTokenError

app = FastAPI(
    title="Python service API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router_api)


@app.exception_handler(InvalidAuthorizationTokenError)
def handle_invalid_authorization_token(_: Request, exception: InvalidAuthorizationTokenError) -> None:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authorization token",
    ) from exception
