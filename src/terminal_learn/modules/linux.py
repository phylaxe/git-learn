"""Linux learning module configuration."""

from pathlib import Path

from ..module_config import ModuleConfig
from ..validator.linux import LINUX_VALIDATORS
from . import register_module


LESSONS_DIR = Path(__file__).parent.parent.parent.parent / "lessons" / "linux"
DOCKER_DIR = Path(__file__).parent.parent.parent.parent / "docker" / "linux"


def linux_setup(exercise_dir: Path) -> None:
    """Set up exercise directory for Linux lessons (no-op for Docker)."""
    # Docker container handles the environment.
    # Exercise dir is mounted as /exercise in the container.
    pass


LINUX_MODULE = ModuleConfig(
    name="linux",
    title="Linux Learn",
    lessons_dir=LESSONS_DIR,
    level_order=[
        "navigation", "files", "permissions", "text", "pipes", "search", "processes",
    ],
    level_labels={
        "navigation": "Kapitel 1: Navigation",
        "files": "Kapitel 2: Dateien & Verzeichnisse",
        "permissions": "Kapitel 3: Berechtigungen",
        "text": "Kapitel 4: Textverarbeitung",
        "pipes": "Kapitel 5: Pipes & Redirects",
        "search": "Kapitel 6: Suchen & Finden",
        "processes": "Kapitel 7: Prozesse",
    },
    shell_target="docker",
    setup_fn=linux_setup,
    docker_image="terminal-learn-linux:latest",
    docker_context=DOCKER_DIR,
    extra_validators=LINUX_VALIDATORS,
)

register_module(LINUX_MODULE)
