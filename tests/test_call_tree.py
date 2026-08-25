from performance_lab.call_tree import CallTree
from performance_lab.events import EventType, ExecutionEvent


def make_events() -> list[ExecutionEvent]:
    return [
        ExecutionEvent(
            event_type=EventType.FUNCTION_CALL,
            timestamp=1.0,
            file="example.py",
            line=1,
            function="<module>",
            data={},
        ),
        ExecutionEvent(
            event_type=EventType.FUNCTION_CALL,
            timestamp=2.0,
            file="example.py",
            line=5,
            function="greet",
            data={},
        ),
        ExecutionEvent(
            event_type=EventType.LINE_EXECUTION,
            timestamp=3.0,
            file="example.py",
            line=6,
            function="greet",
            data={"locals": {"name": "Jadon"}},
        ),
        ExecutionEvent(
            event_type=EventType.FUNCTION_RETURN,
            timestamp=4.0,
            file="example.py",
            line=7,
            function="greet",
            data={"return_value": "Hello, Jadon!"},
        ),
        ExecutionEvent(
            event_type=EventType.FUNCTION_RETURN,
            timestamp=5.0,
            file="example.py",
            line=8,
            function="<module>",
            data={"return_value": None},
        ),
    ]


def test_call_tree_builds_function_hierarchy():
    tree = CallTree(make_events())
    root = tree.build()

    assert len(root.children) == 1
    assert root.children[0].function == "<module>"

    module = root.children[0]

    assert len(module.children) == 1
    assert module.children[0].function == "greet"


def test_call_tree_records_call_location():
    tree = CallTree(make_events())
    root = tree.build()

    module = root.children[0]
    greet = module.children[0]

    assert module.file == "example.py"
    assert module.line == 1

    assert greet.file == "example.py"
    assert greet.line == 5


def test_call_tree_flatten():
    tree = CallTree(make_events())
    tree.build()

    nodes = tree.flatten()

    assert [node.function for node in nodes] == [
        "<module>",
        "greet",
    ]


def test_call_tree_handles_nested_calls():
    events = [
        ExecutionEvent(
            event_type=EventType.FUNCTION_CALL,
            timestamp=1.0,
            file="example.py",
            line=1,
            function="<module>",
            data={},
        ),
        ExecutionEvent(
            event_type=EventType.FUNCTION_CALL,
            timestamp=2.0,
            file="example.py",
            line=2,
            function="outer",
            data={},
        ),
        ExecutionEvent(
            event_type=EventType.FUNCTION_CALL,
            timestamp=3.0,
            file="example.py",
            line=3,
            function="inner",
            data={},
        ),
        ExecutionEvent(
            event_type=EventType.FUNCTION_RETURN,
            timestamp=4.0,
            file="example.py",
            line=3,
            function="inner",
            data={},
        ),
        ExecutionEvent(
            event_type=EventType.FUNCTION_RETURN,
            timestamp=5.0,
            file="example.py",
            line=2,
            function="outer",
            data={},
        ),
        ExecutionEvent(
            event_type=EventType.FUNCTION_RETURN,
            timestamp=6.0,
            file="example.py",
            line=1,
            function="<module>",
            data={},
        ),
    ]

    tree = CallTree(events)
    root = tree.build()

    module = root.children[0]
    outer = module.children[0]
    inner = outer.children[0]

    assert module.function == "<module>"
    assert outer.function == "outer"
    assert inner.function == "inner"


def test_call_tree_records_timing():
    tree = CallTree(make_events())
    root = tree.build()

    module = root.children[0]
    greet = module.children[0]

    assert greet.start_timestamp == 2.0
    assert greet.end_timestamp == 4.0
    assert greet.duration == 2.0


def test_call_tree_records_return_value():
    tree = CallTree(make_events())
    root = tree.build()

    greet = root.children[0].children[0]

    assert greet.return_value == "Hello, Jadon!"


def test_call_tree_counts_events():
    tree = CallTree(make_events())
    root = tree.build()

    greet = root.children[0].children[0]

    assert greet.event_count == 2