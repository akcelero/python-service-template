FROM python:3.13.6-alpine3.22 AS base

ENTRYPOINT ["tini", "--"]

WORKDIR /app

ENV APP_PORT=8000 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    PATH="/app/.venv/bin:$PATH"

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup && \
    apk update && \
    apk add --no-cache bash curl tini

COPY --from=ghcr.io/astral-sh/uv:0.8.3 /uv /bin/uv
COPY pyproject.toml uv.lock ./


FROM base AS remote

RUN uv sync --frozen --no-dev

COPY src ./src

USER appuser
CMD uvicorn src.app:app --host 0.0.0.0 --port ${APP_PORT} --workers 4


FROM base AS local

RUN uv sync

COPY src ./src

USER appuser
CMD uvicorn src.app:app --host 0.0.0.0 --port ${APP_PORT} --reload --reload-dir src
