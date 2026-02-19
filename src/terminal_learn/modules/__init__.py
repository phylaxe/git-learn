"""Module registry — maps module names to their configurations."""

from __future__ import annotations

from ..module_config import ModuleConfig


_REGISTRY: dict[str, ModuleConfig] = {}


def register_module(config: ModuleConfig) -> None:
    """Register a module configuration."""
    _REGISTRY[config.name] = config


def get_module(name: str) -> ModuleConfig:
    """Get a registered module by name."""
    if name not in _REGISTRY:
        available = ", ".join(_REGISTRY.keys()) or "(none)"
        raise ValueError(f"Unknown module '{name}'. Available: {available}")
    return _REGISTRY[name]


def list_modules() -> list[str]:
    """List all registered module names."""
    return list(_REGISTRY.keys())


# Auto-register built-in modules
from . import git as _git_module  # noqa: E402, F401
from . import linux as _linux_module  # noqa: E402, F401
