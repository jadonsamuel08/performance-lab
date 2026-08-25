from performance_lab.events import EventType, ExecutionEvent
from performance_lab.timeline import Timeline

from performance_lab.recorder import Recorder
from performance_lab.runner import Runner


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


def test_timeline_navigation():
    timeline = Timeline(make_events())

    timeline.step_forward()

    assert timeline.current_index == 0
    assert timeline.total_events == 3
    assert timeline.previous_event is None
    assert timeline.next_event is not None


def test_timeline_progress():
    timeline = Timeline(make_events())

    assert timeline.progress == 0.0

    timeline.step_forward()
    assert timeline.progress == 1 / 3

    timeline.step_forward()
    assert timeline.progress == 2 / 3

    timeline.step_forward()
    assert timeline.progress == 1.0

def test_recorder_jump_to_event():
    runner = Runner("examples/example.py")
    result = runner.run()

    recorder = Recorder(result.events)

    event = recorder.jump_to(3)

    assert event is not None
    assert recorder.position == 3
    assert recorder.current == event


def test_recorder_jump_rebuilds_state():
    runner = Runner("examples/example.py")
    result = runner.run()

    recorder = Recorder(result.events)

    recorder.jump_to(8)

    state = recorder.state.snapshot()

    assert state["name"] == "Jadon"
    assert state["result"] == "Hello, Jadon!"


def test_recorder_jump_clamps_to_start():
    runner = Runner("examples/example.py")
    result = runner.run()

    recorder = Recorder(result.events)

    event = recorder.jump_to(-100)

    assert event is not None
    assert recorder.position == 0


def test_recorder_jump_clamps_to_end():
    runner = Runner("examples/example.py")
    result = runner.run()

    recorder = Recorder(result.events)

    event = recorder.jump_to(10000)

    assert event is not None
    assert recorder.position == len(result.events) - 1
    assert recorder.finished


def test_recorder_reports_progress():
    runner = Runner("examples/example.py")
    result = runner.run()

    recorder = Recorder(result.events)

    assert recorder.progress == 0.0

    recorder.jump_to(4)

    assert recorder.progress == 5 / len(result.events)