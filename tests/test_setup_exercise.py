"""Tests for exercise setup."""

from pathlib import Path

from terminal_learn.lesson_loader import load_lesson
from terminal_learn.setup_exercise import setup_exercise, get_exercise_path, teardown_exercise


def test_get_exercise_path() -> None:
    path = get_exercise_path("git", "beginner/01-init")
    assert "terminal-learn" in str(path)
    assert "beginner-01-init" in str(path)


def test_setup_exercise_creates_repo(tmp_path: Path) -> None:
    lesson_file = tmp_path / "lesson.md"
    lesson_file.write_text(
        '---\ntitle: "Test"\nlevel: beginner\norder: 1\npoints: 10\n'
        "setup:\n  - cmd: \"touch hello.txt\"\n"
        'task: |\n  Do it.\n'
        "hints:\n  - \"Hint\"\n"
        'solution: |\n  solution\n'
        "validation:\n  - type: file_exists\n    path: hello.txt\n"
        "---\n\nBody\n"
    )
    lesson = load_lesson(lesson_file)
    exercise_dir = tmp_path / "exercise"
    setup_exercise(lesson, exercise_dir)

    assert (exercise_dir / ".git").is_dir()
    assert (exercise_dir / "hello.txt").exists()
    assert (exercise_dir / ".terminal-learn").is_dir()


def test_setup_exercise_installs_command_log_hook(tmp_path: Path) -> None:
    lesson_file = tmp_path / "lesson.md"
    lesson_file.write_text(
        '---\ntitle: "Test"\nlevel: beginner\norder: 1\npoints: 10\n'
        "setup:\n  - cmd: \"git init\"\n"
        'task: |\n  Do it.\n'
        "hints:\n  - \"Hint\"\n"
        'solution: |\n  solution\n'
        "validation:\n  - type: working_tree_clean\n    expected: true\n"
        "---\n\nBody\n"
    )
    lesson = load_lesson(lesson_file)
    exercise_dir = tmp_path / "exercise"
    setup_exercise(lesson, exercise_dir)

    bashrc = exercise_dir / ".terminal-learn" / "bashrc"
    assert bashrc.exists()
    content = bashrc.read_text()
    assert "check" in content
    assert "hint" in content


def test_teardown_exercise(tmp_path: Path) -> None:
    exercise_dir = tmp_path / "exercise"
    exercise_dir.mkdir()
    (exercise_dir / "file.txt").write_text("x")
    teardown_exercise(exercise_dir)
    assert not exercise_dir.exists()
