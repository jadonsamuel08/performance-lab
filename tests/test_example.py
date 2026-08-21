from pathlib import Path

from performance_lab.tracer import Tracer


def test_example_program():
    example_path = Path("examples/example.py").resolve()

    tracer = Tracer(str(example_path))
    tracer.start()

    exec(
        compile(
            example_path.read_text(),
            str(example_path),
            "exec",
        )
    )

    tracer.stop()

    assert len(tracer.events) > 0

    for event in tracer.events:
        print(event)