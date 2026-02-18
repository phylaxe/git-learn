"""Set up exercise repos for lessons."""

import shutil
import subprocess
import tempfile
from pathlib import Path

from .lesson_loader import Lesson


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
    _install_logging(exercise_dir)

    return exercise_dir


def _install_logging(exercise_dir: Path) -> None:
    """Install bash functions for check/hint/solution and git command logging."""
    bashrc = exercise_dir / ".git" / "git-learn-bashrc"
    log_file = exercise_dir / ".git" / "git-learn-log"

    bashrc.write_text(f"""\
# git-learn shell environment
export GIT_LEARN_EXERCISE="{exercise_dir}"
export GIT_LEARN_LOG="{log_file}"

# Log git commands
_git_learn_log() {{
    echo "$(date +%s) $@" >> "$GIT_LEARN_LOG"
    command git "$@"
}}
alias git='_git_learn_log'

# Shell commands
check() {{
    echo "__GIT_LEARN_CHECK__"
    exit 0
}}

hint() {{
    echo "__GIT_LEARN_HINT__"
}}

solution() {{
    echo "__GIT_LEARN_SOLUTION__"
}}

echo ""
echo "  Git Learn Exercise: {exercise_dir.name}"
echo "  Type 'check' when done, 'hint' for help, 'solution' to see the answer."
echo "  Press Ctrl+D to return to Git Learn."
echo ""
""")


def teardown_exercise(exercise_dir: Path) -> None:
    """Remove exercise directory."""
    if exercise_dir.exists():
        shutil.rmtree(exercise_dir)
