"""Schema v1: skeleton, load and deterministic dump.

Schema v1 is a stable intermediate representation shared by every renderer
of the resume compiler. Serialization is fully deterministic: a fixed key
order, string scalars, sorted collections, no timestamps.
"""

from __future__ import annotations

import yaml

SCHEMA_VERSION = 1


def empty_resume() -> dict:
    """Schema v1 skeleton with canonical key order."""
    return {
        "schema_version": SCHEMA_VERSION,
        "identity": {
            "name": None,
            "title": None,
            "email": None,
            "phone": None,
            "location": None,
            "linkedin": None,
        },
        "summary": None,
        "engagements": [],
        "skills_groups": [],
        "education": [],
        "extras": {
            "opensource": [],
            "volunteering": [],
            "teaching": [],
        },
    }


def load_schema_text(text: str) -> dict:
    return yaml.safe_load(text)


def dump_schema(resume: dict) -> str:
    """Deterministic YAML dump: fixed key order, block style, unicode kept."""
    return yaml.dump(
        resume,
        Dumper=yaml.SafeDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=4096,
    )
