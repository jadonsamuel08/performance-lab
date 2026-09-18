from performance_lab.state_changes import StateChangesView


def test_state_changes_detects_changed_variable():
    previous = {
        "count": 1,
    }
    current = {
        "count": 2,
    }

    changes = StateChangesView.from_states(previous, current)

    assert len(changes.changes) == 1
    assert changes.changes[0].name == "count"
    assert changes.changes[0].previous_value == 1
    assert changes.changes[0].current_value == 2


def test_state_changes_ignores_unchanged_variable():
    previous = {
        "count": 1,
    }
    current = {
        "count": 1,
    }

    changes = StateChangesView.from_states(previous, current)

    assert changes.changes == []


def test_state_changes_detects_new_variable():
    previous = {}
    current = {
        "name": "Jadon",
    }

    changes = StateChangesView.from_states(previous, current)

    assert changes.contains("name")

    change = changes.get("name")

    assert change is not None
    assert change.previous_value is None
    assert change.current_value == "Jadon"


def test_state_changes_detects_multiple_changes():
    previous = {
        "name": "Jadon",
        "count": 1,
    }
    current = {
        "name": "John",
        "count": 2,
    }

    changes = StateChangesView.from_states(previous, current)

    assert len(changes.changes) == 2
    assert set(changes.names) == {"name", "count"}


def test_state_changes_get_returns_none_for_missing_variable():
    changes = StateChangesView.from_states(
        {"count": 1},
        {"count": 2},
    )

    assert changes.get("missing") is None
    assert not changes.contains("missing")