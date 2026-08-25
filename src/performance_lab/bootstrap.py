import json
import sys
from pathlib import Path

from performance_lab.tracer import Tracer


def serialize_value(value):
    try:
        json.dumps(value)
        return value
    except TypeError:
        return repr(value)


def serialize_event(event):
    return {
        "event_type": event.event_type.value,
        "timestamp": event.timestamp,
        "file": event.file,
        "line": event.line,
        "function": event.function,
        "data": {
            key: serialize_value(value)
            for key, value in event.data.items()
        },
    }


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python -m performance_lab.bootstrap <target_file>",
            file=sys.stderr,
        )
        sys.exit(1)

    target_file = Path(sys.argv[1]).resolve()

    tracer = Tracer(str(target_file))

    tracer.start()

    try:
        source = target_file.read_text(encoding="utf-8")
        code = compile(source, str(target_file), "exec")

        namespace = {
            "__name__": "__main__",
            "__file__": str(target_file),
        }

        exec(code, namespace)
    finally:
        tracer.stop()

    for event in tracer.events:
        print(json.dumps(serialize_event(event)), file=sys.stderr)


if __name__ == "__main__":
    main()