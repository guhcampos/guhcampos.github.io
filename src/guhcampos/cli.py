import click
from rich.console import Console

from .hugo import build_hugo
from .logging import setup_logging
from .obsidian.client import pull_obsidian_content
from .settings import settings
from .spotify.client import (
    fetch_spotify_playlists,
    list_spotify_playlists,
)

setup_logging(logdir=settings.log_dir)

console = Console()


@click.group()
def guhcampos() -> None:
    """
    Utility CLI for building and publishing guhcampos.github.io.
    """
    pass


@guhcampos.group()
def hugo():
    """
    Interactions with the Hugo website generator.
    """
    pass


@hugo.command()
def build() -> None:
    """
    Build the Hugo website with standardized settings
    """
    build_hugo(src=settings.hugo_src_dir, dst=settings.hugo_dst_dir)


@guhcampos.group()
def obsidian():
    """
    Interactions with my Obsidian Vault. Most require the vault directory to be
    locally accessible in the path defined in the settings.py file or through
    an environment variable.
    """
    pass


@obsidian.command()
def pull() -> None:
    """
    Pull content from the obsidian vault and save it to the output directory for
    being later processed by Hugo.
    """
    pull_obsidian_content(
        posts_path=settings.obsidian_vault_root / "03 Posts",
        dst_dir=settings.obsidian_content_output_dir,
    )


@guhcampos.group()
def spotify() -> None:
    """
    Interactions with Spotify. In general these required the spotify client id
    and secret to operate, so they must be defined as environment variables according
    to the settings.py naming convention.
    """
    pass


@spotify.command()
def fetch_playlists() -> None:
    """
    Fetch playlists from Spotify and save them to the output directory as both
    M3U and JSON files.
    """
    playlists = settings.spotify_playlists

    success = fetch_spotify_playlists(
        playlists,
        settings.spotify_playlists_output_dir,
        settings.spotify_user_id,
        settings.spotify_client_id,
        settings.spotify_client_secret,
    )

    if not success:
        raise click.ClickException("Failed to fetch playlists")


@spotify.command()
def list_playlists() -> None:
    """
    List all spotify playlists for the configured user.
    """
    success = list_spotify_playlists(
        settings.spotify_user_id,
        settings.spotify_client_id,
        settings.spotify_client_secret,
    )

    if not success:
        raise click.ClickException("Failed to list playlists")


if __name__ == "__main__":
    guhcampos()
