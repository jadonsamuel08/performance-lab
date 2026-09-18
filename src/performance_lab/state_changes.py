from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StateChange:
    """Represents a change to a program variable."""

    name: str
    previous_value: Any
    current_value: Any


@dataclass(frozen=True)
class StateChangesView:
    """Represents variable changes at a point in execution."""

    changes: list[StateChange]

    @property
    def names(self) -> list[str]:
        return [change.name for change in self.changes]

    def get(self, name: str) -> StateChange | None:
        for change in self.changes:
            if change.name == name:
                return change

        return None

    def contains(self, name: str) -> bool:
        return self.get(name) is not None

    @classmethod
    def from_states(
        cls,
        previous: dict[str, Any],
        current: dict[str, Any],
    ) -> "StateChangesView":
        changes: list[StateChange] = []

        names = set(previous) | set(current)

        for name in names:
            previous_value = previous.get(name)
            current_value = current.get(name)

            if previous_value != current_value:
                changes.append(
                    StateChange(
                        name=name,
                        previous_value=previous_value,
                        current_value=current_value,
                    )
                )

        return cls(changes=changes)