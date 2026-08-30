from performance_lab.execution import Execution
from performance_lab.view import ExecutionView


class Microscope:
    """Controls navigation through a program execution."""

    def __init__(self, execution: Execution) -> None:
        self.execution = execution

    @property
    def view(self) -> ExecutionView:
        return ExecutionView.from_execution(self.execution)

    @property
    def position(self) -> int:
        return self.execution.recorder.position

    @property
    def total_events(self) -> int:
        return len(self.execution.events)

    @property
    def finished(self) -> bool:
        return self.execution.recorder.finished

    @property
    def started(self) -> bool:
        return self.execution.recorder.started

    def step_forward(self) -> ExecutionView:
        self.execution.recorder.step_forward()
        return self.view

    def step_back(self) -> ExecutionView:
        self.execution.recorder.step_back()
        return self.view

    def reset(self) -> ExecutionView:
        self.execution.recorder.reset()
        return self.view

    def jump_to(self, position: int) -> ExecutionView:
        self.execution.recorder.jump_to(position)
        return self.view