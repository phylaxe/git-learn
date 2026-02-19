"""Git learning module configuration."""

import subprocess
from pathlib import Path

from ..module_config import ModuleConfig
from . import register_module


LESSONS_DIR = Path(__file__).parent.parent.parent.parent / "lessons" / "git"


def git_setup(exercise_dir: Path) -> None:
    """Initialize a git repo with learner config."""
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


GIT_MODULE = ModuleConfig(
    name="git",
    title="Git Learn",
    lessons_dir=LESSONS_DIR,
    level_order=["beginner", "intermediate", "advanced", "stash", "remotes", "expert"],
    level_labels={
        "beginner": "Kapitel 1: Grundlagen",
        "intermediate": "Kapitel 2: Branches",
        "advanced": "Kapitel 3: History umschreiben",
        "stash": "Kapitel 4: Stash & Bisect",
        "remotes": "Kapitel 5: Remotes & Collaboration",
        "expert": "Kapitel 6: Profi-Workflows",
    },
    shell_target="local",
    setup_fn=git_setup,
)

register_module(GIT_MODULE)
