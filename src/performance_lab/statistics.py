from dataclasses import dataclass, field

from performance_lab.events import EventType, ExecutionEvent


@dataclass
class FunctionStats:
    function: str
    call_count: int = 0
    event_count: int = 0
    total_duration: float = 0.0


@dataclass
class ExecutionStats:
    total_events: int = 0
    total_duration: float = 0.0
    function_count: int = 0
    functions: dict[str, FunctionStats] = field(default_factory=dict)

    @property
    def average_event_time(self) -> float:
        if self.total_events == 0:
            return 0.0

        return self.total_duration / self.total_events

    @property
    def slowest_function(self) -> FunctionStats | None:
        if not self.functions:
            return None

        return max(
            self.functions.values(),
            key=lambda stats: stats.total_duration,
        )


def analyze_execution(events: list[ExecutionEvent]) -> ExecutionStats:
    stats = ExecutionStats(
        total_events=len(events),
    )

    active_calls: list[tuple[str, float]] = []

    for event in events:
        if event.event_type == EventType.FUNCTION_CALL:
            stats.functions.setdefault(
                event.function,
                FunctionStats(function=event.function),
            )

            stats.functions[event.function].call_count += 1
            active_calls.append((event.function, event.timestamp))

        elif event.event_type == EventType.FUNCTION_RETURN:
            if active_calls:
                function, start_timestamp = active_calls.pop()

                duration = event.timestamp - start_timestamp

                function_stats = stats.functions[function]
                function_stats.total_duration += duration

                stats.total_duration += duration

    for event in events:
        if event.function in stats.functions:
            stats.functions[event.function].event_count += 1

    stats.function_count = len(stats.functions)

    return stats