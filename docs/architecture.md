# architecture.md

# Agent Runtime Architecture

## Vision

This project is not a chatbot.

It is an event-driven agent runtime platform designed to support:

- research agents
- educational agents
- multiplayer game agents
- orchestration workflows
- long-running intelligent systems

The architecture intentionally avoids:

- LangChain
- CrewAI
- AutoGen
- framework-heavy abstractions
- hidden orchestration logic

The goal is to build explicit and inspectable primitives.

---

# Core Architectural Philosophy

## Separation Of Concerns

Each layer owns a single responsibility.

| Layer | Responsibility |
|---|---|
| API Layer | external communication |
| EventBus | transport events |
| Runtime | orchestrate execution |
| Dispatcher | route events |
| Handler Registry | map events to handlers |
| Handlers | execute workflows |
| Agents | reasoning and planning |
| Tools | external capabilities |
| Repositories | persistence |
| Memory | retrieval and long-term state |

---

# High-Level Architecture

```text
                ┌────────────────────┐
                │      Litestar      │
                │    API Gateway     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │      EventBus      │
                │       Redis        │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │      Runtime       │
                │  Orchestration     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │     Dispatcher     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │  Handler Registry  │
                └─────────┬──────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
    ┌──────────────┐           ┌──────────────┐
    │ Research     │           │ Dungeon      │
    │ Handlers     │           │ Handlers     │
    └──────┬───────┘           └──────┬───────┘
           │                           │
           ▼                           ▼
    ┌──────────────┐           ┌──────────────┐
    │ Research     │           │ Dungeon      │
    │ Agent        │           │ Agent        │
    └──────┬───────┘           └──────┬───────┘
           │                           │
           ▼                           ▼
    ┌──────────────┐           ┌──────────────┐
    │ Tools        │           │ Tools        │
    └──────────────┘           └──────────────┘
```

---

# Runtime Responsibilities

The runtime is the orchestration engine.

It is NOT:

- the agent
- the API layer
- the event transport
- the reasoning engine

It coordinates execution.

## Runtime Owns

- consuming events
- dispatching events
- orchestration lifecycle
- async task scheduling
- retries
- cancellation
- tracing
- concurrency coordination
- execution boundaries

## Runtime Does NOT Own

- HTTP logic
- reasoning
- tool implementation
- persistence details

---

# Event-Driven Architecture

The system is event-first.

All meaningful system actions become events.

## Example Events

```text
UserMessageEvent
ToolCallRequestedEvent
ToolCallCompletedEvent
AgentResponseEvent
MemoryStoredEvent
TaskFailedEvent
```

Events are immutable.

---

# Core Event Flow

```text
HTTP Request
    ↓
API Route
    ↓
Create Event
    ↓
EventBus.publish()
    ↓
Runtime.consume()
    ↓
Dispatcher.dispatch()
    ↓
Handler.handle()
    ↓
Agent.run()
    ↓
Tool Calls
    ↓
New Events Published
```

---

# Dependency Direction

Dependencies should only flow downward.

```text
Runtime
    ↓
Dispatcher
    ↓
Handlers
    ↓
Agents
    ↓
Tools / Repositories
```

Agents should never know:

- Runtime
- Dispatcher
- EventBus internals
- API framework

Tools should never know:

- Agents
- Runtime
- HTTP

---

# API Layer

The API layer is only responsible for:

- ingress
- egress
- validation
- authentication
- request translation

The API layer should remain thin.

## Example

```python
@post("/chat")
async def chat(
    data: ChatRequest,
    bus: EventBus,
):
    event = UserMessageEvent(...)

    await bus.publish(event)

    return {"status": "accepted"}
```

The route does not orchestrate the agent.

---

# EventBus

The EventBus only transports events.

It does not:

- route events
- orchestrate workflows
- know about handlers
- know about agents

## Recommended Interface

```python
from typing import Protocol


class EventBus(Protocol):

    async def publish(self, event) -> None:
        ...

    async def consume(self):
        ...
```

---

# Dispatcher

