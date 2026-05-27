

from __future__ import annotations 

from src.shared.events.base import BaseEvent
from src.shared.events.types import E
import uuid

def create_root_event(workflow_id: uuid.UUID, trace_id: uuid.UUID, source: str, event_type: str) -> E:
    event_id = uuid.uuid4()
    timestamp = time.time()
    return BaseEvent(event_id=event_id, workflow_id=workflow_id, trace_id=trace_id, source=source, parent_event_id=None, event_type=event_type,  timestamp=timestamp)


def duplicate_event(event: E) -> E:
    event_id = uuid.uuid4()
    timestamp = time.time()
    return BaseEvent(event_id=event_id, workflow_id=event.workflow_id, trace_id=event.trace_id, source=event.source, parent_event_id=event.event_id, event_type=event.event_type,  timestamp=timestamp)


def create_child_event(parent: E, child_event_type: str) -> E:
    return duplicate_event(parent)