#!/usr/bin/env python3
"""Add a version banner to each standalone explorer in the rendered site.

Quarto runs this after every render (post-render in _quarto.yml).

Standalone explorers are self-contained HTML files kept as-is in the repo,
one folder per version:

    community/<project>/v1/index.html
    community/<project>/v2/index.html
    ...

The highest number is the latest. Each copy in _site gets a slim bar at the
top that names its version and links to the project page (with all versions).
Older versions also link to the latest, so a shared old link doesn't pass for
the current numbers. The files in the repo are never changed.
"""
import os
import re
from pathlib import Path

START = "<!-- ftw-explorer-banner -->"
END = "<!-- /ftw-explorer-banner -->"

STYLE = """<style>
#ftw-explorer-banner{--ftw-b-bg:#eeecf8;--ftw-b-fg:#2b2a33;--ftw-b-link:#4b3f9e;--ftw-b-old-bg:#fbeee8;--ftw-b-old-fg:#a8401f;
  background:var(--ftw-b-bg);color:var(--ftw-b-fg);font:15px/1.4 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  padding:8px 16px;display:flex;flex-wrap:wrap;gap:4px 14px;justify-content:center;text-align:center;overflow-wrap:anywhere}
#ftw-explorer-banner a{color:var(--ftw-b-link);font-weight:700}
#ftw-explorer-banner.old{background:var(--ftw-b-old-bg)}
#ftw-explorer-banner.old b{color:var(--ftw-b-old-fg)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) #ftw-explorer-banner{--ftw-b-bg:#2a2733;--ftw-b-fg:#f2ede1;--ftw-b-link:#b4a9ff;--ftw-b-old-bg:#3a2620;--ftw-b-old-fg:#f29470}}
:root[data-theme="dark"] #ftw-explorer-banner{--ftw-b-bg:#2a2733;--ftw-b-fg:#f2ede1;--ftw-b-link:#b4a9ff;--ftw-b-old-bg:#3a2620;--ftw-b-old-fg:#f29470}
</style>"""


def banner(n, latest):
    if n == latest:
        body = (f"<span>Version {n}, the latest</span>"
                '<a href="../">About this explorer and earlier versions</a>')
        cls = ""
    else:
        body = (f"<span><b>Older version ({n} of {latest})</b></span>"
                f'<a href="../v{latest}/">Open the latest version</a>'
                '<a href="../">All versions</a>')
        cls = ' class="old"'
    return f'{START}\n{STYLE}\n<div id="ftw-explorer-banner"{cls} role="note">{body}</div>\n{END}'


def main():
    site = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
    for project in sorted(p for p in site.glob("community/*") if p.is_dir()):
        versions = {}
        for page in project.glob("v*/index.html"):
            m = re.fullmatch(r"v(\d+)", page.parent.name)
            if m:
                versions[int(m.group(1))] = page
        if not versions:
            continue
        latest = max(versions)
        for n, page in versions.items():
            html = page.read_text(encoding="utf-8")
            # Drop a banner left by an earlier render (the latest may have changed)
            html = re.sub("\n?" + re.escape(START) + ".*?" + re.escape(END) + "\n?", "", html, flags=re.S)
            html, count = re.subn(r"<body[^>]*>", lambda m: m.group(0) + "\n" + banner(n, latest) + "\n", html, count=1)
            if count:
                page.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
