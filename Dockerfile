FROM ghcr.io/astral-sh/uv:latest AS builder

WORKDIR /app

COPY pyproject.toml ./
COPY src/ ./src/

RUN uv sync --no-dev --no-install-project

FROM ghcr.io/astral-sh/uv:latest AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv

ENV PYTHONPATH=/app/src/app
ENV PATH=/app/.venv/bin:$PATH

EXPOSE 8000

CMD ["uv", "run", "agent-os"]