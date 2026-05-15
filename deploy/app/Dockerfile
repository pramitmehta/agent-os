FROM ghcr.io/astral-sh/uv:latest AS builder

WORKDIR /app

COPY pyproject.toml ./
COPY src/app/pyproject.toml src/app/
COPY src/runtime/pyproject.toml src/runtime/
COPY src/agents/pyproject.toml src/agents/
COPY src/app/ src/app/
COPY src/runtime/ src/runtime/
COPY src/agents/ src/agents/

RUN uv sync --no-dev --no-install-project -p src/app

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PYTHONPATH=/app/src/app
ENV PATH=/app/.venv/bin:$PATH

EXPOSE 8000

CMD ["python", "-m", "agent_os_app.main"]