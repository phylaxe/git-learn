"""Smoke test for the TUI app."""

import asyncio

from git_learn.app import GitLearnApp

from click.testing import CliRunner
from git_learn.__main__ import cli


def test_app_starts() -> None:
    async def _test() -> None:
        app = GitLearnApp()
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
