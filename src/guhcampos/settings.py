from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GUHCAMPOS_")

    hugo_src_dir: Path = REPO_ROOT / "hugo"
    hugo_dst_dir: Path = REPO_ROOT / "public"

    log_dir: Path = REPO_ROOT / "log"

    obsidian_vault_root: Path = REPO_ROOT / "obsidian"
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
        "Beard Growing",  # 01.01
        "Breathe",  # 01.02
        "Rock de Adulto",  # 01.03
        "Banda Indie Canta Hey!",  # 01.04
        # "Lento, Sujo e Pesado", # 01.05
        # Worshipping Questionable Entities", # 01.06
        "Prog Jovem",  # 01.07,
        "Funksouzera",  # 01.08
        "Dirty Rockin",  # 01.09
        "Esquerda Festiva",  # 01.10
        "Rebolation",  # 01.11
        # Metalerage", # 01.12
        "Smooth Talkin",  # 01.13
        "Powerzera",  # 01.14
        "Hot and Hard",  # 01.15
        # "Weird Stuff", # 01.16
        "80's Stuff the Nice and the Ugly",  # 01.17
        "Metalheads in Love",  # 01.18
        "Everybody Loves Covers",  # 01.19
        # "Game Soundtracks", # 01.20,
        "Balada G0y Internacional",  # 01.21,
        "Party Rock",  # 01.22,
        # "90's Tash Awesome Shit Great", # 01.23,
        "Resenha Fortíssima",  # 01.24,
        "Metalerage Corset",  # 01.25,
        "Heavy Brazilian Fucking Metal",  # 01.26
    ]
    spotify_playlists_output_dir: Path = REPO_ROOT / "hugo" / "static" / "playlists"


settings = Settings()  # type: ignore
