from performance_lab.state_view import StateView


def test_state_view_contains_variables():
    state = {
        "name": "Jadon",
        "count": 3,
    }

    view = StateView.from_state(state)

    assert len(view.variables) == 2
    assert view.names == ["name", "count"]


def test_state_view_preserves_variable_values():
    state = {
        "name": "Jadon",
        "count": 3,
    }

    view = StateView.from_state(state)

    assert view.get("name") == "Jadon"
    assert view.get("count") == 3


def test_state_view_returns_default_for_missing_variable():
    view = StateView.from_state({"name": "Jadon"})

    assert view.get("missing") is None
    assert view.get("missing", 42) == 42


def test_state_view_checks_variable_existence():
    view = StateView.from_state({"name": "Jadon"})

    assert view.contains("name")
    assert not view.contains("missing")


def test_state_view_values_returns_dictionary():
    state = {
        "name": "Jadon",
        "count": 3,
    }

    view = StateView.from_state(state)

    assert view.values == state