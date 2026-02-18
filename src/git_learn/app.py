"""Main Textual application for Git Learn."""

from pathlib import Path

from textual.app import App

from .lesson_loader import Lesson, load_all_lessons
from .progress import Progress
from .screens.lesson import LessonScreen
from .screens.lesson_list import LessonListScreen
from .screens.result import ResultScreen
from .setup_exercise import setup_exercise, get_exercise_path, teardown_exercise
from .shell import spawn_shell
from .validator import validate_all


LESSONS_DIR = Path(__file__).parent.parent.parent / "lessons"


class GitLearnApp(App):
    """The Git Learn TUI application."""

    TITLE = "Git Learn"
    CSS = """
    Screen {
        background: $surface;
    }
    """

    def __init__(self, lessons_dir: Path | None = None) -> None:
        super().__init__()
        self._lessons_dir = lessons_dir or LESSONS_DIR
        self.progress = Progress()
        self.lessons: list[Lesson] = []
        self.selected_lesson: Lesson | None = None
        self.solution_viewed = False
        self._current_hints_shown = 0
        self._current_exercise_dir: Path | None = None

    def on_mount(self) -> None:
        self.lessons = load_all_lessons(self._lessons_dir)
        self.push_screen(LessonListScreen(self.lessons, self.progress))

    def start_exercise(self, lesson: Lesson, hints_shown: int) -> None:
        """Set up exercise and drop to shell."""
        self._current_hints_shown = hints_shown
        exercise_dir = get_exercise_path(lesson.slug)
        setup_exercise(lesson, exercise_dir)
        self._current_exercise_dir = exercise_dir

        # Suspend TUI and spawn shell
        with self.suspend():
            spawn_shell(exercise_dir)

        # Back from shell — validate
        self._validate_exercise(lesson)

    def _validate_exercise(self, lesson: Lesson) -> None:
        """Validate the exercise and show results."""
        exercise_dir = self._current_exercise_dir
        if exercise_dir is None:
            return
        results = validate_all(lesson.validation, exercise_dir)
        all_passed = all(r.passed for r in results)

        if all_passed:
            if self.solution_viewed:
                stars = 1
            elif self._current_hints_shown > 0:
                stars = 2
            else:
                stars = 3
            self.progress.complete_lesson(lesson.slug, stars, self._current_hints_shown)
        else:
            stars = 0

        self.push_screen(ResultScreen(results, stars, lesson.title))
        self.solution_viewed = False

    def next_lesson(self) -> None:
        """Move to the next lesson."""
        if self.selected_lesson:
            idx = self.lessons.index(self.selected_lesson)
            if idx + 1 < len(self.lessons):
                self.selected_lesson = self.lessons[idx + 1]
                self.pop_screen()  # Remove result
                self.pop_screen()  # Remove current lesson
                self.push_screen(LessonScreen(self.selected_lesson))

    def retry_lesson(self) -> None:
        """Retry the current lesson."""
        if self.selected_lesson:
            self.pop_screen()  # Remove result screen
