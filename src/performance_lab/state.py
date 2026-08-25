from typing import Any

from performance_lab.events import EventType, ExecutionEvent


class ProgramState:
    def __init__(self) -> None:
        self.scopes: list[dict[str, Any]] = [{}]

    @property
    def variables(self) -> dict[str, Any]:
        return self.scopes[-1]

    def apply(self, event: ExecutionEvent) -> None:
        if event.event_type == EventType.FUNCTION_CALL:
            if event.function != "<module>":
                self.scopes.append({})

            return

        if event.event_type == EventType.LINE_EXECUTION:
            locals_data = event.data.get("locals", {})

            if isinstance(locals_data, dict):
                self.scopes[-1].update(locals_data)

            return

        if event.event_type == EventType.FUNCTION_RETURN:
            if event.function != "<module>" and len(self.scopes) > 1:
                self.scopes.pop()

            return

    def snapshot(self) -> dict[str, Any]:
        state: dict[str, Any] = {}

        for scope in self.scopes:
            state.update(scope)

        return state

    def reset(self) -> None:
        self.scopes = [{}]