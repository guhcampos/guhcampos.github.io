import re
from collections.abc import Generator
from pathlib import Path
from typing import Any

import yaml
from loguru import logger

from ..utils import ensure_dir
from .errors import ObsidianPostError
from .models import ObsidianPost


def pull_obsidian_content(
    posts_path: Path,
    dst_dir: Path,
) -> None:
    published_posts = gen_published_posts(src=posts_path)

    ensure_dir(dst_dir / "en" / "posts")
    ensure_dir(dst_dir / "pt-br" / "posts")

    for post in published_posts:
        filename = dst_dir / post.language / "posts" / f"{post.slug}.md"
        logger.info(f"writing {filename}")
        with open(filename, "w") as f:
            f.write(post.as_hugo_post())


def gen_published_posts(src: Path) -> Generator[ObsidianPost, Any, Any]:
    errors = 0

    for path in src.rglob("*.md"):
        with open(path) as f:
            try:
                post = parse_obsidian_note(f.read())
                if post.publish:
                    yield post

            except ObsidianPostError as e:
                errors += 1
                logger.warning("Failed to parse an obsidian post")
                logger.debug(e)

    logger.info(f"Failed to parse {errors} obsidian posts")


def parse_obsidian_note(data: str, series: str | None = None) -> ObsidianPost:
    def _strip_id(s: str) -> str:
        return re.sub(r"^\d+(\.\d+)+\s", "", s)

    def _parse_tags(tags: list[str]) -> list[str]:
        tagset = set()

        for tag in tags:
            for t in tag.split("/"):
                tagset.add(t)

        return list(tagset)

    try:
        _, header, body = data.split("---", 2)
        title, content = body.strip("\n").split("\n", 1)
        frontmatter = yaml.safe_load(header)
        tags = _parse_tags(frontmatter.pop("tags"))

        print(80 * "#")
        print(tags)
        print(80 * "#")

        return ObsidianPost(
            content=content.strip("\n"),
            title=_strip_id(title.strip("# ").strip("\n")),
            tags=tags,
            **frontmatter,
        )
    except Exception as e:
        logger.debug(f"Failed to parse obsidian post: frontmatter: {frontmatter}")
        raise ObsidianPostError(f"Failed to parse obsidian post: {e}") from e
