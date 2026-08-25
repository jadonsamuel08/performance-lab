from dataclasses import dataclass

from performance_lab.statistics import ExecutionStats, FunctionStats


@dataclass
class FunctionSummary:
    function: str
    call_count: int
    event_count: int
    total_duration: float


@dataclass
class ExecutionSummary:
    total_events: int
    total_duration: float
    function_count: int
    functions: list[FunctionSummary]
    slowest_function: str | None


def create_summary(stats: ExecutionStats) -> ExecutionSummary:
    functions = [
        FunctionSummary(
            function=function_stats.function,
            call_count=function_stats.call_count,
            event_count=function_stats.event_count,
            total_duration=function_stats.total_duration,
        )
        for function_stats in stats.functions.values()
    ]

    slowest = stats.slowest_function

    return ExecutionSummary(
        total_events=stats.total_events,
        total_duration=stats.total_duration,
        function_count=stats.function_count,
        functions=functions,
        slowest_function=slowest.function if slowest else None,
    )


def format_summary(summary: ExecutionSummary) -> str:
    lines = [
        "Performance Lab — Execution Summary",
        "",
        "Execution",
        "─────────",
        f"Duration:       {summary.total_duration:.6f}s",
        f"Events:         {summary.total_events}",
        f"Functions:      {summary.function_count}",
        "",
        "Functions",
        "─────────",
    ]

    for function in summary.functions:
        lines.extend(
            [
                function.function,
                f"  Calls:        {function.call_count}",
                f"  Duration:     {function.total_duration:.6f}s",
                f"  Events:       {function.event_count}",
                "",
            ]
        )

    if summary.slowest_function is not None:
        lines.append(f"Slowest function: {summary.slowest_function}")

    return "\n".join(lines)