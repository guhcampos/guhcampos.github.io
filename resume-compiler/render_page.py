#!/usr/bin/env python3
"""Driver for the vendored HTML renderer slice.

Renders the committed schema snapshot (schema.yaml) into a self-contained
deterministic index.html. Byte-identical to what the canonical compiler in
the resume-compiler repository produces for the same schema.

Usage: python render_page.py --schema schema.yaml --output index.html
"""

from __future__ import annotations

import argparse
from pathlib import Path

from resume_compiler import render_html
from resume_compiler import schema as schema_mod


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    schema_text = Path(args.schema).read_text(encoding="utf-8")
    resume = schema_mod.load_schema_text(schema_text)
    if not isinstance(resume, dict):
        parser.error(f"invalid schema file: {args.schema}")
    render_html.render_to_file(resume, Path(args.output))
    print(f"html written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
