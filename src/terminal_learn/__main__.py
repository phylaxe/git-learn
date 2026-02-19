"""CLI entry point for terminal-learn."""

import click

from .app import TerminalLearnApp
from .modules import get_module, list_modules
from .progress import Progress


@click.group(invoke_without_command=True)
@click.option("--module", "-m", default="git", help="Learning module (git, linux, ...)")
@click.pass_context
def cli(ctx: click.Context, module: str) -> None:
    """Terminal Learn - Interactive Terminal Trainer."""
    ctx.ensure_object(dict)
    ctx.obj["module"] = module
    if ctx.invoked_subcommand is None:
        config = get_module(module)
        app = TerminalLearnApp(config)
        app.run()


@cli.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Show learning progress."""
    module = ctx.obj["module"]
    progress = Progress(module=module)
    click.echo(f"Module: {module}")
    click.echo(f"Lessons completed: {progress.lessons_completed}")
    click.echo(f"Total stars: {progress.total_stars}")

    if progress._lessons:
        click.echo("\nCompleted lessons:")
        for slug, data in progress._lessons.items():
            stars = "\u2b50" * data["stars"] + "\u2606" * (3 - data["stars"])
            click.echo(f"  {slug}: {stars}")


@cli.command()
@click.pass_context
def reset(ctx: click.Context) -> None:
    """Reset all progress."""
    module = ctx.obj["module"]
    if click.confirm(f"Are you sure you want to reset all {module} progress?"):
        progress = Progress(module=module)
        progress.reset()
        click.echo("Progress reset.")
    else:
        click.echo("Cancelled.")


@cli.command(name="modules")
def list_mods() -> None:
    """List available learning modules."""
    for name in list_modules():
        config = get_module(name)
        click.echo(f"  {name}: {config.title}")


if __name__ == "__main__":
    cli()
