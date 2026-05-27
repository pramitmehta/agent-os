# AGENTS.md

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
| Lint | ruff (E,F,I,N,W,UP, line-length=100) |
| Typecheck | mypy --strict |

Python 3.12+, MIT license.

## Monorepo Structure (uv workspace)

| Package | Dir | Entrypoint |
|---------|-----|------------|
| `agent-os-runtime` | `src/runtime/` | `agent_os_runtime.engine` (deploy/runtime/Dockerfile) |
| `agent-os-app` | `src/app/` | `agent_os_app.main:main` (CLI: `uv run agent-os`) |
| `agent-os-agents` | `src/agents/` | `agent_os_agents.run` (deploy/agents/Dockerfile) |

`src/handlers/`, `src/shared/` — not packages; common code in `src/shared/{exceptions,integrations,logging,serialization,telemetry}/`.

Deploy images in `deploy/{app,runtime,agents}/Dockerfile`; `docker-compose.yml` at root runs all 3 services plus Redis + PostgreSQL.

## Architecture (see docs/architecture.md for full detail)

```
EventBus → Runtime → Dispatcher → HandlerRegistry → Handlers → Agents → Tools/Repositories
```

- Event-driven: all actions flow as events through the pipeline above
- Dependency direction is strictly downward (agents know nothing about runtime/dispatcher/EventBus)
- API layer is thin: only ingress, egress, validation (routes publish events, never orchestrate)
- LLM never controls deterministic mechanics (e.g., dungeon master rule engine vs. narration)
- Avoid: LangChain, CrewAI, AutoGen, microservices, graph executors, autonomous infinite loops

## Current State

Greenfield — all `.py` files are empty stubs (except `src/runtime/__init__.py` which forward-declares imports). No tests exist yet.

## Commands

```sh
uv sync                              # install all workspace packages + dev-deps
uv run ruff check src/               # lint
uv run mypy src/                     # typecheck (strict)
uv run pytest                        # run tests (none exist yet)
uv run agent-os                      # start app service
uv sync -p src/app                   # sync only app package (for deploy)
```

Env vars documented in `.env.example`.
