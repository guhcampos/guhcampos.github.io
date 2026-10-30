"""HTML renderer: Schema v1 dict -> one self-contained deterministic index.html.

Fully deterministic: hard-coded English month names (no locale-dependent
`strftime`), content-derived ids (no random/timestamp tokens), and a fixed
template. All CSS is embedded; no JS, no external requests. Print-friendly
A4 via @page/@media print; dark/light via prefers-color-scheme with light
forced under print.
"""

from __future__ import annotations

import re
import unicodedata
from importlib.resources import files as package_files
from pathlib import Path

import jinja2

MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        str(package_files("resume_compiler") / "templates")
    ),
    autoescape=True,
    keep_trailing_newline=True,
    undefined=jinja2.StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)


def format_date(value) -> str:
    """Deterministic date formatting, locale-independent."""
    if not value:
        return "…"
    value = str(value)
    if len(value) >= 4 and value[:4].isdigit():
        if len(value) >= 7 and value[5:7].isdigit():
            month = int(value[5:7])
            if 1 <= month <= 12:
                return f"{MONTHS[month - 1]} {value[:4]}"
            return value  # malformed month: keep the raw string verbatim
        return value[:4]
    return value


@jinja2.pass_context
def date_range(ctx, engagement) -> str:
    start = format_date(engagement.get("start_date"))
    end = format_date(engagement.get("end_date"))
    if engagement.get("start_date") and engagement.get("end_date"):
        return f"{start} – {end}"
    if engagement.get("start_date"):
        return f"{start} – Present"
    if engagement.get("end_date"):
        return f"through {end}"
    return ""


def contact_items(identity: dict) -> list[dict]:
    items = []
    email, phone = identity.get("email"), identity.get("phone")
    location, linkedin = identity.get("location"), identity.get("linkedin")
    if email:
        items.append({"text": email, "href": f"mailto:{email}"})
    if phone:
        items.append({"text": phone, "href": None})
    if location:
        items.append({"text": location, "href": None})
    if linkedin:
        display = re.sub(r"^https?://(www\.)?", "", str(linkedin)).rstrip("/")
        display = urllib_unquote(display)
        text = str(linkedin)
        href = text if text.startswith("http") else f"https://{text}"
        items.append({"text": display, "href": href})
    return items


def urllib_unquote(text: str) -> str:
    return text


def slug(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(text))
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slugified = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text).strip("-").lower()
    return slugified or "section"


def render(resume: dict) -> str:
    """Render Schema v1 to a self-contained HTML string."""
    template = _env.get_template("resume.html.j2")
    data = {
        "identity": resume.get("identity") or {},
        "summary": resume.get("summary"),
        "engagements": resume.get("engagements") or [],
        "skills_groups": resume.get("skills_groups") or [],
        "education": resume.get("education") or [],
        "extras": resume.get("extras") or {},
        "contact_items": contact_items(resume.get("identity") or {}),
        "date_range": date_range,
        "month": format_date,
    }
    return template.render(**data) + "\n"


def render_to_file(resume: dict, output: Path) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(resume), encoding="utf-8")
