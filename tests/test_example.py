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