"""Smoke test for the TUI app."""

import asyncio

from git_learn.app import GitLearnApp


def test_app_starts() -> None:
    async def _test() -> None:
        app = GitLearnApp()
        async with app.run_test() as pilot:
            assert app.title == "Git Learn"

    asyncio.run(_test())
