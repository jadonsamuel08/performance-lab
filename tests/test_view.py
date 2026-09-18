from performance_lab.api import run
from performance_lab.view import ExecutionView


def test_view_starts_before_execution():
    execution = run("examples/example.py")

    view = ExecutionView.from_execution(execution)

    assert view.event is None
    assert view.position == -1
    assert view.total_events == len(execution.events)
    assert view.progress == 0.0
    assert view.source == []
    assert view.state_changes.changes == []


def test_view_updates_after_stepping():
    execution = run("examples/example.py")

    execution.recorder.step_forward()

    view = ExecutionView.from_execution(execution)

    assert view.event is not None
    assert view.position == 0
    assert view.file.endswith("examples/example.py")
    assert view.function == "<module>"
    assert view.progress > 0


def test_view_exposes_program_state():
    execution = run("examples/example.py")

    while not execution.recorder.finished:
        execution.recorder.step_forward()

    view = ExecutionView.from_execution(execution)

    assert view.state.get("name") == "Jadon"
    assert view.state.get("result") == "Hello, Jadon!"


def test_view_exposes_state_changes():
    execution = run("examples/example.py")

    execution.recorder.jump_to(7)

    view = ExecutionView.from_execution(execution)

    assert view.state_changes.changes


def test_view_state_changes_match_current_state():
    execution = run("examples/example.py")

    execution.recorder.jump_to(7)

    view = ExecutionView.from_execution(execution)

    for change in view.state_changes.changes:
        assert view.state.get(change.name) == change.current_value


def test_view_tracks_call_stack():
    execution = run("examples/example.py")

    for _ in range(5):
        execution.recorder.step_forward()

    view = ExecutionView.from_execution(execution)

    assert "greet" in view.call_stack


def test_view_includes_source_context():
    execution = run("examples/example.py")

    for _ in range(7):
        execution.recorder.step_forward()

    view = ExecutionView.from_execution(execution)

    assert view.source
    assert any(line.is_current for line in view.source)
    assert any(line.number == view.line for line in view.source)


def test_view_marks_current_source_line():
    execution = run("examples/example.py")

    for _ in range(7):
        execution.recorder.step_forward()

    view = ExecutionView.from_execution(execution)

    current_lines = [
        line for line in view.source
        if line.is_current
    ]

    assert len(current_lines) == 1
    assert current_lines[0].number == view.line