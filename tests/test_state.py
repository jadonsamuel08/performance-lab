from performance_lab.events import EventType, ExecutionEvent
from performance_lab.state import ProgramState


def test_state_starts_empty():
    state = ProgramState()

    assert state.snapshot() == {}


def test_state_captures_line_execution_locals():
    state = ProgramState()

    event = ExecutionEvent(
        event_type=EventType.LINE_EXECUTION,
        timestamp=1.0,
        file="example.py",
        line=2,
        function="example",
        data={
            "locals": {
                "value": 42,
                "message": "hello",
            }
        },
    )

    state.apply(event)

    assert state.snapshot() == {
        "value": 42,
        "message": "hello",
    }


def test_state_ignores_non_line_events():
    state = ProgramState()

    event = ExecutionEvent(
        event_type=EventType.FUNCTION_CALL,
        timestamp=1.0,
        file="example.py",
        line=1,
        function="example",
        data={},
    )

    state.apply(event)

    assert state.snapshot() == {}


def test_state_replaces_previous_snapshot():
    state = ProgramState()

    first_event = ExecutionEvent(
        event_type=EventType.LINE_EXECUTION,
        timestamp=1.0,
        file="example.py",
        line=1,
        function="example",
        data={
            "locals": {
                "value": 42,
            }
        },
    )

    second_event = ExecutionEvent(
        event_type=EventType.LINE_EXECUTION,
        timestamp=2.0,
        file="example.py",
        line=2,
        function="example",
        data={
            "locals": {
                "value": 43,
                "message": "updated",
            }
        },
    )

    state.apply(first_event)
    state.apply(second_event)

    assert state.snapshot() == {
        "value": 43,
        "message": "updated",
    }