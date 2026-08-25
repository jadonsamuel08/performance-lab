from performance_lab.events import EventType, ExecutionEvent
from performance_lab.timeline import Timeline


def make_events() -> list[ExecutionEvent]:
    return [
        ExecutionEvent(
            event_type=EventType.FUNCTION_CALL,
            timestamp=1.0,
            file="example.py",
            line=1,
            function="example",
            data={},
        ),
        ExecutionEvent(
            event_type=EventType.LINE_EXECUTION,
            timestamp=2.0,
            file="example.py",
            line=2,
            function="example",
            data={"locals": {"value": 42}},
        ),
        ExecutionEvent(
            event_type=EventType.FUNCTION_RETURN,
            timestamp=3.0,
            file="example.py",
            line=3,
            function="example",
            data={"return_value": 42},
        ),
    ]


def test_timeline_starts_before_first_event():
    timeline = Timeline(make_events())

    assert timeline.current is None
    assert not timeline.started
    assert not timeline.finished


def test_timeline_steps_forward():
    timeline = Timeline(make_events())

    event = timeline.step_forward()

    assert event is not None
    assert event.event_type == EventType.FUNCTION_CALL
    assert timeline.started


def test_timeline_steps_backward():
    timeline = Timeline(make_events())

    timeline.step_forward()
    timeline.step_forward()

    event = timeline.step_back()

    assert event is not None
    assert event.event_type == EventType.FUNCTION_CALL


def test_timeline_detects_boundaries():
    timeline = Timeline(make_events())

    assert not timeline.has_previous
    assert timeline.has_next

    timeline.step_forward()
    timeline.step_forward()
    timeline.step_forward()

    assert timeline.finished
    assert not timeline.has_next
    assert timeline.has_previous


def test_timeline_reset():
    timeline = Timeline(make_events())

    timeline.step_forward()
    timeline.step_forward()

    timeline.reset()

    assert timeline.position == -1
    assert timeline.current is None
    assert not timeline.started


def test_timeline_length():
    timeline = Timeline(make_events())

    assert len(timeline) == 3