The dispatcher routes events to handlers.

The dispatcher should remain thin.

## Responsibilities

- resolve handler
- invoke handler

## Non-Responsibilities

- orchestration
- reasoning
- persistence

---

# Handler Registry

The handler registry enables pluggable handlers.

## Example

```python
registry.register(UserMessageHandler(...))
```

Later this can support:

- multiple handlers per event
- plugins
- dynamic loading
- replay systems

---

# Handlers

Handlers coordinate workflows.

Handlers may:

- invoke agents
- invoke repositories
- publish events
- coordinate state transitions

Handlers should NOT:

- contain transport logic
- contain framework logic
- contain giant reasoning prompts

---

# Agents

Agents are reasoning units.

Agents should focus on:

- reasoning
- planning
- tool selection
- memory retrieval
- generating responses

Agents should NOT:

- manage queues
- manage orchestration
- own retries
- manage worker lifecycle

---

# Tools

Tools are atomic capabilities.

Examples:

- web search
- paper retrieval
- PDF parsing
- telegram messaging
- dice rolling
- file reading

Tools should remain deterministic whenever possible.

---

# Repositories

Repositories abstract persistence.

Examples:

- SessionRepository
- MemoryRepository
- WikiRepository
- CampaignRepository

Avoid giant generic repositories.

---

# Recommended Tech Stack

| Component | Choice |
|---|---|
| ASGI Framework | Litestar |
| Validation | msgspec |
| Queue/EventBus | Redis |
| ORM | SQLAlchemy |
| DB | PostgreSQL |
| Async Runtime | asyncio |
| HTTP Client | httpx |

---

# Recommended Folder Structure

```text
project/
├── api/
│   ├── routes/
│   └── schemas/
│
├── runtime/
│   ├── engine.py
│   ├── dispatcher.py
│   ├── registry.py
│   ├── events.py
│   ├── context.py
│   ├── bus/
│   │   ├── base.py
│   │   ├── redis.py
│   │   └── memory.py
│   │
│   └── handlers/
│
├── agents/
│   ├── research/
│   └── dungeon_master/
│
├── tools/
│
├── repositories/
│
├── memory/
│
├── integrations/
│   ├── telegram/
│   ├── arxiv/
│   └── semantic_scholar/
│
└── storage/
```

---

# Research Agent Vision

The research agent will:

```text
Search papers
    ↓
Retrieve papers
    ↓
Extract concepts
    ↓
Generate wiki graph
    ↓
Teach concepts
    ↓
Evaluate understanding
    ↓
Suggest deeper reading
```

This agent emphasizes:

- RAG
- semantic memory
- tutoring workflows
- adaptive learning
- knowledge graphs

---

# Dungeon Master Agent Vision

The dungeon master agent will:

```text
Manage multiplayer sessions
    ↓
Track campaign state
    ↓
Handle combat
    ↓
Generate narrative
    ↓
Coordinate player actions
```

Important distinction:

| System | Responsibility |
|---|---|
| Rule Engine | deterministic logic |
| LLM | narration and creativity |

The LLM should not control deterministic mechanics.

---

# Important Engineering Principles

## Keep Boundaries Sharp

Avoid mixing:

- orchestration
- reasoning
- transport
- persistence

---

## Prioritize Observability

Log:

```text
EVENT_RECEIVED
EVENT_DISPATCHED
HANDLER_STARTED
HANDLER_COMPLETED
AGENT_STEP
TOOL_CALLED
TOOL_COMPLETED
```

---

## Avoid Premature Complexity

Avoid initially:

- microservices
- distributed orchestration
- graph execution engines
- autonomous infinite loops
- overcomplicated planners

---

## Prefer Explicit Systems

Good systems are:

- inspectable
- replayable
- testable
- observable
- deterministic where possible

---

# Future Evolution

This architecture can later support:

- multiple runtimes
- autonomous workflows
- scheduled agents
- distributed workers
- replay systems
- observability dashboards
- multi-agent coordination
- event sourcing
- DAG execution

without rewriting core foundations.

---
