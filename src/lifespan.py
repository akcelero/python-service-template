import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from aiohttp import ClientSession, ClientTimeout
from fastapi import FastAPI

from src.db import get_engine, get_async_session
from src.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    settings = get_settings()

    engine = get_engine(settings)
    async_session = get_async_session(engine)

    logging.getLogger("uvicorn.access").disabled = True
    logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(message)s")

    timeout = ClientTimeout(total=settings.request_timeout)

    async with ClientSession(timeout=timeout) as aiohttp_session:
        app.state.aiohttp_session = aiohttp_session
        app.state.engine = engine
        app.state.AsyncSessionLocal = async_session

        yield
