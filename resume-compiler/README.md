# Resume page — vendored HTML renderer slice

Static output powering `https://guhcampos.github.io/resume/`.

## Provenance

**Canonical source:** the `resume-compiler` project
(`~/workspace/guhcampos/resume-compiler`, career board task
"Resume compiler - schema and Obsidian extraction"). Only its committed
HTML-render slice is vendored here so the site workflow can regenerate the
page without extra credentials or checkouts:

- `src/resume_compiler/schema.py` — Schema v1 load/skeleton (verbatim copy)
- `src/resume_compiler/render_html.py` — Schema v1 → deterministic HTML (verbatim copy)
- `src/resume_compiler/templates/resume.html.j2` — page template (verbatim copy)
- `render_page.py` — thin driver: `schema.yaml` → `index.html`
- `schema.yaml` — generated Schema v1 snapshot of the current resume content

`schema.yaml` is produced by the canonical compiler:

```bash
cd ~/workspace/guhcampos/resume-compiler
uv run resume-compiler build --schema-out <site>/resume-compiler/schema.yaml /tmp/ignore.html
```

For the same `schema.yaml`, this slice renders **byte-identical** output to
the canonical compiler (verified: sha256 `9651926a…` across both).

## Pipeline

`.github/workflows/hugo.yml` (this repo) on every build:

1. renders `resume-compiler/schema.yaml` → `hugo/static/resume/index.html`,
2. Hugo copies it verbatim to `public/resume/index.html` (deployed URL
   `https://guhcampos.github.io/resume/`),
3. commits the regenerated `hugo/static/resume/index.html` when it changed
   (the page is never hand-edited; the commit history is the audit trail).
   Note: any `static/` directory is gitignored in this repo — the workflow
   force-adds (`git add -f`) the rendered file so the output stays tracked.

## Update rules

- **Never hand-edit** rendered output (`index.html` is compiler output, a
  superset of Schema v1). Fix the schema or the template in the canonical
  compiler, then re-sync and push.
- When the canonical HTML-render slice changes, copy the three verbatim
  files into `src/resume_compiler/` again (plus a fresh `schema.yaml` when
  content changed) and push.
- Renderer deps are minimal and pinned at runtime by the workflow for this
  slice: `pyyaml>=6`, `jinja2>=3.1` (canonical `pyproject.toml` ranges).
