from performance_lab.api import run


def test_run_returns_execution():
    execution = run("examples/example.py")

    assert execution.events
    assert execution.succeeded


def test_run_provides_analysis():
    execution = run("examples/example.py")

    assert execution.recorder is not None
    assert execution.timeline is not None
    assert execution.call_tree is not None
    assert execution.statistics is not None
    assert execution.summary is not None


def test_run_captures_program_output():
    execution = run("examples/example.py")

    assert "Hello, Jadon!" in execution.process.stdout

def test_run_is_available_from_package():
    from performance_lab import run

    execution = run("examples/example.py")

    assert execution.succeeded
    assert execution.events