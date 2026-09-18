from performance_lab.api import run
from performance_lab.microscope import Microscope


def test_microscope_starts_before_execution():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    assert not microscope.started
    assert not microscope.finished
    assert microscope.position == -1
    assert microscope.total_events == len(execution.events)
    assert microscope.view.position == -1


def test_microscope_steps_forward():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    view = microscope.step_forward()

    assert microscope.started
    assert view.position == 0
    assert microscope.position == 0
    assert view.event is not None


def test_microscope_steps_backward():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    microscope.step_forward()
    microscope.step_forward()

    view = microscope.step_back()

    assert view.position == 0
    assert microscope.position == 0


def test_microscope_resets():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    microscope.step_forward()
    microscope.step_forward()

    view = microscope.reset()

    assert view.position == -1
    assert view.event is None
    assert microscope.position == -1
    assert not microscope.started


def test_microscope_jumps_to_event():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    view = microscope.jump_to(5)

    assert view.position == 5
    assert microscope.position == 5
    assert view.event is not None


def test_microscope_reaches_end():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    while not microscope.finished:
        microscope.step_forward()

    assert microscope.finished
    assert microscope.position == len(execution.events) - 1


def test_microscope_view_contains_source_context():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    for _ in range(7):
        microscope.step_forward()

    view = microscope.view

    assert view.source
    assert any(line.is_current for line in view.source)
    assert any(line.number == view.line for line in view.source)


def test_microscope_view_contains_program_state():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    while not microscope.finished:
        microscope.step_forward()

    view = microscope.view

    assert view.state.get("name") == "Jadon"
    assert view.state.get("result") == "Hello, Jadon!"


def test_microscope_syncs_timeline_after_step_forward():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    microscope.step_forward()

    assert execution.timeline.position == execution.recorder.position
    assert execution.timeline.current is execution.recorder.current


def test_microscope_syncs_timeline_after_step_back():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    microscope.step_forward()
    microscope.step_forward()
    microscope.step_back()

    assert execution.timeline.position == execution.recorder.position
    assert execution.timeline.current is execution.recorder.current


def test_microscope_syncs_timeline_after_reset():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    microscope.step_forward()
    microscope.reset()

    assert execution.timeline.position == execution.recorder.position
    assert execution.timeline.current is execution.recorder.current


def test_microscope_syncs_timeline_after_jump():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    microscope.jump_to(5)

    assert execution.timeline.position == execution.recorder.position
    assert execution.timeline.current is execution.recorder.current