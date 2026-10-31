---
name: check-layout
description: Check the rendered site for mobile layout problems (sideways scrolling, cut-off text) at normal and very large text sizes, in light and dark mode, and save screenshots to review. Use after any change to styles, navbar, cards, or page content, and before opening a PR.
---

# Check layout

1. Render the site: `quarto render`
2. Run the check from the repo root:
   `node .claude/skills/check-layout/check_layout.js`
3. Fix anything it reports. Every page must fit at 200px wide with no sideways scrolling.
4. Look at the screenshots in `_layout-check/` (gitignored), at least the home page at 390px and 200px in both color schemes.
   Check for things the script can't catch: cramped cards, text that is hard to read in dark mode, a menu that blends into the page.
5. Run the link and structured data check too:
   `python3 .github/scripts/check_site.py _site <site-url>`

Widths: 390px is a typical phone.
300, 240 and 200px are the same phone with larger and larger text, because Android and iOS large text zooms the page.

See `DESIGN.md` for the rules these checks enforce and why.
