from performance_lab.events import ExecutionEvent


class Timeline:
    def __init__(self, events: list[ExecutionEvent]) -> None:
        self.events = events
        self.position = -1

    @property
    def current(self) -> ExecutionEvent | None:
        if self.position < 0 or self.position >= len(self.events):
            return None

        return self.events[self.position]

    @property
    def previous_event(self) -> ExecutionEvent | None:
        index = self.position - 1

        if index < 0:
            return None

        return self.events[index]

    @property
    def next_event(self) -> ExecutionEvent | None:
        index = self.position + 1

        if index >= len(self.events):
            return None

        return self.events[index]

    @property
    def current_index(self) -> int | None:
        if self.current is None:
            return None

        return self.position

    @property
    def total_events(self) -> int:
        return len(self.events)

    @property
    def progress(self) -> float:
        if not self.events:
            return 1.0

        if self.position < 0:
            return 0.0

        return (self.position + 1) / len(self.events)

    @property
    def finished(self) -> bool:
        return self.position >= len(self.events) - 1

    @property
    def started(self) -> bool:
        return self.position >= 0

    @property
    def has_next(self) -> bool:
        return self.position < len(self.events) - 1

    @property
    def has_previous(self) -> bool:
        return self.position > 0

    def step_forward(self) -> ExecutionEvent | None:
        if not self.has_next:
            return self.current

        self.position += 1
        return self.current

    def step_back(self) -> ExecutionEvent | None:
        if not self.has_previous:
            self.reset()
            return None

        self.position -= 1
        return self.current

    def reset(self) -> None:
        self.position = -1

    def __len__(self) -> int:
        return len(self.events)