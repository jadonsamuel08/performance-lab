from performance_lab.api import run
from performance_lab.microscope import Microscope


def test_microscope_starts_before_execution():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    assert not microscope.started
    assert not microscope.finished
    assert microscope.view.position == -1


def test_microscope_steps_forward():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    view = microscope.step_forward()

    assert microscope.started
    assert view.position == 0
    assert view.event is not None


def test_microscope_steps_backward():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    microscope.step_forward()
    microscope.step_forward()

    view = microscope.step_back()

    assert view.position == 0


def test_microscope_resets():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    microscope.step_forward()
    microscope.step_forward()

    view = microscope.reset()

    assert view.position == -1
    assert view.event is None
    assert not microscope.started


def test_microscope_jumps_to_event():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    view = microscope.jump_to(5)

    assert view.position == 5
    assert view.event is not None


def test_microscope_reaches_end():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    while not microscope.finished:
        microscope.step_forward()

    assert microscope.finished
    assert microscope.view.position == len(execution.events) - 1