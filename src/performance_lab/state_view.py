from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StateVariable:
    """Represents a single program variable."""

    name: str
    value: Any


@dataclass(frozen=True)
class StateView:
    """Represents the program state at a point in execution."""

    variables: list[StateVariable]

    @property
    def names(self) -> list[str]:
        return [variable.name for variable in self.variables]

    @property
    def values(self) -> dict[str, Any]:
        return {
            variable.name: variable.value
            for variable in self.variables
        }

    def get(self, name: str, default: Any = None) -> Any:
        return self.values.get(name, default)

    def contains(self, name: str) -> bool:
        return name in self.values

    @classmethod
    def from_state(cls, state: dict[str, Any]) -> "StateView":
        return cls(
            variables=[
                StateVariable(name=name, value=value)
                for name, value in state.items()
            ]
        )