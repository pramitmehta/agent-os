# AGENTS.md

## Tech Stack (from architecture doc)

- ASGI Framework: Litestar
- Validation: msgspec
- Queue/EventBus: Redis
- ORM: SQLAlchemy
- DB: PostgreSQL
- Async Runtime: asyncio
- HTTP Client: httpx
- Package Manager: uv

## Project Structure

```
src/runtime/          # Orchestration engine (consume → dispatch → handlers)
  ├── engine.py       # Runtime core
  ├── dispatcher.py   # Route events to handlers
  ├── registry.py     # Handler registry
  ├── events.py       # Event definitions
  ├── context.py      # Execution context
  └── bus/            # EventBus implementations (base, memory, redis)
docs/
  └── architecture.md # Full architecture reference
```

## Architecture Notes

- Event-driven: all actions flow as events through EventBus → Runtime → Dispatcher → Handlers → Agents → Tools
- Dependency direction: Runtime → Dispatcher → Handlers → Agents → Tools/Repositories
- Agents do NOT know about Runtime, Dispatcher, or EventBus
- API layer should remain thin (only ingress/egress/validation)
- LLM does not control deterministic mechanics (e.g., in the Dungeon Master agent)

## Important Principles

- Good systems are: inspectable, replayable, testable, observable, deterministic where possible
- Avoid: LangChain, CrewAI, AutoGen, framework-heavy abstractions, hidden orchestration logic
- Avoid premature complexity: microservices, distributed orchestration, graph execution engines, autonomous infinite loops

## Current State

This is a greenfield project. `src/runtime/` files are empty stubs. The architecture doc at `docs/architecture.md` is the primary reference for intended design.