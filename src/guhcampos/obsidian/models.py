import datetime

import slugify
import yaml
from pydantic import BaseModel


class ObsidianPost(BaseModel):
    content: str
    language: str
    publish_date: datetime.date
    publish: bool
    tags: list[str]
    title: str
    series: str | None = None

    @property
    def slug(self) -> str:
        return slugify.slugify(self.title)

    def as_hugo_post(self) -> str:
        return (
            "---\n"
            + f"date: {self.publish_date}\n"
            + f"title: {self.title}\n"
            + f"tags: \n{yaml.dump(self.tags)}\n"
            + "---\n"
            + self.content
        )

    #     return (
    #         dedent(f"""
    #     ---
    #
    #     title: {self.title}
    #     tags: {yaml.dump(self.tags)}
    #     ---
    #     """)
    #         + self.content
    #     )
    #     # topics: {", ".join(self.topics)}
