FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src/ src/

RUN uv sync --no-dev --locked

FROM python:3.13-slim-bookworm

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY src/ src/

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "vehicle_mcp"]
