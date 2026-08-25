from performance_lab.events import EventType
from performance_lab.runner import Runner


def test_example_program():
    runner = Runner("examples/example.py")
    result = runner.run()

    assert result.process.returncode == 0
    assert "Hello, Jadon!" in result.process.stdout
    assert result.events


def test_runner_captures_execution_events():
    runner = Runner("examples/example.py")
    result = runner.run()

    event_types = {event.event_type for event in result.events}

    assert EventType.FUNCTION_CALL in event_types
    assert EventType.LINE_EXECUTION in event_types
    assert EventType.FUNCTION_RETURN in event_types