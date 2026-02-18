"""CLI entry point."""

import click


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Git Learn - Interactive Git Terminal Trainer."""
    if ctx.invoked_subcommand is None:
        click.echo("git-learn v0.1.0 - use --help for commands")


if __name__ == "__main__":
    cli()
