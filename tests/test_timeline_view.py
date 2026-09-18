from performance_lab.api import run
from performance_lab.microscope import Microscope
from performance_lab.timeline_view import TimelineView


def test_timeline_view_contains_all_events():
    execution = run("examples/example.py")

    timeline = TimelineView.from_execution(execution)

    assert len(timeline.entries) == len(execution.events)
    assert timeline.total_events == len(execution.events)


def test_timeline_view_starts_before_execution():
    execution = run("examples/example.py")

    timeline = TimelineView.from_execution(execution)

    assert timeline.position == -1
    assert timeline.progress == 0.0
    assert not any(entry.is_current for entry in timeline.entries)


def test_timeline_view_marks_current_event():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    microscope.step_forward()

    timeline = microscope.timeline

    assert timeline.position == 0
    assert timeline.entries[0].is_current
    assert sum(entry.is_current for entry in timeline.entries) == 1


def test_timeline_view_updates_after_navigation():
    execution = run("examples/example.py")
    microscope = Microscope(execution)

    microscope.jump_to(5)

    timeline = microscope.timeline

    assert timeline.position == 5
    assert timeline.entries[5].is_current
    assert not timeline.entries[4].is_current
    assert not timeline.entries[6].is_current


def test_timeline_entries_match_execution_events():
    execution = run("examples/example.py")

    timeline = TimelineView.from_execution(execution)

    for index, entry in enumerate(timeline.entries):
        event = execution.events[index]

        assert entry.position == index
        assert entry.event_type == event.event_type.value
        assert entry.function == event.function
        assert entry.file == event.file
        assert entry.line == event.line