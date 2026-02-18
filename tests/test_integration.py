"""Integration test: load lesson, setup exercise, validate."""

import subprocess
from pathlib import Path

from git_learn.lesson_loader import load_lesson
from git_learn.setup_exercise import setup_exercise
from git_learn.validator import validate_all


def test_beginner_01_init_full_flow(tmp_path: Path) -> None:
    lesson_path = Path(__file__).parent.parent / "lessons" / "beginner" / "01-init.md"
    if not lesson_path.exists():
        return
    lesson = load_lesson(lesson_path)
    exercise_dir = tmp_path / "exercise"
    setup_exercise(lesson, exercise_dir)

    # Lesson 01-init just needs a clean working tree after git init
    results = validate_all(lesson.validation, exercise_dir)
    assert all(r.passed for r in results), [r.message for r in results if not r.passed]


def test_beginner_05_commit_full_flow(tmp_path: Path) -> None:
    lesson_path = Path(__file__).parent.parent / "lessons" / "beginner" / "05-commit.md"
    if not lesson_path.exists():
        return
    lesson = load_lesson(lesson_path)
    exercise_dir = tmp_path / "exercise"
    setup_exercise(lesson, exercise_dir)

    # Simulate user solving: stage README.md and commit
    subprocess.run("git add README.md && git commit -m 'initial commit'",
                   shell=True, cwd=exercise_dir, capture_output=True, check=True)

    results = validate_all(lesson.validation, exercise_dir)
    assert all(r.passed for r in results), [r.message for r in results if not r.passed]
