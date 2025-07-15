from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GUHCAMPOS_")

    hugo_src_dir: Path = REPO_ROOT / "hugo"
    hugo_dst_dir: Path = REPO_ROOT / "public"

    spotify_client_id: str
    spotify_client_secret: str
    spotify_user_id: str
    spotify_playlists: list[str] = [
        "This is Guhcampos",
        "01.01 Beard Growing",
    ]
    spotify_playlists_output_dir: Path = REPO_ROOT / "hugo" / "static" / "playlists"


settings = Settings()  # type: ignore
