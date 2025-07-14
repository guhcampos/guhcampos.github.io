"""Tests for the Spotify module."""

from unittest.mock import Mock, patch

import pytest

from guhcampos.spotify.client import (
    SpotifyAPI,
    fetch_spotify_playlists,
    list_spotify_playlists,
)
from guhcampos.spotify.models import SpotifyPlaylist, SpotifyTrack


def test_spotify_api_initialization():
    """Test SpotifyAPI initialization."""
    api = SpotifyAPI("test_client_id", "test_client_secret")
    assert api.client_id == "test_client_id"
    assert api.client_secret == "test_client_secret"
    assert api.access_token is None
    assert api.base_url == "https://api.spotify.com/v1"


@patch("guhcampos.spotify.client.requests.post")
def test_spotify_api_authenticate_success(mock_post):
    """Test successful authentication."""
    mock_response = Mock()
    mock_response.json.return_value = {"access_token": "test_token"}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    api = SpotifyAPI("test_client_id", "test_client_secret")
    result = api.authenticate()

    assert result is True
    assert api.access_token == "test_token"


@patch("guhcampos.spotify.client.requests.post")
def test_spotify_api_authenticate_failure(mock_post):
    """Test failed authentication."""
    mock_post.side_effect = Exception("Auth failed")

    api = SpotifyAPI("test_client_id", "test_client_secret")

    with pytest.raises(Exception):
        api.authenticate()


@patch("guhcampos.spotify.client.requests.get")
def test_fetch_playlists_pagination(mock_get):
    """Test fetch_playlists with pagination."""

    def mock_get_side_effect(*args, **kwargs):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None

        # Check the offset parameter to determine which page to return
        params = kwargs.get("params", {})
        offset = params.get("offset", 0)

        print(f"DEBUG: Mock called with offset={offset}, params={params}")

        if offset == 0:
            # First page: 50 items (full page, should continue)
            print("DEBUG: Returning first page with 50 items")
            mock_response.json.return_value = {
                "items": [
                    {
                        "id": str(i),
                        "name": f"Playlist {i}",
                        "description": f"Test playlist {i}",
                        "owner": {"display_name": "Test User"},
                        "external_urls": {
                            "spotify": f"https://open.spotify.com/playlist/{i}"
                        },
                    }
                    for i in range(1, 51)  # 50 items
                ]
            }
        elif offset == 50:
            # Second page: 3 items (partial page, should stop)
            print("DEBUG: Returning second page with 3 items")
            mock_response.json.return_value = {
                "items": [
                    {
                        "id": str(i),
                        "name": f"Playlist {i}",
                        "description": f"Test playlist {i}",
                        "owner": {"display_name": "Test User"},
                        "external_urls": {
                            "spotify": f"https://open.spotify.com/playlist/{i}"
                        },
                    }
                    for i in range(51, 54)  # 3 items
                ]
            }
        else:
            # Any other offset: empty
            print(f"DEBUG: Returning empty page for offset {offset}")
            mock_response.json.return_value = {"items": []}

        return mock_response

    mock_get.side_effect = mock_get_side_effect

    api = SpotifyAPI("test_client_id", "test_client_secret")
    api.access_token = "test_token"

    playlists = list(api.fetch_playlists("test_user"))

    assert len(playlists) == 53  # 50 from first page + 3 from second page
    assert playlists[0].name == "Playlist 1"
    assert playlists[49].name == "Playlist 50"  # Last item from first page
    assert playlists[50].name == "Playlist 51"  # First item from second page
    assert playlists[52].name == "Playlist 53"  # Last item from second page
    assert all(isinstance(p, SpotifyPlaylist) for p in playlists)


