from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GUHCAMPOS_")

    hugo_src_dir: Path = REPO_ROOT / "hugo"
    hugo_dst_dir: Path = REPO_ROOT / "public"

    log_dir: Path = REPO_ROOT / "log"

    obsidian_vault_root: Path = REPO_ROOT / "obsidian"
    # obsidian_content_output_dir: Path = REPO_ROOT / "hugo" / "build" / "obsidian"
    obsidian_content_output_dir: Path = REPO_ROOT / "hugo/content"
    obsidian_content_posts_dir: str = "03 Posts"
    obsidian_content_mappings: dict[str, str] = {
        "03 Posts": "posts",
    }

    spotify_client_id: str
    spotify_client_secret: str
    spotify_user_id: str
    spotify_playlists: list[str] = [
        "This is Guhcampos",
        "01.01 Beard Growing",
        "01.04 Banda Indie Canta Hey!",
    ]
    spotify_playlists_output_dir: Path = REPO_ROOT / "hugo" / "static" / "playlists"


settings = Settings()  # type: ignore
