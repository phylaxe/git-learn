"""Load and parse lesson files (Markdown + YAML frontmatter)."""

from dataclasses import dataclass
from pathlib import Path

import frontmatter


LEVEL_ORDER = ["beginner", "intermediate", "advanced", "stash", "remotes", "expert"]


@dataclass
class Lesson:
    """A single lesson with metadata and content."""

    title: str
    level: str
    order: int
    points: int
    setup: list[dict[str, str]]
    task: str
    hints: list[str]
    solution: str
    validation: list[dict]
    body: str
    file_path: Path | None = None

    @property
    def slug(self) -> str:
        """Unique identifier like 'beginner/01-init'."""
        if self.file_path:
            return f"{self.level}/{self.file_path.stem}"
        return f"{self.level}/{self.order:02d}"


def load_lesson(path: Path) -> Lesson:
    """Load a single lesson from a Markdown file with YAML frontmatter."""
    post = frontmatter.load(str(path))
    meta = post.metadata
    return Lesson(
        title=meta["title"],
        level=meta["level"],
        order=meta["order"],
        points=meta["points"],
        setup=meta["setup"],
        task=meta["task"],
        hints=meta["hints"],
        solution=meta["solution"],
        validation=meta["validation"],
        body=post.content,
        file_path=path,
    )


def load_all_lessons(lessons_dir: Path) -> list[Lesson]:
    """Load all lessons from subdirectories, sorted by level and order."""
    lessons: list[Lesson] = []
    for md_file in sorted(lessons_dir.rglob("*.md")):
        lessons.append(load_lesson(md_file))
    lessons.sort(key=lambda l: (LEVEL_ORDER.index(l.level) if l.level in LEVEL_ORDER else 99, l.order))
    return lessons
