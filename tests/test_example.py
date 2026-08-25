from performance_lab.events import EventType
from performance_lab.recorder import Recorder
from performance_lab.runner import Runner


def test_example_program():
    runner = Runner("examples/example.py")
    result = runner.run()

    assert result.process.returncode == 0
    assert "Hello, Jadon!" in result.process.stdout
    assert result.events


def test_runner_captures_execution_events():
    runner = Runner("examples/example.py")
    result = runner.run()

    event_types = {event.event_type for event in result.events}

    assert EventType.FUNCTION_CALL in event_types
    assert EventType.LINE_EXECUTION in event_types
    assert EventType.FUNCTION_RETURN in event_types


def test_recorder_steps_through_events():
    runner = Runner("examples/example.py")
    result = runner.run()

    recorder = Recorder(result.events)

    assert recorder.current is None
    assert recorder.started is False

    first_event = recorder.step_forward()

    assert first_event is not None
    assert recorder.current == first_event
    assert recorder.started is True


def test_recorder_can_step_back_and_reset():
    runner = Runner("examples/example.py")
    result = runner.run()

    recorder = Recorder(result.events)

    first_event = recorder.step_forward()
    second_event = recorder.step_forward()

    assert first_event is not None
    assert second_event is not None
    assert recorder.current == second_event

    previous_event = recorder.step_back()

    assert previous_event == first_event
    assert recorder.current == first_event

    recorder.reset()

    assert recorder.current is None
    assert recorder.started is False

def test_recorder_tracks_program_state():
    runner = Runner("examples/example.py")
    result = runner.run()

    recorder = Recorder(result.events)

    while not recorder.finished:
        recorder.step_forward()

    state = recorder.state.snapshot()

    assert state["name"] == "Jadon"
    assert state["result"] == "Hello, Jadon!"


def test_recorder_rebuilds_state_when_stepping_back():
    runner = Runner("examples/example.py")
    result = runner.run()

    recorder = Recorder(result.events)

    while not recorder.finished:
        recorder.step_forward()

    final_state = recorder.state.snapshot()

    recorder.step_back()
    recorder.step_back()

    previous_state = recorder.state.snapshot()

    assert final_state != previous_state
    assert final_state["result"] == "Hello, Jadon!"
    assert "result" not in previous_state