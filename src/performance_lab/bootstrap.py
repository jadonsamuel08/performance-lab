import json
import runpy
import sys
from pathlib import Path
from typing import Any

from performance_lab.events import ExecutionEvent
from performance_lab.tracer import Tracer


def serialize_value(value: Any) -> Any:
    """Convert a Python value into something JSON can serialize."""

    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, dict):
        return {
            str(key): serialize_value(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [serialize_value(item) for item in value]

    if isinstance(value, (set, frozenset)):
        return [serialize_value(item) for item in value]

    return str(value)


def serialize_event(event: ExecutionEvent) -> dict[str, Any]:
    """Convert an ExecutionEvent into a JSON-serializable dictionary."""

    return {
        "event_type": event.event_type.value,
        "timestamp": event.timestamp,
        "file": event.file,
        "line": event.line,
        "function": event.function,
        "data": serialize_value(event.data),
    }


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python -m performance_lab.bootstrap <python-file>",
            file=sys.stderr,
        )
        raise SystemExit(2)

    target_file = Path(sys.argv[1]).resolve()

    if not target_file.exists():
        print(f"File not found: {target_file}", file=sys.stderr)
        raise SystemExit(1)

    tracer = Tracer(str(target_file))

    tracer.start()

    try:
        runpy.run_path(
            str(target_file),
            run_name="__main__",
        )
    finally:
        tracer.stop()

    for event in tracer.events:
        print(
            json.dumps(serialize_event(event)),
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()