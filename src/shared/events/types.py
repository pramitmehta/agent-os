
from __future__ import annotations

from typing import TypeVar

from src.shared.events.base import BaseEvent


E = TypeVar("E", bound=BaseEvent)