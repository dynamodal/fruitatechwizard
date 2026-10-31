# Fruita Tech Wizard website

Quarto website for fruitatechwizard.com, Thomas Wells's local tech help side business in Fruita, Colorado.
A GitHub Actions workflow renders and publishes it to the `gh-pages` branch on every push to `main`.

Read `DESIGN.md` before changing styles, layout, navigation or copy. Its Voice section lists business rules (service area, pricing, what's free) that copy must follow.

## Conventions

- Prose in `.qmd` files: one sentence per line.
- Colors live in `html/styles.scss` (light, `!default`) and `html/dark.scss` (dark). No hard-coded colors in rules.
- Work on a branch and open a PR. The **Check site** workflow must pass.

## Commands

- Preview: `quarto preview`
- Build: `quarto render`
- Links and structured data: `python3 .github/scripts/check_site.py _site https://fruitatechwizard.com https://www.fruitatechwizard.com`
- Mobile and large-text layout: `node .claude/skills/check-layout/check_layout.js`
