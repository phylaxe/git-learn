"""Tests for lesson loader."""

from pathlib import Path

from terminal_learn.lesson_loader import Lesson, load_lesson, load_all_lessons


def test_load_lesson_parses_frontmatter(tmp_path: Path) -> None:
    lesson_file = tmp_path / "test.md"
    lesson_file.write_text(
        '---\ntitle: "Test"\nlevel: beginner\norder: 1\npoints: 10\n'
        "setup:\n  - cmd: \"git init\"\n"
        'task: |\n  Do something.\n'
        "hints:\n  - \"Hint 1\"\n"
        'solution: |\n  git status\n'
        "validation:\n  - type: working_tree_clean\n    expected: true\n"
        "---\n\n## Content\n\nBody text here.\n"
    )
    lesson = load_lesson(lesson_file)
    assert lesson.title == "Test"
    assert lesson.level == "beginner"
    assert lesson.order == 1
    assert lesson.points == 10
    assert lesson.setup == [{"cmd": "git init"}]
    assert lesson.task == "Do something.\n"
    assert lesson.hints == ["Hint 1"]
    assert lesson.solution == "git status\n"
    assert len(lesson.validation) == 1
    assert lesson.validation[0]["type"] == "working_tree_clean"
    assert lesson.body == "## Content\n\nBody text here."


def test_load_lesson_from_real_file() -> None:
    lesson_path = Path(__file__).parent.parent / "lessons" / "git" / "beginner" / "01-init.md"
    if not lesson_path.exists():
        return
    lesson = load_lesson(lesson_path)
    assert lesson.title == "Willkommen in der Zeitmaschine"
    assert lesson.level == "beginner"
    assert len(lesson.hints) >= 1


def test_load_all_lessons(tmp_path: Path) -> None:
    beginner = tmp_path / "beginner"
    beginner.mkdir()
    for i, title in enumerate(["First", "Second"], 1):
        (beginner / f"0{i}-test.md").write_text(
            f'---\ntitle: "{title}"\nlevel: beginner\norder: {i}\npoints: 10\n'
            f"setup:\n  - cmd: \"git init\"\n"
            f'task: |\n  Task {i}.\n'
            f"hints:\n  - \"Hint\"\n"
            f'solution: |\n  solution\n'
            f"validation:\n  - type: working_tree_clean\n    expected: true\n"
            f"---\n\nBody {i}\n"
        )
    lessons = load_all_lessons(tmp_path)
    assert len(lessons) == 2
    assert lessons[0].title == "First"
    assert lessons[1].title == "Second"


def test_load_all_lessons_sorted_by_level_and_order(tmp_path: Path) -> None:
    for level in ["beginner", "intermediate"]:
        d = tmp_path / level
        d.mkdir()
        (d / "01-test.md").write_text(
            f'---\ntitle: "{level}"\nlevel: {level}\norder: 1\npoints: 10\n'
            f"setup:\n  - cmd: \"git init\"\n"
            f'task: |\n  Task.\n'
            f"hints:\n  - \"Hint\"\n"
            f'solution: |\n  solution\n'
            f"validation:\n  - type: working_tree_clean\n    expected: true\n"
            f"---\n\nBody\n"
        )
    lessons = load_all_lessons(tmp_path)
    assert lessons[0].level == "beginner"
    assert lessons[1].level == "intermediate"
