"""Smoke test for the TUI app."""

import asyncio

from terminal_learn.app import TerminalLearnApp
from terminal_learn.modules import get_module

from click.testing import CliRunner
from terminal_learn.__main__ import cli


def test_app_starts() -> None:
    async def _test() -> None:
        config = get_module("git")
        app = TerminalLearnApp(config)
        async with app.run_test() as pilot:
            assert app.title == "Git Learn"

    asyncio.run(_test())


def test_cli_status() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["status"])
    assert result.exit_code == 0
    assert "completed" in result.output.lower() or "lessons" in result.output.lower()


def test_cli_reset_cancel() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["reset"], input="n\n")
    assert result.exit_code == 0
