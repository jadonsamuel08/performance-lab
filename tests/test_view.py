from performance_lab.api import run
from performance_lab.view import ExecutionView


def test_view_starts_before_execution():
    execution = run("examples/example.py")

    view = ExecutionView.from_execution(execution)

    assert view.event is None
    assert view.position == -1
    assert view.total_events == len(execution.events)
    assert view.progress == 0.0


def test_view_updates_after_stepping():
    execution = run("examples/example.py")

    execution.recorder.step_forward()

    view = ExecutionView.from_execution(execution)

    assert view.event is not None
    assert view.position == 0
    assert view.file == "examples/example.py"
    assert view.function == "<module>"
    assert view.progress > 0


def test_view_exposes_program_state():
    execution = run("examples/example.py")

    while not execution.recorder.finished:
        execution.recorder.step_forward()

    view = ExecutionView.from_execution(execution)

    assert view.state["name"] == "Jadon"
    assert view.state["result"] == "Hello, Jadon!"


def test_view_tracks_call_stack():
    execution = run("examples/example.py")

    for _ in range(5):
        execution.recorder.step_forward()

    view = ExecutionView.from_execution(execution)

    assert "greet" in view.call_stack