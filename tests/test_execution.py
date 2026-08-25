from performance_lab.execution import Execution
from performance_lab.runner import Runner


def test_execution_builds_analysis_objects():
    runner = Runner("examples/example.py")
    result = runner.run()

    execution = Execution.from_result(result)

    assert execution.events
    assert execution.recorder is not None
    assert execution.timeline is not None
    assert execution.call_tree is not None
    assert execution.statistics is not None
    assert execution.summary is not None


def test_execution_exposes_process():
    runner = Runner("examples/example.py")
    result = runner.run()

    execution = Execution.from_result(result)

    assert execution.process.returncode == 0
    assert "Hello, Jadon!" in execution.process.stdout


def test_execution_reports_success():
    runner = Runner("examples/example.py")
    result = runner.run()

    execution = Execution.from_result(result)

    assert execution.succeeded


def test_execution_shares_events_with_recorder():
    runner = Runner("examples/example.py")
    result = runner.run()

    execution = Execution.from_result(result)

    assert execution.recorder.events is execution.events