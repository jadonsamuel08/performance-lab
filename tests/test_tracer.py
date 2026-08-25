from pathlib import Path

from performance_lab.events import EventType
from performance_lab.tracer import Tracer


def test_tracer_captures_execution_events():
    target_file = str(Path(__file__).resolve())
    tracer = Tracer(target_file)

    def example():
        value = 42
        return value

    tracer.start()

    try:
        example()
    finally:
        tracer.stop()

    assert tracer.events

    event_types = {event.event_type for event in tracer.events}

    assert EventType.FUNCTION_CALL in event_types
    assert EventType.LINE_EXECUTION in event_types
    assert EventType.FUNCTION_RETURN in event_types


def test_tracer_captures_local_variables():
    target_file = str(Path(__file__).resolve())
    tracer = Tracer(target_file)

    def example():
        value = 42
        message = "hello"
        return message

    tracer.start()

    try:
        example()
    finally:
        tracer.stop()

    line_events = [
        event
        for event in tracer.events
        if event.event_type == EventType.LINE_EXECUTION
        and event.function == "example"
    ]

    assert line_events

    captured_locals = [
        event.data["locals"]
        for event in line_events
    ]

    assert any(locals_.get("value") == 42 for locals_ in captured_locals)
    assert any(locals_.get("message") == "hello" for locals_ in captured_locals)