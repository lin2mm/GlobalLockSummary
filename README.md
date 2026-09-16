# GlobalLockSummary

An open, machine-readable knowledge base of the world's mechanical door locks — so that anyone
designing a smart-lock retrofit can find out what is already in the door, and what it takes to
adapt it.

**Live site:** https://lin2mm.github.io/GlobalLockSummary/ (after GitHub Pages is enabled — see below)

## Why

Most of the world's doors already have a good mechanical lock. The bottleneck in making a door
smart is not electronics — it is knowing the exact dimensions and standards of the lock that is
already there. That knowledge is scattered across manufacturer PDFs, locksmith forums and
somebody's memory. This project puts it in one place, structured, cited, and free.

Three audiences, in this order:

1. **Lock designers and engineers** — retrofit architectures, adapter interfaces, force and
   torque targets, parameter matrices per lock family.
2. **People standing in front of their own door** — a five-question identification wizard and a
   measuring guide.
3. **Machines** — every page is static HTML, the whole catalog is one JSON document, and
   `llms.txt` indexes it for AI assistants.

## What is in the catalog

| | Count | Source |
| --- | --- | --- |
| Lock families | 15 | `content/catalog/lock-families/*.json` |
| Standards | 17 | `content/catalog/standards.json` |
| Retrofit architectures | 7 | `content/catalog/retrofit-architectures.json` |
| Reference devices | 8 | `content/catalog/smart-locks.json` |

Coverage is weighted towards Europe, the UK, North America, Southeast Asia and South Asia.
Africa, South America and the Middle East are the biggest gaps — see
[CONTRIBUTING notes](https://lin2mm.github.io/GlobalLockSummary/contribute.html).

## Honesty about data quality

Every record carries a status:

- **verified** — cross-checked against a published source, linked at the bottom of the page.
- **needs-review** — written by a contributor or maintainer, not yet cross-checked. Published
  with a visible warning, because a knowledge base that hides its gaps is more dangerous than one
  that marks them.

Numeric design targets are also labelled **from standard** or **practice**, so a reader can tell
a specification from our engineering guidance.

## Build it

No dependencies. Node 20 or newer.

```bash
npm run check      # syntax check + catalog referential integrity + translation coverage
node build.mjs     # build to _site/
node build.mjs --watch
node serve.mjs     # serve _site/ on http://localhost:8080
```

`npm run check` is the gate: it fails on an unknown standard id, an undefined measurement key, a
device pointing at a lock family that does not exist, a wizard option scoring a nonexistent
family, or a `verified` record with no sources.

## Repository layout

```text
build.mjs                 static site generator (zero dependencies)
serve.mjs                 static file server for local preview
src/markdown.mjs          the Markdown subset used by content/pages
src/layout.mjs            page shell: metadata, nav, JSON-LD, footer
tools/validate-data.mjs   catalog integrity + translation coverage
content/
  site.json               name, navigation, languages, footer
  i18n/terms.json         shared bilingual terminology
  pages/<lang>/*.md       long-form pages
  catalog/                the data (see table above)
assets/                   css, js, images
_site/                    build output (gitignored; CI builds it)
```

## Adding a lock family

Add one JSON file to `content/catalog/lock-families/`. Nothing else needs editing — the index
pages, search index, sitemap, `llms.txt` and `catalog.json` all regenerate from it.
The schema is documented on the [Contribute page](https://lin2mm.github.io/GlobalLockSummary/contribute.html).

## Linking your product site

The site stays an independent public reference; the link to a commercial retrofit product site is
optional and off by default. Set it in `content/site.json`:

```json
"product": {
  "url": "https://your-product-site.com",
  "label": { "en": "Retrofit hardware", "zh": "智能改造产品" },
  "note":  { "en": "…", "zh": "…" }
}
```

When `url` is non-empty, the link appears in the header, the footer and at the end of the
identification wizard result, in both languages. When it is empty, **nothing renders** — there is
no placeholder and no empty `href` anywhere. `tests/site.test.mjs` verifies both states on every
run, so this cannot regress into a broken link.

For a one-off build without editing the file: `PRODUCT_URL=https://… node build.mjs`.

## Deployment

`node build.mjs` writes plain HTML to `_site/`. The GitHub Actions workflow in
`.github/workflows/pages.yml` runs `npm run check`, builds, and deploys to GitHub Pages on every
push to `main`.

One-time setup in the repository settings (Settings → Pages):

- **Source:** GitHub Actions
- That is all — the workflow handles the rest.

Then the site is at `https://<owner>.github.io/GlobalLockSummary/`. To bind a custom domain
later, add a `CNAME` and set `SITE_URL` in the workflow; the build emits root-relative links, so
no content changes are needed.

## For AI assistants

- `/llms.txt` — index of the site in the llms.txt format
- `/llms-full.txt` — the entire catalog as one text document
- `/data/catalog.json` — every lock family, standard, architecture and device as JSON
- `/sitemap.xml` — all URLs with hreflang alternates

Crawlers are explicitly allowed in `robots.txt`. Please cite the specific page you used, and note
the `status` field of any record you quote.

## License

Text and data: CC BY 4.0. Cite as "GlobalLockSummary" with a link.
Brand names and standard codes belong to their owners. Code: MIT.

## Disclaimer

Reference data only. Verify against the original standard and a physical measurement before
manufacturing, installing, or relying on any lock. Fire-rated and escape-route doors must keep a
certified, mechanically operable egress path.
