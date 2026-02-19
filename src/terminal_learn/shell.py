"""Shell spawning for modal TUI-Shell switch."""

from __future__ import annotations

import os
import subprocess
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .module_config import ModuleConfig

from .setup_exercise import MARKER_DIR


class ShellResult(Enum):
    """Result of the shell session."""

    CHECK = auto()  # User typed 'check'
    EXIT = auto()   # User pressed Ctrl+D


def build_shell_env(exercise_dir: Path) -> dict[str, str]:
    """Build environment variables for the exercise shell."""
    env = os.environ.copy()
    env["TERMINAL_LEARN_EXERCISE"] = str(exercise_dir)
    env["TERMINAL_LEARN_LOG"] = str(exercise_dir / MARKER_DIR / "log")
    return env


def spawn_shell(exercise_dir: Path, config: ModuleConfig | None = None) -> ShellResult:
    """Spawn an interactive shell in the exercise directory."""
    if config is not None and config.shell_target == "docker":
        return _spawn_docker_shell(exercise_dir, config)
    return _spawn_local_shell(exercise_dir)


def _spawn_local_shell(exercise_dir: Path) -> ShellResult:
    """Spawn a local interactive shell."""
    marker_dir = exercise_dir / MARKER_DIR
    bashrc = marker_dir / "bashrc"
    env = build_shell_env(exercise_dir)

    shell = os.environ.get("SHELL", "/bin/bash")
    if "zsh" in shell:
        env["ZDOTDIR"] = str(marker_dir)
        zshrc = marker_dir / ".zshrc"
        zshrc.write_text(f"source {bashrc}\n")
        cmd = [shell]
    else:
        cmd = [shell, "--rcfile", str(bashrc)]

    subprocess.run(cmd, cwd=exercise_dir, env=env)

    check_marker = marker_dir / "check"
    if check_marker.exists():
        check_marker.unlink()
        return ShellResult.CHECK
    return ShellResult.EXIT


def _ensure_docker_image(config: ModuleConfig) -> None:
    """Check if the Docker image exists locally; build it if not."""
    image = config.docker_image or "terminal-learn-linux:latest"
    result = subprocess.run(
        ["docker", "image", "inspect", image],
        capture_output=True,
    )
    if result.returncode == 0:
        return  # image exists

    if config.docker_context is None:
        raise RuntimeError(
            f"Docker image '{image}' not found and no docker_context configured "
            f"for module '{config.name}'. Build the image manually or set docker_context."
        )

    print(f"\n  Docker-Image '{image}' nicht gefunden — wird jetzt gebaut …\n")
    subprocess.run(
        ["docker", "build", "-t", image, str(config.docker_context)],
        check=True,
    )
    print()


def _spawn_docker_shell(exercise_dir: Path, config: ModuleConfig) -> ShellResult:
    """Spawn an interactive shell inside a Docker container."""
    _ensure_docker_image(config)

    marker_dir = exercise_dir / MARKER_DIR
    bashrc_path = f"/exercise/{MARKER_DIR}/bashrc"

    cmd = [
        "docker", "run", "-it", "--rm",
        "-v", f"{exercise_dir}:/exercise",
        "-w", "/exercise",
        config.docker_image or "terminal-learn-linux:latest",
        "bash", "--rcfile", bashrc_path,
    ]
    subprocess.run(cmd)

    check_marker = marker_dir / "check"
    if check_marker.exists():
        check_marker.unlink()
        return ShellResult.CHECK
    return ShellResult.EXIT
