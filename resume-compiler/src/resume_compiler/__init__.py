"""Resume compiler core.

Modules:
- extract.py     : Obsidian vault -> schema dict (Schema v1)
- schema.py      : schema skeleton + deterministic (de)serialization
- render_html.py : schema dict -> self-contained deterministic index.html
- validate.py    : completeness checks over the vault
"""
