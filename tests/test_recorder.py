from performance_lab.api import run
from performance_lab.recorder import Recorder


def test_recorder_starts_before_execution():
    execution = run("examples/example.py")
    recorder = Recorder(execution.events)

    assert recorder.position == -1
    assert recorder.current is None
    assert not recorder.started


def test_recorder_previous_state_is_empty_before_execution():
    execution = run("examples/example.py")
    recorder = Recorder(execution.events)

    assert recorder.previous_state == {}


def test_recorder_previous_state_excludes_current_event():
    execution = run("examples/example.py")
    recorder = Recorder(execution.events)

    recorder.step_forward()

    assert recorder.previous_state == {}


def test_recorder_previous_state_matches_state_before_current_event():
    execution = run("examples/example.py")
    recorder = Recorder(execution.events)

    recorder.jump_to(5)

    state_before_event = recorder.previous_state

    recorder.jump_to(4)

    assert recorder.state.snapshot() == state_before_event


def test_recorder_previous_state_updates_after_navigation():
    execution = run("examples/example.py")
    recorder = Recorder(execution.events)

    recorder.jump_to(5)

    state_at_five = recorder.state.snapshot()

    recorder.jump_to(6)

    assert recorder.previous_state == state_at_five


def test_recorder_previous_state_resets():
    execution = run("examples/example.py")
    recorder = Recorder(execution.events)

    recorder.jump_to(5)
    recorder.reset()

    assert recorder.position == -1
    assert recorder.previous_state == {}