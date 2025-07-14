import click
from rich.console import Console

from .hugo import build_hugo

console = Console()
from pathlib import Path

HUGO_DIR = Path(__file__).parent.parent.parent / "hugo"
PUBLIC_DIR = Path(__file__).parent.parent.parent / "public"


@click.group()
def cli() -> None:
    pass


@cli.command()
def build() -> None:
    build_hugo(src=HUGO_DIR, dst=PUBLIC_DIR)


if __name__ == "__main__":
    cli()
