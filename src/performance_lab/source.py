from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceLine:
    """Represents a single line of source code."""

    number: int
    text: str
    is_current: bool = False


class SourceViewer:
    """Provides source code surrounding an execution location."""

    def __init__(self, file: str | Path) -> None:
        self.file = Path(file).resolve()

        if not self.file.is_file():
            raise FileNotFoundError(f"Source file not found: {self.file}")

        self.lines = self.file.read_text(encoding="utf-8").splitlines()

    @property
    def total_lines(self) -> int:
        return len(self.lines)

    def get_line(self, number: int) -> SourceLine:
        if number < 1 or number > self.total_lines:
            raise IndexError(f"Source line out of range: {number}")

        return SourceLine(
            number=number,
            text=self.lines[number - 1],
        )

    def get_lines(
        self,
        start: int,
        end: int,
        current_line: int | None = None,
    ) -> list[SourceLine]:
        if start < 1:
            start = 1

        if end > self.total_lines:
            end = self.total_lines

        if start > end:
            return []

        return [
            SourceLine(
                number=number,
                text=self.lines[number - 1],
                is_current=number == current_line,
            )
            for number in range(start, end + 1)
        ]

    def get_context(
        self,
        line: int,
        radius: int = 2,
    ) -> list[SourceLine]:
        return self.get_lines(
            start=line - radius,
            end=line + radius,
            current_line=line,
        )