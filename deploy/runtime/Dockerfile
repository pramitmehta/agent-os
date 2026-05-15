FROM ghcr.io/astral-sh/uv:latest AS builder

WORKDIR /app

COPY pyproject.toml ./
COPY src/runtime/pyproject.toml src/runtime/

RUN uv sync --no-dev --no-install-project -p src/runtime

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PYTHONPATH=/app/src/runtime
ENV PATH=/app/.venv/bin:$PATH

CMD ["python", "-m", "agent_os_runtime.engine"]