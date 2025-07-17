from pydantic import BaseModel, HttpUrl
from slugify import slugify


class SpotifyTrack(BaseModel):
    name: str
    artists: list[str]
    album: str
    duration_ms: int
    url: HttpUrl

    @property
    def duration(self) -> int:
        return self.duration_ms // 1000


class SpotifyPlaylist(BaseModel):
    id: str
    name: str
    tracks: list[SpotifyTrack]
    url: HttpUrl
    description: str
    owner: str

    @property
    def slug(self) -> str:
        return slugify(self.name)

    def to_m3u(self) -> str:
        output = [
            "#EXTM3U",
            f"# {self.name}",
            f"# Description:{self.description}",
            f"# Created by: {self.owner}",
            f"# Tracks: {len(self.tracks)}",
            f"# Spotify URL: {self.url}",
        ]

        for track in self.tracks:
            artists_str = ", ".join(track.artists)
            output.append(
                f"#EXTINF:{track.duration},{artists_str} - {track.album} - {track.name}"
            )
            output.append(track.url.encoded_string())
        return "\n".join(output)

    def to_json(self) -> str:
        return self.model_dump_json()
