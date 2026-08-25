from dataclasses import dataclass

from performance_lab.call_tree import CallTree
from performance_lab.events import ExecutionEvent
from performance_lab.recorder import Recorder
from performance_lab.runner import RunResult
from performance_lab.statistics import ExecutionStats, analyze_execution
from performance_lab.summary import ExecutionSummary, create_summary
from performance_lab.timeline import Timeline


@dataclass
class Execution:
    result: RunResult
    events: list[ExecutionEvent]
    recorder: Recorder
    timeline: Timeline
    call_tree: CallTree
    statistics: ExecutionStats
    summary: ExecutionSummary

    @classmethod
    def from_result(cls, result: RunResult) -> "Execution":
        events = result.events

        recorder = Recorder(events)
        timeline = Timeline(events)
        call_tree = CallTree(events)
        statistics = analyze_execution(events)
        summary = create_summary(statistics)

        return cls(
            result=result,
            events=events,
            recorder=recorder,
            timeline=timeline,
            call_tree=call_tree,
            statistics=statistics,
            summary=summary,
        )

    @property
    def process(self):
        return self.result.process

    @property
    def succeeded(self) -> bool:
        return self.process.returncode == 0