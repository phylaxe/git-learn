"""Tests for progress tracking."""

from pathlib import Path

from terminal_learn.progress import Progress


def test_new_progress_is_empty(tmp_path: Path) -> None:
    progress = Progress(tmp_path / "progress.json")
    assert progress.get_lesson("beginner/01-init") is None
    assert progress.total_stars == 0
    assert progress.lessons_completed == 0


def test_complete_lesson(tmp_path: Path) -> None:
    progress = Progress(tmp_path / "progress.json")
    progress.complete_lesson("beginner/01-init", stars=3, hints_used=0)
    lesson = progress.get_lesson("beginner/01-init")
    assert lesson is not None
    assert lesson["stars"] == 3
    assert lesson["completed"] is True
    assert progress.total_stars == 3
    assert progress.lessons_completed == 1


def test_progress_persists(tmp_path: Path) -> None:
    path = tmp_path / "progress.json"
    progress = Progress(path)
    progress.complete_lesson("beginner/01-init", stars=2, hints_used=1)

    progress2 = Progress(path)
    lesson = progress2.get_lesson("beginner/01-init")
    assert lesson is not None
    assert lesson["stars"] == 2


def test_best_score_kept(tmp_path: Path) -> None:
    progress = Progress(tmp_path / "progress.json")
    progress.complete_lesson("beginner/01-init", stars=1, hints_used=2)
    progress.complete_lesson("beginner/01-init", stars=3, hints_used=0)
    assert progress.get_lesson("beginner/01-init")["stars"] == 3


def test_worse_score_not_overwritten(tmp_path: Path) -> None:
    progress = Progress(tmp_path / "progress.json")
    progress.complete_lesson("beginner/01-init", stars=3, hints_used=0)
    progress.complete_lesson("beginner/01-init", stars=1, hints_used=2)
    assert progress.get_lesson("beginner/01-init")["stars"] == 3


def test_reset(tmp_path: Path) -> None:
    progress = Progress(tmp_path / "progress.json")
    progress.complete_lesson("beginner/01-init", stars=3, hints_used=0)
    progress.reset()
    assert progress.lessons_completed == 0


def test_multi_module_isolation(tmp_path: Path) -> None:
    path = tmp_path / "progress.json"
    git_progress = Progress(path, module="git")
    git_progress.complete_lesson("beginner/01-init", stars=3, hints_used=0)

    linux_progress = Progress(path, module="linux")
    assert linux_progress.lessons_completed == 0

    linux_progress.complete_lesson("navigation/01-pwd-ls", stars=2, hints_used=1)
    assert linux_progress.lessons_completed == 1

    # Git progress should be unchanged
    git_progress2 = Progress(path, module="git")
    assert git_progress2.lessons_completed == 1