@patch("guhcampos.spotify.client.requests.get")
def test_get_playlist_tracks(mock_get):
    """Test get_playlist_tracks method."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "items": [
            {
                "track": {
                    "name": "Test Song",
                    "artists": [{"name": "Test Artist"}],
                    "album": {"name": "Test Album"},
                    "duration_ms": 180000,
                    "external_urls": {"spotify": "https://open.spotify.com/track/test"},
                }
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    api = SpotifyAPI("test_client_id", "test_client_secret")
    api.access_token = "test_token"

    tracks = api.get_playlist_tracks("test_playlist_id")

    assert len(tracks) == 1
    assert isinstance(tracks[0], SpotifyTrack)
    assert tracks[0].name == "Test Song"
    assert tracks[0].artists == ["Test Artist"]
    assert tracks[0].album == "Test Album"
    assert tracks[0].duration_ms == 180000


def test_spotify_track_model():
    """Test SpotifyTrack model."""
    track = SpotifyTrack(
        name="Test Song",
        artists=["Test Artist"],
        album="Test Album",
        duration_ms=180000,
        url="https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh",
    )

    assert track.name == "Test Song"
    assert track.artists == ["Test Artist"]
    assert track.album == "Test Album"
    assert track.duration_ms == 180000
    assert track.duration == 180  # duration in seconds


def test_spotify_playlist_model():
    """Test SpotifyPlaylist model."""
    playlist = SpotifyPlaylist(
        id="test_id",
        name="Test Playlist",
        tracks=[],
        url="https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M",
        description="Test description",
        owner="Test User",
    )

    assert playlist.id == "test_id"
    assert playlist.name == "Test Playlist"
    assert playlist.description == "Test description"
    assert playlist.owner == "Test User"
    assert playlist.slug == "test-playlist"  # slugified name


def test_playlist_to_m3u():
    """Test playlist to_m3u method."""
    track = SpotifyTrack(
        name="Test Song",
        artists=["Test Artist"],
        album="Test Album",
        duration_ms=180000,
        url="https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh",
    )

    playlist = SpotifyPlaylist(
        id="test_id",
        name="Test Playlist",
        tracks=[track],
        url="https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M",
        description="Test description",
        owner="Test User",
    )

    m3u_content = playlist.to_m3u()

    assert "#EXTM3U" in m3u_content
    assert "Test Playlist" in m3u_content
    assert "Test User" in m3u_content
    assert "#EXTINF:180,Test Artist - Test Album - Test Song" in m3u_content
    assert "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh" in m3u_content


@patch("guhcampos.spotify.client.SpotifyAPI")
def test_fetch_spotify_playlists_success(mock_spotify_api, tmp_path):
    """Test fetch_spotify_playlists with successful API calls."""
    mock_api_instance = Mock()
    mock_api_instance.authenticate.return_value = True

    # Mock playlist
    mock_playlist = SpotifyPlaylist(
        id="1",
        name="Test Playlist",
        tracks=[],
        url="https://open.spotify.com/playlist/1",
        description="Test description",
        owner="Test User",
    )

    mock_api_instance.fetch_playlists.return_value = [mock_playlist]
    mock_api_instance.get_playlist_tracks.return_value = []
    mock_spotify_api.return_value = mock_api_instance

    result = fetch_spotify_playlists(
        ["Test Playlist"],
        tmp_path,  # Use pytest's tmp_path fixture
        "test_user_id",
        "test_client_id",
        "test_client_secret",
    )

    assert result is True
    mock_api_instance.authenticate.assert_called_once()
    mock_api_instance.fetch_playlists.assert_called_once_with("test_user_id")


@patch("guhcampos.spotify.client.SpotifyAPI")
def test_list_spotify_playlists_success(mock_spotify_api):
    """Test list_spotify_playlists with successful API calls."""
    mock_api_instance = Mock()
    mock_api_instance.authenticate.return_value = True

    mock_playlist = SpotifyPlaylist(
        id="1",
        name="Test Playlist",
        tracks=[],
        url="https://open.spotify.com/playlist/1",
        description="Test description",
        owner="Test User",
    )

    mock_api_instance.fetch_playlists.return_value = [mock_playlist]
    mock_spotify_api.return_value = mock_api_instance

    result = list_spotify_playlists(
        "test_user",
        "test_client_id",
        "test_client_secret",
    )

    assert result is True
    mock_api_instance.authenticate.assert_called_once()
    mock_api_instance.fetch_playlists.assert_called_once_with("test_user")
