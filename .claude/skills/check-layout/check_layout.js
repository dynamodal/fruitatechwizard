// Layout check for the rendered site in _site/.
//
// Serves _site/ locally, opens every page at phone widths that match normal
// and very large text sizes, in light and dark mode, and reports any page that
// scrolls sideways. Saves screenshots to _layout-check/ for a visual review.
//
// Usage (from the repo root, after `quarto render`):
//   node .claude/skills/check-layout/check_layout.js
//
// Needs Playwright with Chromium (`npm install playwright` and
// `npx playwright install chromium` if they aren't already available).

const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const SITE = path.resolve("_site");
const OUT = path.resolve("_layout-check");
// 390 = typical phone; 300/240/200 = the same phone with larger and larger
// text (Android and iOS large text zooms the page, shrinking the CSS width).
const WIDTHS = [390, 300, 240, 200];
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript",
  ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png",
  ".jpg": "image/jpeg", ".webp": "image/webp", ".woff": "font/woff", ".woff2": "font/woff2" };

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p.endsWith("/")) p += "index.html";
  const file = path.join(SITE, p);
  if (!file.startsWith(SITE) || !fs.existsSync(file)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
  fs.createReadStream(file).pipe(res);
});

(async () => {
  await new Promise((r) => server.listen(0, r));
  const base = `http://localhost:${server.address().port}`;
  const pages = fs.readdirSync(SITE).filter((f) => f.endsWith(".html"));
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  let problems = 0;

  for (const scheme of ["light", "dark"]) {
    for (const width of WIDTHS) {
      const ctx = await browser.newContext({ viewport: { width, height: 800 }, colorScheme: scheme });
      const page = await ctx.newPage();
      for (const name of pages) {
        await page.goto(`${base}/${name}`, { waitUntil: "networkidle" });
        const result = await page.evaluate(() => {
          const W = document.documentElement.clientWidth;
          const culprits = [...document.querySelectorAll("body *")]
            .filter((e) => e.scrollWidth > e.clientWidth + 1 && e.clientWidth > 0 &&
              getComputedStyle(e).overflowX === "visible" && !e.closest(".navbar-collapse:not(.show)"))
            .slice(-3)
            .map((e) => `${e.tagName.toLowerCase()} "${e.textContent.trim().slice(0, 40)}"`);
          return { scroll: document.documentElement.scrollWidth, width: W, culprits };
        });
        if (result.scroll > result.width) {
          problems++;
          console.log(`✗ ${name} at ${width}px (${scheme}): page is ${result.scroll}px wide`);
          result.culprits.forEach((c) => console.log(`    ${c}`));
        }
        await page.screenshot({ path: path.join(OUT, `${name.replace(".html", "")}-${width}-${scheme}.png`) });
      }
      await ctx.close();
    }
  }

  await browser.close();
  server.close();
  console.log(problems ? `\n${problems} problem(s). Screenshots in _layout-check/` :
    `No sideways scrolling on ${pages.length} pages. Screenshots in _layout-check/`);
  process.exit(problems ? 1 : 0);
})();
