---
title: Contribute
description: How to add a lock family, a standard or a correction to GlobalLockSummary — one JSON record per lock, the data schema, and what makes a record verifiable.
---

This catalog grows by people who have measured a real lock writing down what they found. The most valuable contribution is not a big one — it is one lock family from a country we have not covered, with numbers and a photo.

## The fastest contribution

Open an issue with:

1. Country and city
2. What the door is (timber, uPVC, metal gate, glass)
3. Backset, centre distance, faceplate size, door thickness
4. A photo of the door edge with a ruler in frame
5. Whether the door is fire-rated

That is enough for a maintainer to create the record. If you would rather write the record yourself, the instructions are below.

## Repository layout

```text
content/
  site.json                 site name, navigation, languages, footer text
  i18n/terms.json           shared bilingual terminology — add a term once
  pages/<lang>/*.md         long-form pages, one folder per language
  catalog/
    lock-families/*.json    one file per lock family
    standards.json          all standards in one file
    retrofit-architectures.json
    smart-locks.json        reference devices
    decision-tree.json      the identification wizard's questions
```

Adding a lock family is adding one JSON file. Nothing else needs editing — the index pages, the search index, the sitemap and `llms.txt` all regenerate from it.

## The lock family schema

```json
{
  "id": "kebab-case-unique-id",
  "status": "verified | needs-review",
  "regions": ["Country", "..."],
  "title": { "en": "...", "zh": "..." },
  "summary": { "en": "...", "zh": "..." },
  "anatomy": { "en": ["..."], "zh": ["..."] },
  "measurements": [
    {
      "key": "backset",
      "typical": "55 mm, 60 mm",
      "tolerance": "±1 mm",
      "how": { "en": "Door edge to keyhole centre.", "zh": "..." }
    }
  ],
  "measureOrder": ["backset", "centreDistance"],
  "standards": ["din-18251"],
  "retrofit": { "architectures": ["motor-on-thumbturn"], "notes": { "en": "...", "zh": "..." } },
  "faq": { "en": [{ "q": "...", "a": "..." }], "zh": [] },
  "sources": [{ "title": "...", "url": "https://..." }]
}
```

The `key` values in `measurements` must exist in `content/i18n/terms.json` under `measurements` — that is how the label gets translated once instead of per record. `npm run check` fails the build if you use a key that does not exist.

## Status is not optional

- **verified** — the numbers were cross-checked against a published source, which is linked in `sources`. Datasheets, standard documents and manufacturer specifications count. A forum post does not.
- **needs-review** — anything else, including anything you measured yourself but nobody has confirmed. This is published with a visible warning, and it is much better than the record not existing.

Never mark something verified without a link. The whole value of this site is that a reader can check it.

## Writing for the two audiences

Every record is read by a homeowner and by a mechanical engineer, often in that order. Keep the summary in plain language and the measurements precise. If a number matters, give the tolerance — a dimension without a tolerance is not a specification.

## Translations

Content is bilingual (English and 中文) today. The structure is designed to grow: data lives in JSON with per-language fields, and shared vocabulary lives in `terms.json`, so machine translation later can work on terminology rather than prose.

If you add a language, create `content/pages/<lang>/` and add the language to `content/site.json` under `languages`, `navigation` and the UI strings. Nothing in the build needs changing.

## Running it locally

```bash
node build.mjs            # build to _site/
node build.mjs --watch    # rebuild on change
node serve.mjs            # serve _site/ on http://localhost:8080
npm run check             # syntax + referential integrity of the catalog data
```

No dependencies to install. Node 20 or newer.

## What is most wanted right now

1. **Africa, South America, India, the Middle East** — no lock families at all yet
2. **Australia** — the standard designation needs confirming
3. **Japan** — case dimensions and the applicable JIS reference
4. **Photos with rulers** — for every family, so the identification wizard can show them
5. **Adapter teardowns** — measured clamp ranges and turn-piece profiles, which no manufacturer publishes
