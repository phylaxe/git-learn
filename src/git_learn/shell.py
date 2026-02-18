"""Shell spawning for modal TUI-Shell switch."""

import os
import subprocess
from enum import Enum, auto
from pathlib import Path


class ShellResult(Enum):
    """Result of the shell session."""

    CHECK = auto()  # User typed 'check' or Ctrl+D
    EXIT = auto()   # User wants to quit


def build_shell_env(exercise_dir: Path) -> dict[str, str]:
    """Build environment variables for the exercise shell."""
    env = os.environ.copy()
    env["GIT_LEARN_EXERCISE"] = str(exercise_dir)
    env["GIT_LEARN_LOG"] = str(exercise_dir / ".git" / "git-learn-log")
    return env


def spawn_shell(exercise_dir: Path) -> ShellResult:
    """Spawn an interactive shell in the exercise directory.

    The shell loads git-learn-bashrc which provides check/hint/solution commands.
    Returns ShellResult.CHECK when the user exits (check or Ctrl+D).
    """
    bashrc = exercise_dir / ".git" / "git-learn-bashrc"
    env = build_shell_env(exercise_dir)

    shell = os.environ.get("SHELL", "/bin/bash")
    if "zsh" in shell:
        env["ZDOTDIR"] = str(exercise_dir / ".git")
        zshrc = exercise_dir / ".git" / ".zshrc"
        zshrc.write_text(f"source {bashrc}\n")
        cmd = [shell]
    else:
        cmd = [shell, "--rcfile", str(bashrc)]

    subprocess.run(cmd, cwd=exercise_dir, env=env)

    # check command creates a marker file to distinguish from Ctrl+D
    check_marker = exercise_dir / ".git" / "git-learn-check"
    if check_marker.exists():
        check_marker.unlink()
        return ShellResult.CHECK
    return ShellResult.EXIT
