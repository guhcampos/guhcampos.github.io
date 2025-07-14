import base64
from collections.abc import Generator
from pathlib import Path

import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

from .models import SpotifyPlaylist, SpotifyTrack


class SpotifyAPI:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.base_url = "https://api.spotify.com/v1"

    def authenticate(self) -> bool:
        def _get_basic_auth() -> str:
            credentials = f"{self.client_id}:{self.client_secret}"
            return base64.b64encode(credentials.encode()).decode()

        auth_url = "https://accounts.spotify.com/api/token"
        auth_data = {"grant_type": "client_credentials"}
        auth_headers = {"Authorization": f"Basic {_get_basic_auth()}"}

        console.print("[yellow]Authenticating with Spotify...[/yellow]")

        try:
            response = requests.post(auth_url, data=auth_data, headers=auth_headers)
            response.raise_for_status()

            self.access_token = response.json()["access_token"]

            if not self.access_token:
                raise Exception("Authentication failed")

            console.print("[green]Authentication successful![/green]")
            return True

        except requests.RequestException as e:
            console.print(f"[red]Authentication failed: {e}[/red]")
            raise

    def fetch_playlists(self, user_id: str) -> Generator[SpotifyPlaylist, None, None]:
        """
        Yield all playlists for a given user.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        limit = 50  # Maximum allowed by Spotify API
        offset = 0

        while True:
            params = {"limit": limit, "offset": offset}

            try:
                response = requests.get(
                    f"{self.base_url}/users/{user_id}/playlists",
                    headers=headers,
                    params=params,
                )
                response.raise_for_status()

                data = response.json()
                playlists = data.get("items", [])

                if not playlists:
                    break

                yield from [
                    SpotifyPlaylist(
                        description=playlist["description"],
                        owner=playlist["owner"]["display_name"],
                        url=playlist["external_urls"]["spotify"],
                        id=playlist["id"],
                        name=playlist["name"],
                        tracks=[],  # playlist["tracks"],
                    )
                    for playlist in playlists
                ]

                if len(playlists) < limit:
                    break

                offset += limit

            except requests.RequestException as e:
                console.print(f"[red]Failed to fetch playlists: {e}[/red]")
                break

    def get_playlist_tracks(self, playlist_id: str) -> list[SpotifyTrack]:
        """
        Get all tracks from a playlist.
        """

        headers = {"Authorization": f"Bearer {self.access_token}"}
        tracks = []
        url = f"{self.base_url}/playlists/{playlist_id}/tracks"

        while url:
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()

                data = response.json()
                tracks.extend(data.get("items", []))

                url = data.get("next")

            except requests.RequestException as e:
                console.print(f"[red]Failed to fetch tracks: {e}[/red]")
                break

        tracks.sort(key=lambda x: x["track"]["name"])
        tracks.sort(key=lambda x: x["track"]["artists"][0]["name"])

        return [
            SpotifyTrack(
                name=track["track"]["name"],
                artists=[artist["name"] for artist in track["track"]["artists"]],
                album=track["track"]["album"]["name"],
                duration_ms=track["track"]["duration_ms"],
                url=track["track"]["external_urls"]["spotify"],
            )
            for track in tracks
        ]


def fetch_spotify_playlists(
    playlists_filter: list[str],
    output_dir: Path,
    user_id: str,
    client_id: str,
    client_secret: str,
):
    """
    Fetch all Spotify playlists for a user and save them as M3U files.

    Args:
        user_id: Spotify user ID
        output_dir: Directory to save M3U files
        client_id: Spotify client ID
        client_secret: Spotify client secret

    Returns:
        True if successful, False otherwise
    """
    spotify = SpotifyAPI(client_id, client_secret)
    spotify.authenticate()

    output_dir.mkdir(parents=True, exist_ok=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for playlist in spotify.fetch_playlists(user_id):
            if playlist.name in playlists_filter:
                task = progress.add_task(f"Processing '{playlist.name}'...", total=None)

                playlist.tracks = spotify.get_playlist_tracks(playlist.id)

                progress.update(
                    task,
                    description=f"[green]Processed '{playlist.name}' ({len(playlist.tracks)} tracks)[/green]",
                )

                with open(
                    output_dir / f"{playlist.slug}.m3u", "w", encoding="utf-8"
                ) as f:
                    f.write(playlist.to_m3u())

                with open(
                    output_dir / f"{playlist.slug}.json", "w", encoding="utf-8"
                ) as f:
                    f.write(playlist.to_json())

    return True


def list_spotify_playlists(
    user_id: str,
    client_id: str,
    client_secret: str,
):
    """
    List all playlists for a user using pagination.

    Args:
        user_id: Spotify user ID
        client_id: Spotify client ID
        client_secret: Spotify client secret

    Returns:
        True if successful, False otherwise
    """

    spotify = SpotifyAPI(client_id, client_secret)
    spotify.authenticate()

    playlists = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Fetching playlists...", total=None)

        try:
            for playlist in spotify.fetch_playlists(user_id):
                playlists.append(playlist)
                progress.update(
                    task, description=f"Found {len(playlists)} playlists..."
                )

        except Exception as e:
            progress.update(task, description=f"[red]Error: {e}[/red]")
            return False
    console.print(
        Panel(
            f"[bold green]Found {len(playlists)} playlists[/bold green]\n\n"
            + "\n".join(
                [f"• {p.name} ({len(p.tracks)} tracks) - {p.url})" for p in playlists]
            ),
            title="📋 All Playlists",
            border_style="blue",
        )
    )

    return True
