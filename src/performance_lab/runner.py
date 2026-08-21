from pathlib import Path

from performance_lab.tracer import Tracer


class Runner:
    def __init__(self, target_file: str | Path) -> None:
        self.target_file = Path(target_file).resolve()

    def run(self) -> Tracer:
        tracer = Tracer(str(self.target_file))

        tracer.start()

        exec(
            compile(
                self.target_file.read_text(),
                str(self.target_file),
                "exec",
            )
        )

        tracer.stop()

        return tracer