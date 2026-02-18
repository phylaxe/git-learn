"""Set up exercise repos for lessons."""

import shutil
import subprocess
import tempfile
from pathlib import Path

from .lesson_loader import Lesson


def _build_task_echo(task: str) -> str:
    """Build echo statements for multi-line task text."""
    lines = task.rstrip().split("\n")
    return "\n".join(f"echo '    {line}'" for line in lines)


def get_exercise_path(slug: str) -> Path:
    """Get the path for an exercise repo."""
    safe_name = slug.replace("/", "-")
    return Path(tempfile.gettempdir()) / "git-learn" / safe_name


def setup_exercise(lesson: Lesson, exercise_dir: Path) -> Path:
    """Create exercise repo, run setup commands, install logging."""
    if exercise_dir.exists():
        shutil.rmtree(exercise_dir)
    exercise_dir.mkdir(parents=True)

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=exercise_dir, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "learner@git-learn"],
        cwd=exercise_dir, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Git Learner"],
        cwd=exercise_dir, capture_output=True, check=True,
    )

    # Run setup commands
    for step in lesson.setup:
        cmd = step["cmd"]
        subprocess.run(
            cmd, shell=True, cwd=exercise_dir,
            capture_output=True, check=True,
        )

    # Install command logging bashrc
    _install_logging(exercise_dir, lesson)

    return exercise_dir


def _install_logging(exercise_dir: Path, lesson: Lesson) -> None:
    """Install bash functions for check/hint/solution and git command logging."""
    bashrc = exercise_dir / ".git" / "git-learn-bashrc"
    log_file = exercise_dir / ".git" / "git-learn-log"

    # Build hint case statements
    hint_cases = ""
    for i, hint in enumerate(lesson.hints):
        escaped = hint.replace("'", "'\\''")
        hint_cases += f"        {i}) echo '\\033[33mHint {i + 1}:\\033[0m {escaped}' ;;\n"

    # Escape solution for shell
    solution_escaped = lesson.solution.replace("'", "'\\''").rstrip()

    bashrc.write_text(f"""\
# git-learn shell environment
export GIT_LEARN_EXERCISE="{exercise_dir}"
export GIT_LEARN_LOG="{log_file}"
_GIT_LEARN_HINT_COUNT=0

# Log git commands
_git_learn_log() {{
    echo "$(date +%s) $@" >> "$GIT_LEARN_LOG"
    command git "$@"
}}
alias git='_git_learn_log'

# Shell commands
check() {{
    if [ -n "$1" ]; then
        echo "$*" > "$GIT_LEARN_EXERCISE/.git/git-learn-answer"
    fi
    touch "$GIT_LEARN_EXERCISE/.git/git-learn-check"
    exit 0
}}

hint() {{
    case $_GIT_LEARN_HINT_COUNT in
{hint_cases}        *) echo "Keine weiteren Hints verfügbar." ;;
    esac
    _GIT_LEARN_HINT_COUNT=$((_GIT_LEARN_HINT_COUNT + 1))
}}

solution() {{
    echo ""
    echo "\\033[31mLösung:\\033[0m"
    echo '{solution_escaped}'
    echo ""
}}

echo ""
echo "  \\033[1mGit Learn Exercise: {lesson.title}\\033[0m"
echo ""
echo "  \\033[1mAufgabe:\\033[0m"
{_build_task_echo(lesson.task)}
echo ""
echo "  Befehle: check | hint | solution"
echo "  Ctrl+D um zurückzukehren."
echo ""
""")


def teardown_exercise(exercise_dir: Path) -> None:
    """Remove exercise directory."""
    if exercise_dir.exists():
        shutil.rmtree(exercise_dir)
