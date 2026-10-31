#!/usr/bin/env python3
"""Check a rendered Quarto site for broken internal links and bad structured data.

Usage: python3 .github/scripts/check_site.py _site https://example.com

- Every internal href/src (relative, root-relative, or on the site's own
  domain) must point to a file that exists in the rendered site.
- Every <script type="application/ld+json"> block must be valid JSON.

External links are not fetched, so the check never fails because some
other website is slow or blocks bots.
"""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.jsonld = []
        self._in_jsonld = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_jsonld = True
            self.jsonld.append("")

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_jsonld = False

    def handle_data(self, data):
        if self._in_jsonld:
            self.jsonld[-1] += data


def main():
    site = Path(sys.argv[1]).resolve()
    hosts = {urlparse(u).netloc for u in sys.argv[2:]}
    errors = []
    pages = {}
    for page in sorted(site.rglob("*.html")):
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        pages[page] = parser

    for page, parser in pages.items():
        rel = page.relative_to(site)
        for i, block in enumerate(parser.jsonld):
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                errors.append(f"{rel}: invalid JSON-LD block {i + 1}: {e}")

        for link in parser.links:
            u = urlparse(link)
            if u.scheme in ("mailto", "tel", "sms", "data", "javascript"):
                continue
            if u.scheme in ("http", "https"):
                if u.netloc not in hosts:
                    continue  # external link: not checked
                path = u.path
                base = site
            elif u.scheme or u.netloc:
                continue
            else:
                path = u.path
                base = site if path.startswith("/") else page.parent
            if not path:
                target = page  # same-page anchor
            else:
                target = (base / unquote(path).lstrip("/")).resolve()
                if target.is_dir() or path.endswith("/"):
                    target = target / "index.html"
            if not target.is_file() or site not in (target, *target.parents):
                errors.append(f"{rel}: broken link {link}")
            elif u.fragment and target in pages and u.fragment not in pages[target].ids:
                errors.append(f"{rel}: missing anchor {link}")

    print(f"Checked {len(pages)} pages.")
    for e in errors:
        print(f"::error::{e}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
