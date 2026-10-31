# Fruita Tech Wizard site design guide

Design rules for fruitatechwizard.com, and the lessons behind them.
Dynamodal (dynamodal/dynamodal.github.io) follows the same technical rules with its own look and voice.

## Voice

- Fun, casual, friendly neighbor. Plain English, no jargon. Many readers are older or less comfortable with tech.
- Service area is Fruita only ("bike distance"). Not the whole Grand Valley.
- No set rates: pay what's fair, trades welcome.
- Don't advertise evenings or weekends.
- In person means a home, a business, a coffee shop or the library.
- Free help is a call or text only: "A quick 'is this a scam?' call or text is always free." Never free visits.
- Group talks are for "local community groups".
- The WTF-stickers story stays available (About page, footer link) but not front and center.
- Keep the FTW oval and the wizard dino.

## Look

| Token | Light | Dark | Use |
|---|---|---|---|
| `$cream` | `#fbf6ea` | `#1e1c25` | page background |
| `$sand` | `#f3e8ce` | `#272430` | bands, footer, open menu |
| `$ink` | `#2b2a33` | `#f2ede1` | text |
| `$purple` | `#4b3f9e` | `#b4a9ff` | links, buttons (wizard hat) |
| `$green` | `#3f7d1f` | `#8fcf6a` | icons (dino) |
| `$red` | `#a8401f` | `#f29470` | scam warnings |
| `$surface` | `#ffffff` | `#2a2733` | cards |
| `$line` | `#e6dcc3` | `#3a3646` | borders |

- Font: Nunito, 19px base (`118.75%`) for easier reading. Headings 800.
- Buttons are big (at least 3.2rem tall) with an icon and a word, for easy tapping.
- Icons: Bootstrap Icons, `<i class="bi bi-..." aria-hidden="true"></i>`.
- Building blocks in `html/styles.scss`: `ftw-hero`, `ftw-section`, `ftw-sand`, `ftw-wrap`, `ftw-grid`, `ftw-card`, `ftw-buttons`, `ftw-callout` (`-scam`, `-info`, `-green`), `ftw-note`, `ftw-not`.

## How the styles are built

- `html/styles.scss` holds every color as a `!default` variable plus all rules.
- `html/dark.scss` only overrides those variables (and a few dark-only rules). The dark theme loads it after `styles.scss`, so its values win.
- New colors go in both files as variables. Never hard-code a color in a rule, or dark mode breaks.
- `$font-size-root` is a percentage, not pixels, so the reader's own text-size setting still works.

## Mobile and large text

Most visitors are on phones, and many use very large text.
Android and iOS large text zooms the page, so a 390px phone acts like a 240px or even 200px wide screen.

- Every page must fit at 200px wide with no sideways scrolling. Check with the `check-layout` skill (`.claude/skills/check-layout/`).
- Grids use `minmax(min(260px, 100%), 1fr)`, never a bare `minmax(260px, 1fr)`, which overflows narrow screens.
- On phones, don't stack padding. Quarto's page grid already adds a 1.5em gutter, so `ftw-wrap` adds none below 576px, and cards and callouts use about 1rem of padding.
- The `ftw-sand` band runs edge to edge on phones by cancelling the gutter with `margin: 0 -1.5em`.
- Long words and links wrap (`overflow-wrap: anywhere` on links, cards, callouts and the footer). Headings hyphenate only below 340px.
- Below 340px the navbar hides the oval and lets "Fruita Tech Wizard" wrap instead of cutting it off.

## Navbar and menu

- The navbar starts with a "Home" link. Not everyone knows the logo goes home.
- Below 992px the navbar collapses into a menu. Search and the light/dark switch move into that menu (`html/mobile-menu.html`) so the top bar holds only the menu button and the full site name.
- The open menu has its own background, border and shadow so it doesn't blend into the page, and the menu button becomes an X.
- Hide individual tools in the top bar, not the whole `.quarto-navbar-tools` box. That empty box keeps the site name centered.

## Dark mode

- Quarto builds a light and a dark stylesheet. `respect-user-color-scheme: true` follows the visitor's system setting; the toggle (desktop) or menu item (phones) overrides it.
- The oval and dino images work on both backgrounds.
- Check every change in both modes.

## Search

- Quarto's built-in overlay search. It costs about 37 KB of compressed JavaScript per page (cached after the first visit); the index downloads only when someone searches.

## Search engines and AI assistants

- `site-url` is `https://fruitatechwizard.com` (www redirects there).
- `html/structured-data.html` describes FTW as a LocalBusiness in Fruita, CO, with phone, email and services, as JSON-LD on every page. Keep it in sync with the Services and Contact pages.
- Every page sets `description` in its front matter. It is for search results and link previews only (hidden on the page).
- The biggest wins for local search are off-site: Google Business Profile, Bing Places, the chamber listing and reviews.

## Checks before a PR

1. `quarto render`
2. `python3 .github/scripts/check_site.py _site https://fruitatechwizard.com https://www.fruitatechwizard.com` (also runs in CI on every PR)
3. The `check-layout` skill: no sideways scrolling at 390, 300, 240 and 200px, light and dark.

## Lessons learned

- Pandoc wraps a row of button links in a `<p>`, so `ftw-buttons` makes both itself and its `> p` the flex container.
- The jolla About template centers text; a `.quarto-about-jolla` override left-aligns it.
- An empty `.nav-footer-center` makes the footer columns stack; it is hidden.
- `url()` paths in SCSS resolve from the project root, not from the `html/` folder.
- Quarto's dark search highlight is too harsh; `dark.scss` softens it.
- The site name used to be cut off on phones by the navbar brand's max width; the mobile overrides at the end of `styles.scss` keep it whole.
