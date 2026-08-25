from dataclasses import dataclass, field
from typing import Any

from performance_lab.events import EventType, ExecutionEvent


@dataclass
class CallNode:
    function: str
    file: str
    line: int
    children: list["CallNode"] = field(default_factory=list)

    start_timestamp: float | None = None
    end_timestamp: float | None = None
    return_value: Any = None
    event_count: int = 0

    @property
    def duration(self) -> float | None:
        if self.start_timestamp is None or self.end_timestamp is None:
            return None

        return self.end_timestamp - self.start_timestamp

    def add_child(self, child: "CallNode") -> None:
        self.children.append(child)


class CallTree:
    def __init__(self, events: list[ExecutionEvent]) -> None:
        self.events = events
        self.root = CallNode(
            function="<root>",
            file="",
            line=0,
        )

    def build(self) -> CallNode:
        self.root = CallNode(
            function="<root>",
            file="",
            line=0,
        )

        stack: list[CallNode] = [self.root]

        for event in self.events:
            current = stack[-1]

            if event.event_type == EventType.FUNCTION_CALL:
                node = CallNode(
                    function=event.function,
                    file=event.file,
                    line=event.line,
                    start_timestamp=event.timestamp,
                )

                current.add_child(node)
                stack.append(node)

            elif event.event_type == EventType.FUNCTION_RETURN:
                if len(stack) > 1:
                    node = stack.pop()

                    node.end_timestamp = event.timestamp
                    node.return_value = event.data.get("return_value")

            if len(stack) > 1:
                stack[-1].event_count += 1

        return self.root

    def flatten(self) -> list[CallNode]:
        nodes: list[CallNode] = []

        def visit(node: CallNode) -> None:
            for child in node.children:
                nodes.append(child)
                visit(child)

        visit(self.root)
        return nodes