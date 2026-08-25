from performance_lab.events import EventType
from performance_lab.runner import Runner


def test_example_program():
    runner = Runner("examples/example.py")
    events = runner.run()

    assert events

    event_types = [event.event_type for event in events]

    assert EventType.FUNCTION_CALL in event_types
    assert EventType.LINE_EXECUTION in event_types
    assert EventType.FUNCTION_RETURN in event_types

    greet_calls = [
        event
        for event in events
        if event.event_type == EventType.FUNCTION_CALL
        and event.function == "greet"
    ]

    assert len(greet_calls) == 1

    return_events = [
        event
        for event in events
        if event.event_type == EventType.FUNCTION_RETURN
        and event.function == "greet"
    ]

    assert len(return_events) == 1
    assert return_events[0].data["return_value"] == "Hello, Jadon!"