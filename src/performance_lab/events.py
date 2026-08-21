from dataclasses import dataclass
from enum import Enum
from typing import Any


class EventType(Enum):
    LINE_EXECUTION = "line_execution"
    FUNCTION_CALL = "function_call"
    FUNCTION_RETURN = "function_return"
    EXCEPTION = "exception"


@dataclass
class ExecutionEvent:
    event_type: EventType
    timestamp: float
    file: str
    line: int
    function: str
    data: dict[str, Any]