from performance_lab.display import format_event
from performance_lab.runner import Runner


def test_example_program():
    runner = Runner("examples/example.py")
    tracer = runner.run()

    assert len(tracer.events) > 0

    for event in tracer.events:
        print(format_event(event))