from dataclasses import dataclass, field

from performance_lab.events import EventType, ExecutionEvent


@dataclass
class CallNode:
    function: str
    file: str
    line: int
    children: list["CallNode"] = field(default_factory=list)

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
        stack: list[CallNode] = [self.root]

        for event in self.events:
            if event.event_type == EventType.FUNCTION_CALL:
                node = CallNode(
                    function=event.function,
                    file=event.file,
                    line=event.line,
                )

                stack[-1].add_child(node)
                stack.append(node)

            elif event.event_type == EventType.FUNCTION_RETURN:
                if len(stack) > 1:
                    stack.pop()

        return self.root

    def flatten(self) -> list[CallNode]:
        nodes: list[CallNode] = []

        def visit(node: CallNode) -> None:
            for child in node.children:
                nodes.append(child)
                visit(child)

        visit(self.root)
        return nodes