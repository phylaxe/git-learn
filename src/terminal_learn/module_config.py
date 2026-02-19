"""Module configuration — defines how each learning module behaves."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass
class ModuleConfig:
    """Configuration for a learning module (git, linux, etc.)."""

    name: str  # "git", "linux"
    title: str  # "Git Learn", "Linux Learn"
    lessons_dir: Path  # path to lessons/<module>/
    level_order: list[str]  # ["beginner", "intermediate", ...]
    level_labels: dict[str, str]  # {"beginner": "Chapter 1: Basics", ...}
    shell_target: str  # "local" or "docker"
    setup_fn: Callable[[Path], None]  # module-specific setup function
    docker_image: str | None = None  # e.g., "terminal-learn-linux:latest"
    docker_context: Path | None = None  # path to dir containing Dockerfile
    extra_validators: dict[str, Callable] = field(default_factory=dict)
