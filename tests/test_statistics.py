from performance_lab.events import EventType, ExecutionEvent
from performance_lab.statistics import analyze_execution


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


def test_statistics_counts_events():
    stats = analyze_execution(make_events())

    assert stats.total_events == 5


def test_statistics_counts_functions():
    stats = analyze_execution(make_events())

    assert stats.function_count == 2
    assert stats.functions["<module>"].call_count == 1
    assert stats.functions["greet"].call_count == 1


def test_statistics_calculates_function_duration():
    stats = analyze_execution(make_events())

    assert stats.functions["greet"].total_duration == 2.0
    assert stats.functions["<module>"].total_duration == 4.0


def test_statistics_calculates_total_duration():
    stats = analyze_execution(make_events())

    assert stats.total_duration == 6.0


def test_statistics_counts_function_events():
    stats = analyze_execution(make_events())

    assert stats.functions["greet"].event_count == 3
    assert stats.functions["<module>"].event_count == 2


def test_statistics_calculates_average_event_time():
    stats = analyze_execution(make_events())

    assert stats.average_event_time == 6.0 / 5


def test_statistics_identifies_slowest_function():
    stats = analyze_execution(make_events())

    assert stats.slowest_function is not None
    assert stats.slowest_function.function == "<module>"