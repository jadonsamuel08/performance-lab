from pathlib import Path

import pytest

from performance_lab.source import SourceLine, SourceViewer


EXAMPLE_FILE = Path("examples/example.py")


def test_source_viewer_loads_source_file():
    viewer = SourceViewer(EXAMPLE_FILE)

    assert viewer.total_lines > 0


def test_source_viewer_gets_single_line():
    viewer = SourceViewer(EXAMPLE_FILE)

    line = viewer.get_line(1)

    assert isinstance(line, SourceLine)
    assert line.number == 1
    assert line.text
    assert not line.is_current


def test_source_viewer_gets_multiple_lines():
    viewer = SourceViewer(EXAMPLE_FILE)

    lines = viewer.get_lines(1, 3)

    assert len(lines) == 3
    assert [line.number for line in lines] == [1, 2, 3]


def test_source_viewer_marks_current_line():
    viewer = SourceViewer(EXAMPLE_FILE)

    lines = viewer.get_lines(1, 3, current_line=2)

    assert not lines[0].is_current
    assert lines[1].is_current
    assert not lines[2].is_current


def test_source_viewer_gets_context():
    viewer = SourceViewer(EXAMPLE_FILE)

    lines = viewer.get_context(3, radius=1)

    assert [line.number for line in lines] == [2, 3, 4]
    assert lines[1].is_current


def test_source_viewer_clamps_context_to_file():
    viewer = SourceViewer(EXAMPLE_FILE)

    lines = viewer.get_context(1, radius=5)

    assert lines[0].number == 1
    assert lines[-1].number == min(6, viewer.total_lines)


def test_source_viewer_rejects_invalid_line():
    viewer = SourceViewer(EXAMPLE_FILE)

    with pytest.raises(IndexError):
        viewer.get_line(0)

    with pytest.raises(IndexError):
        viewer.get_line(viewer.total_lines + 1)


def test_source_viewer_rejects_missing_file(tmp_path):
    missing_file = tmp_path / "missing.py"

    with pytest.raises(FileNotFoundError):
        SourceViewer(missing_file)