"""Lesson list screen — shows all lessons grouped by level."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label

from ..lesson_loader import Lesson
from ..progress import Progress
from .lesson import LessonScreen


LEVEL_LABELS = {
    "beginner": "Kapitel 1: Grundlagen",
    "intermediate": "Kapitel 2: Branches",
    "advanced": "Kapitel 3: History umschreiben",
    "stash": "Kapitel 4: Stash & Bisect",
    "remotes": "Kapitel 5: Remotes & Collaboration",
    "expert": "Kapitel 6: Profi-Workflows",
}


class LessonListItem(ListItem):
    """A single lesson entry in the list."""

    def __init__(self, lesson: Lesson, progress: Progress) -> None:
        super().__init__()
        self.lesson = lesson
        self._progress = progress

    def compose(self) -> ComposeResult:
        entry = self._progress.get_lesson(self.lesson.slug)
        if entry:
            stars = "\u2b50" * entry["stars"] + "\u2606" * (3 - entry["stars"])
        else:
            stars = "\u2606\u2606\u2606"
        yield Label(
            f"  {self.lesson.order:2d}. {self.lesson.title}  {stars}  [{self.lesson.points}pt]"
        )


class LessonListScreen(Screen):
    """Main screen showing all available lessons."""

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, lessons: list[Lesson], progress: Progress) -> None:
        super().__init__()
        self.lessons = lessons
        self._progress = progress

    def compose(self) -> ComposeResult:
        yield Header()
        items: list[ListItem] = []
        current_level = ""
        for lesson in self.lessons:
            if lesson.level != current_level:
                current_level = lesson.level
                label = LEVEL_LABELS.get(current_level, current_level)
                items.append(ListItem(Label(f"\n  [bold]{label}[/bold]"), disabled=True))
            items.append(LessonListItem(lesson, self._progress))
        yield ListView(*items)
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if isinstance(item, LessonListItem):
            self.app.selected_lesson = item.lesson
            self.app.push_screen(LessonScreen(item.lesson))

    def action_quit(self) -> None:
        self.app.exit()
