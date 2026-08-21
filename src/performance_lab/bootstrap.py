import json
import sys

from performance_lab.events import ExecutionEvent
from performance_lab.tracer import Tracer


def serialize_value(value):
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, (list, tuple)):
        return [serialize_value(item) for item in value]

    if isinstance(value, dict):
        return {
            str(key): serialize_value(item)
            for key, item in value.items()
        }

    return repr(value)


def serialize_event(event: ExecutionEvent) -> dict:
    return {
        "event_type": event.event_type.value,
        "timestamp": event.timestamp,
        "file": event.file,
        "line": event.line,
        "function": event.function,
        "data": serialize_value(event.data),
    }


def main() -> None:
    target_file = sys.argv[1]

    tracer = Tracer(target_file)
    tracer.start()

    try:
        with open(target_file, "r", encoding="utf-8") as file:
            source = file.read()

        namespace = {
            "__name__": "__main__",
            "__file__": target_file,
            "__builtins__": __builtins__,
        }

        exec(
            compile(
                source,
                target_file,
                "exec",
            ),
            namespace,
            namespace,
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