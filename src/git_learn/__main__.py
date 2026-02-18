"""CLI entry point for git-learn."""

from pathlib import Path

import click

from .app import GitLearnApp
from .progress import Progress


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Git Learn - Interactive Git Terminal Trainer."""
    if ctx.invoked_subcommand is None:
        app = GitLearnApp()
        app.run()


@cli.command()
def status() -> None:
    """Show learning progress."""
    progress = Progress()
    click.echo(f"Lessons completed: {progress.lessons_completed}")
    click.echo(f"Total stars: {progress.total_stars}")

    if progress._data["lessons"]:
        click.echo("\nCompleted lessons:")
        for slug, data in progress._data["lessons"].items():
            stars = "\u2b50" * data["stars"] + "\u2606" * (3 - data["stars"])
            click.echo(f"  {slug}: {stars}")


@cli.command()
def reset() -> None:
    """Reset all progress."""
    if click.confirm("Are you sure you want to reset all progress?"):
        progress = Progress()
        progress.reset()
        click.echo("Progress reset.")
    else:
        click.echo("Cancelled.")


if __name__ == "__main__":
    cli()
