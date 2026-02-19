"""Set up exercise repos for lessons."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .module_config import ModuleConfig

from .lesson_loader import Lesson


MARKER_DIR = ".terminal-learn"


def _build_task_echo(task: str) -> str:
    """Build echo statements for multi-line task text."""
    lines = task.rstrip().split("\n")
    return "\n".join(f"echo '    {line}'" for line in lines)


def get_exercise_path(module_or_slug: str, slug: str | None = None) -> Path:
    """Get the path for an exercise repo.

    Can be called as:
        get_exercise_path("git", "beginner/01-init")  # new style
        get_exercise_path("beginner/01-init")          # legacy compat
    """
    if slug is None:
        # Legacy single-arg call
        safe_name = module_or_slug.replace("/", "-")
        return Path(tempfile.gettempdir()) / "terminal-learn" / safe_name
    safe_name = slug.replace("/", "-")
    return Path(tempfile.gettempdir()) / "terminal-learn" / module_or_slug / safe_name


def setup_exercise(
    lesson: Lesson, exercise_dir: Path, config: ModuleConfig | None = None
) -> Path:
    """Create exercise dir, run module setup, run lesson setup, install logging."""
    if exercise_dir.exists():
        shutil.rmtree(exercise_dir)
    exercise_dir.mkdir(parents=True)

    # Create marker directory
    marker_dir = exercise_dir / MARKER_DIR
    marker_dir.mkdir()

    # Run module-specific setup (git init, docker start, etc.)
    if config is not None:
        config.setup_fn(exercise_dir)
    else:
        # Fallback: git init for backward compatibility
        _default_git_setup(exercise_dir)

    # Run lesson setup commands
    for step in lesson.setup:
        cmd = step["cmd"]
        subprocess.run(
            cmd, shell=True, cwd=exercise_dir,
            capture_output=True, check=True,
        )

    # Install command logging bashrc
    _install_logging(exercise_dir, lesson, config)

    return exercise_dir


def _default_git_setup(exercise_dir: Path) -> None:
    """Default git init for backward compatibility (used when no config)."""
    subprocess.run(["git", "init"], cwd=exercise_dir, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "learner@git-learn"],
        cwd=exercise_dir, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Git Learner"],
        cwd=exercise_dir, capture_output=True, check=True,
    )
    # Hide marker directory from git using local exclude (avoids untracked .gitignore)
    exclude_dir = exercise_dir / ".git" / "info"
    exclude_dir.mkdir(parents=True, exist_ok=True)
    exclude_file = exclude_dir / "exclude"
    existing = exclude_file.read_text() if exclude_file.exists() else ""
    if ".terminal-learn" not in existing:
        with open(exclude_file, "a") as f:
            f.write(".terminal-learn/\n")


def _install_logging(
    exercise_dir: Path, lesson: Lesson, config: ModuleConfig | None = None
) -> None:
    """Install bash functions for check/hint/solution and command logging."""
    marker_dir = exercise_dir / MARKER_DIR
    bashrc = marker_dir / "bashrc"
    log_file = marker_dir / "log"

    # Inside Docker, the exercise dir is mounted at /exercise
    if config is not None and config.shell_target == "docker":
        shell_exercise_dir = "/exercise"
    else:
        shell_exercise_dir = str(exercise_dir)

    # Build hint case statements
    hint_cases = ""
    for i, hint in enumerate(lesson.hints):
        escaped = hint.replace("'", "'\\''")
        hint_cases += f"        {i}) printf '\\033[33mHint {i + 1}:\\033[0m {escaped}\\n' ;;\n"

    # Escape solution for shell
    solution_escaped = lesson.solution.replace("'", "'\\''").rstrip()

    bashrc.write_text(f"""\
# terminal-learn shell environment
export TERMINAL_LEARN_EXERCISE="{shell_exercise_dir}"
export TERMINAL_LEARN_LOG="{shell_exercise_dir}/{MARKER_DIR}/log"
_TERMINAL_LEARN_HINT_COUNT=0

# Log git commands
_terminal_learn_log() {{
    echo "$(date +%s) $@" >> "$TERMINAL_LEARN_LOG"
    command git "$@"
}}
alias git='_terminal_learn_log'

# Shell commands
check() {{
    if [ -n "$1" ]; then
        echo "$*" > "$TERMINAL_LEARN_EXERCISE/{MARKER_DIR}/answer"
    fi
    touch "$TERMINAL_LEARN_EXERCISE/{MARKER_DIR}/check"
    exit 0
}}

hint() {{
    case $_TERMINAL_LEARN_HINT_COUNT in
{hint_cases}        *) echo "Keine weiteren Hints verfügbar." ;;
    esac
    _TERMINAL_LEARN_HINT_COUNT=$((_TERMINAL_LEARN_HINT_COUNT + 1))
}}

solution() {{
    printf '\\n'
    printf '\\033[31mLösung:\\033[0m\\n'
    echo '{solution_escaped}'
    printf '\\n'
}}

printf '\\n'
printf '  \\033[1mTerminal Learn: {lesson.title}\\033[0m\\n'
printf '\\n'
printf '  \\033[1mAufgabe:\\033[0m\\n'
{_build_task_echo(lesson.task)}
printf '\\n'
echo "  Befehle: check | hint | solution"
echo "  Ctrl+D um zurückzukehren."
printf '\\n'
""")


def teardown_exercise(exercise_dir: Path) -> None:
    """Remove exercise directory."""
    if exercise_dir.exists():
        shutil.rmtree(exercise_dir)
