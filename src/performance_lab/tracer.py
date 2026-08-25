import sys
import time
from collections.abc import Callable
from types import FrameType
from typing import Any

from performance_lab.events import EventType, ExecutionEvent


class Tracer:
    def __init__(self, target_file: str) -> None:
        self.target_file = target_file
        self.events: list[ExecutionEvent] = []

    def snapshot_locals(self, frame: FrameType) -> dict[str, Any]:
        ignored_names = {
            "__name__",
            "__file__",
            "__builtins__",
            "__package__",
            "__loader__",
            "__spec__",
            "__cached__",
        }

        return {
            name: value
            for name, value in frame.f_locals.items()
            if name not in ignored_names
        }

    def trace(
        self,
        frame: FrameType,
        event: str,
        arg: Any,
    ) -> Callable[..., Any] | None:
        if frame.f_code.co_filename != self.target_file:
            return self.trace

        if event == "line":
            self.events.append(
                ExecutionEvent(
                    event_type=EventType.LINE_EXECUTION,
                    timestamp=time.perf_counter(),
                    file=frame.f_code.co_filename,
                    line=frame.f_lineno,
                    function=frame.f_code.co_name,
                    data={
                        "locals": self.snapshot_locals(frame),
                    },
                )
            )

        elif event == "call":
            self.events.append(
                ExecutionEvent(
                    event_type=EventType.FUNCTION_CALL,
                    timestamp=time.perf_counter(),
                    file=frame.f_code.co_filename,
                    line=frame.f_lineno,
                    function=frame.f_code.co_name,
                    data={},
                )
            )

        elif event == "return":
            self.events.append(
                ExecutionEvent(
                    event_type=EventType.FUNCTION_RETURN,
                    timestamp=time.perf_counter(),
                    file=frame.f_code.co_filename,
                    line=frame.f_lineno,
                    function=frame.f_code.co_name,
                    data={
                        "return_value": arg,
                    },
                )
            )

        elif event == "exception":
            exception_type, exception_value, _ = arg

            self.events.append(
                ExecutionEvent(
                    event_type=EventType.EXCEPTION,
                    timestamp=time.perf_counter(),
                    file=frame.f_code.co_filename,
                    line=frame.f_lineno,
                    function=frame.f_code.co_name,
                    data={
                        "exception_type": exception_type.__name__,
                        "message": str(exception_value),
                    },
                )
            )

        return self.trace

    def start(self) -> None:
        sys.settrace(self.trace)

    def stop(self) -> None:
        sys.settrace(None)