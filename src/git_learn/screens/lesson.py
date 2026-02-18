"""Lesson screen — shows task description, handles shell switch."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Markdown

from ..lesson_loader import Lesson


class LessonScreen(Screen):
    """Shows the current lesson task and instructions."""

    BINDINGS = [
        ("enter", "start_exercise", "Start Exercise"),
        ("h", "show_hint", "Hint"),
        ("s", "show_solution", "Solution"),
        ("escape", "go_back", "Back"),
    ]

    def __init__(self, lesson: Lesson) -> None:
        super().__init__()
        self.lesson = lesson
        self.hints_shown = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            f"\n  [bold]{self.lesson.title}[/bold]"
            f"  |  Level: {self.lesson.level}  |  {self.lesson.points} Punkte\n"
        )
        yield Markdown(self.lesson.body)
        yield Static(f"\n  [bold]Aufgabe:[/bold]\n  {self.lesson.task}")
        yield Static(
            "\n  [dim]Enter: Shell öffnen  |  h: Hint  |  s: Lösung  |  Esc: Zurück[/dim]\n"
        )
        yield Footer()

    def action_start_exercise(self) -> None:
        self.app.start_exercise(self.lesson, self.hints_shown)

    def action_show_hint(self) -> None:
        if self.hints_shown < len(self.lesson.hints):
            hint = self.lesson.hints[self.hints_shown]
            self.hints_shown += 1
            self.mount(Static(f"\n  [yellow]Hint {self.hints_shown}:[/yellow] {hint}"))

    def action_show_solution(self) -> None:
        self.app.solution_viewed = True
        self.mount(Static(f"\n  [red]Lösung:[/red]\n  {self.lesson.solution}"))

    def action_go_back(self) -> None:
        self.app.pop_screen()
