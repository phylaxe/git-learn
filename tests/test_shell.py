"""Tests for shell spawning."""

from pathlib import Path

from terminal_learn.shell import build_shell_env, ShellResult


def test_build_shell_env(tmp_path: Path) -> None:
    env = build_shell_env(tmp_path)
    assert env["TERMINAL_LEARN_EXERCISE"] == str(tmp_path)
    assert "TERMINAL_LEARN_LOG" in env


def test_shell_result_from_check() -> None:
    result = ShellResult.CHECK
    assert result == ShellResult.CHECK


def test_shell_result_from_exit() -> None:
    result = ShellResult.EXIT
    assert result == ShellResult.EXIT
