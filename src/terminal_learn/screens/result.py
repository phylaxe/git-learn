"""Result screen — shows validation results after exercise."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

from ..validator.base import ValidationResult


class ResultScreen(Screen):
    """Shows the result of the exercise validation."""

    BINDINGS = [
        ("enter", "next_lesson", "Next"),
        ("r", "retry", "Retry"),
        ("escape", "go_back", "Back to List"),
        ("q", "quit_app", "Beenden"),
    ]

    def __init__(
        self,
        results: list[ValidationResult],
        stars: int,
        lesson_title: str,
    ) -> None:
        super().__init__()
        self.results = results
        self.stars = stars
        self.lesson_title = lesson_title

    def compose(self) -> ComposeResult:
        yield Header()
        all_passed = all(r.passed for r in self.results)

        if all_passed:
            star_display = "\u2b50" * self.stars + "\u2606" * (3 - self.stars)
            yield Static(
                f"\n  [bold green]Bestanden![/bold green]  {star_display}\n"
                f"  {self.lesson_title}\n"
            )
        else:
            yield Static(f"\n  [bold red]Noch nicht geschafft.[/bold red]\n")

        for r in self.results:
            icon = "[green]\u2713[/green]" if r.passed else "[red]\u2717[/red]"
            yield Static(f"  {icon} {r.message}")

        if all_passed:
            yield Static("\n  [dim]Enter: Nächste Lektion  |  Esc: Zurück zur Liste[/dim]\n")
        else:
            yield Static("\n  [dim]r: Nochmal versuchen  |  Esc: Zurück zur Liste[/dim]\n")
        yield Footer()

    def action_next_lesson(self) -> None:
        self.app.next_lesson()

    def action_retry(self) -> None:
        self.app.retry_lesson()

    def action_go_back(self) -> None:
        self.app.pop_screen()
        self.app.pop_screen()  # Back to lesson list

    def action_quit_app(self) -> None:
        self.app.exit()
