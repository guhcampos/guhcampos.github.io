import click
from rich.console import Console

from .hugo import build_hugo
from .settings import settings
from .spotify.client import (
    fetch_spotify_playlists,
    list_spotify_playlists,
)

console = Console()


@click.group()
def guhcampos() -> None:
    pass


@guhcampos.group()
def hugo():
    pass


@hugo.command()
def build() -> None:
    build_hugo(src=settings.hugo_src_dir, dst=settings.hugo_dst_dir)


@guhcampos.group()
def spotify() -> None:
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
    List all playlists for the configured user.
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
