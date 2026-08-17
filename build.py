#!/usr/bin/env python3
"""
Bundles src/ into a single index.html that GitHub Pages can serve directly.

    python build.py            build index.html once
    python build.py --serve    build, then serve at http://localhost:8000
                               (rebuilds on every page refresh)

How it works
------------
src/page.html is the shell. Four placeholders get filled in:

    <!--{styles}-->    every src/styles/*.css, then each section's .css
    <!--{nav}-->       one <a> per section that has a data-nav attribute
    <!--{sections}-->  each section's .html, in folder order
    <!--{scripts}-->   every src/scripts/*.js

Sections live in src/sections/<NN-name>/ and are ordered by folder name.
A folder whose name starts with "_" is skipped — that's how a section is
turned off without deleting it.

Nothing here needs installing. Standard library only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "index.html"

COMMENTS = re.compile(r"<!--.*?-->", re.S)
TAG = re.compile(r"<[a-zA-Z][^>]*>")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").rstrip() + "\n"


def sections() -> list[Path]:
    """Enabled section folders, in page order."""
    if not (SRC / "sections").is_dir():
        sys.exit("error: src/sections/ not found")
    return sorted(
        d for d in (SRC / "sections").iterdir()
        if d.is_dir() and not d.name.startswith(("_", "."))
    )


def nav_entry(html: str, folder: str):
    """Pull (href, label) out of the section's root tag, if it opted into the nav."""
    for tag in TAG.findall(COMMENTS.sub("", html)):
        label = re.search(r'\sdata-nav\s*=\s*"([^"]+)"', tag)
        if not label:
            continue
        ident = re.search(r'\sid\s*=\s*"([^"]+)"', tag)
        if not ident:
            sys.exit(f'error: {folder} has data-nav="{label.group(1)}" but no id="..."')
        return f"#{ident.group(1)}", label.group(1)
    return None


def indent_into(page: str, token: str, block: str) -> str:
    """Replace <!--{token}--> with block, matching the placeholder's indentation."""
    marker = "<!--{%s}-->" % token
    for line in page.splitlines():
        if marker in line:
            pad = line[: len(line) - len(line.lstrip())]
            body = "\n".join(pad + ln if ln.strip() else ln for ln in block.splitlines())
            return page.replace(line, body, 1)
    sys.exit(f"error: src/page.html is missing the {marker} placeholder")


def build() -> None:
    page = read(SRC / "page.html")

    styles = [f"/* ---------- {p.relative_to(SRC)} ---------- */\n{read(p)}"
              for p in sorted((SRC / "styles").glob("*.css"))]
    scripts = [f"// ---------- {p.relative_to(SRC)} ----------\n{read(p)}"
               for p in sorted((SRC / "scripts").glob("*.js"))]

    bodies, navs, used_ids = [], [], set()

    for folder in sections():
        html_files = sorted(folder.glob("*.html"))
        if not html_files:
            print(f"  skip  {folder.name}  (no .html file)")
            continue

        html = "\n".join(read(f) for f in html_files)
        bodies.append(html)
        styles += [f"/* ---------- sections/{folder.name}/{p.name} ---------- */\n{read(p)}"
                   for p in sorted(folder.glob("*.css"))]
        scripts += [read(p) for p in sorted(folder.glob("*.js"))]

        entry = nav_entry(html, folder.name)
        if entry:
            href, label = entry
            if href in used_ids:
                sys.exit(f"error: duplicate section id {href} (in {folder.name})")
            used_ids.add(href)
            navs.append(f'<a href="{href}">{label}</a>')
            print(f"  ok    {folder.name}  →  nav: {label}")
        else:
            print(f"  ok    {folder.name}")

    page = indent_into(page, "styles", "\n".join(styles))
    page = indent_into(page, "nav", "\n".join(navs))
    page = indent_into(page, "sections", "\n\n".join(bodies))
    page = indent_into(page, "scripts", "\n".join(scripts))

    OUT.write_text(page, encoding="utf-8")
    print(f"\nwrote {OUT.name}  ({len(page) / 1024:.1f} KB, {len(bodies)} sections)")

    if not (ROOT / "assets" / "resume.pdf").exists():
        print("note: assets/resume.pdf is missing — the Résumé button will 404.")


def serve(port: int = 8000) -> None:
    import functools
    import http.server

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path in ("/", "/index.html"):
                build()
            super().do_GET()

        def log_message(self, *a):
            pass

    handler = functools.partial(Handler, directory=str(ROOT))
    print(f"\nserving http://localhost:{port}  —  refresh to rebuild, Ctrl-C to stop")
    try:
        http.server.ThreadingHTTPServer(("", port), handler).serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        serve()
