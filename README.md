# Agent OS

Event-driven agent orchestration framework.

## Architecture

```
Litestar API Gateway → EventBus (Redis) → Runtime → Dispatcher → Handlers → Agents → Tools/Repositories
```

Layers are strictly separated. The API is thin (only ingress/egress/validation). All actions flow as events. See [docs/architecture.md](docs/architecture.md) for full detail.

## Tech Stack

| Component | Choice |
|-----------|--------|
| ASGI Framework | Litestar |
| Validation | msgspec |
| EventBus | Redis |
| ORM | SQLAlchemy |
| DB | PostgreSQL |
| HTTP Client | httpx |
| Package Manager | uv |

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Redis & PostgreSQL (or use `docker compose up -d redis postgres`)

## Getting Started

```sh
uv sync                          # install all packages
uv run ruff check src/           # lint
uv run mypy src/                 # typecheck
```

Copy `.env.example` to `.env` and configure as needed.

## Running

```sh
uv run agent-os                  # start API service
```

Or with Docker Compose (runs app + runtime + agents + Redis + PostgreSQL):

```sh
docker compose up --build
```

## Project Structure

This is a uv workspace monorepo:

| Package | Directory | Entrypoint |
|---------|-----------|------------|
| `agent-os-runtime` | `src/runtime/` | `agent_os_runtime.engine` |
| `agent-os-app` | `src/app/` | `agent_os_app.main:main` (CLI: `uv run agent-os`) |
| `agent-os-agents` | `src/agents/` | `agent_os_agents.run` |

Shared code lives in `src/shared/` and `src/handlers/`.

## Development

```sh
uv sync                          # sync all workspace packages
uv run ruff check src/           # lint (ruff E,F,I,N,W,UP, line-length=100)
uv run mypy src/                 # typecheck (strict)
uv run pytest                    # run tests
```

To add a dependency to a specific package:

```sh
uv add <package> -p src/agents   # --project alias
```

## Design Principles

- Event-driven: all actions flow as events through the pipeline
- Dependency direction is strictly downward (agents know nothing about runtime/dispatcher/EventBus)
- LLM never controls deterministic mechanics
- Avoid: LangChain, CrewAI, AutoGen, microservices, autonomous infinite loops
- Prefer explicit, inspectable, replayable, testable systems

## License

MIT
