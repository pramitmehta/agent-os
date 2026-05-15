FROM ghcr.io/astral-sh/uv:latest AS builder

WORKDIR /app

COPY pyproject.toml ./
COPY src/agents/pyproject.toml src/agents/
COPY src/runtime/pyproject.toml src/runtime/
COPY src/agents/ src/agents/
COPY src/runtime/ src/runtime/

RUN uv sync --no-dev --no-install-project -p src/agents

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PYTHONPATH=/app/src/agents
ENV PATH=/app/.venv/bin:$PATH

CMD ["python", "-m", "agent_os_agents.run"]