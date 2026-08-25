from performance_lab.events import EventType, ExecutionEvent
from performance_lab.statistics import analyze_execution
from performance_lab.summary import create_summary, format_summary


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


def test_create_summary():
    stats = analyze_execution(make_events())
    summary = create_summary(stats)

    assert summary.total_events == 5
    assert summary.total_duration == 6.0
    assert summary.function_count == 2


def test_summary_contains_function_information():
    stats = analyze_execution(make_events())
    summary = create_summary(stats)

    functions = {
        function.function: function
        for function in summary.functions
    }

    assert functions["greet"].call_count == 1
    assert functions["greet"].event_count == 3
    assert functions["greet"].total_duration == 2.0


def test_summary_identifies_slowest_function():
    stats = analyze_execution(make_events())
    summary = create_summary(stats)

    assert summary.slowest_function == "<module>"


def test_format_summary_contains_execution_metrics():
    stats = analyze_execution(make_events())
    summary = create_summary(stats)

    output = format_summary(summary)

    assert "Performance Lab — Execution Summary" in output
    assert "Duration:" in output
    assert "Events:         5" in output
    assert "Functions:      2" in output


def test_format_summary_contains_function_metrics():
    stats = analyze_execution(make_events())
    summary = create_summary(stats)

    output = format_summary(summary)

    assert "greet" in output
    assert "Calls:        1" in output
    assert "Slowest function: <module>" in output