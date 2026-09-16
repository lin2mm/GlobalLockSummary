/**
 * Catalog data validation.
 *
 * `npm run check` runs this after syntax-checking the build scripts. It exists
 * because the catalog is edited by contributors as plain JSON: a typo in a
 * standard id or a measurement key silently produces a broken page, and nothing
 * else in the build would notice.
 *
 * Errors fail the build. Warnings are printed but allowed, because an
 * incomplete record is still more useful than no record.
 */

import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const CONTENT = join(ROOT, 'content');

const readJson = (p) => JSON.parse(readFileSync(p, 'utf8'));

const errors = [];
const warnings = [];
const err = (msg) => errors.push(msg);
const warn = (msg) => warnings.push(msg);

const site = readJson(join(CONTENT, 'site.json'));
const terms = readJson(join(CONTENT, 'i18n', 'terms.json'));
const archDoc = readJson(join(CONTENT, 'catalog', 'retrofit-architectures.json'));
const stdDoc = readJson(join(CONTENT, 'catalog', 'standards.json'));
const devDoc = readJson(join(CONTENT, 'catalog', 'smart-locks.json'));
const tree = readJson(join(CONTENT, 'catalog', 'decision-tree.json'));

const FAMILIES_DIR = join(CONTENT, 'catalog', 'lock-families');
const families = readdirSync(FAMILIES_DIR).filter((f) => f.endsWith('.json'))
  .map((f) => ({ file: f, data: readJson(join(FAMILIES_DIR, f)) }));

const familyIds = new Set(families.map((f) => f.data.id));
const archIds = new Set(archDoc.architectures.map((a) => a.id));
const stdIds = new Set(stdDoc.standards.map((s) => s.id));
const devIds = new Set(devDoc.devices.map((d) => d.id));

const STATUS = new Set(['verified', 'needs-review']);
const measurementKeys = new Set(Object.keys(terms.measurements || {}));
const archTermKeys = new Set(Object.keys(terms.architecture || {}));

const hasLang = (obj, field, where) => {
  if (!obj) return err(`${where}: missing ${field}`);
  if (!obj.en) err(`${where}: ${field} has no English text`);
  if (!obj.zh) warn(`${where}: ${field} has no Chinese text`);
};

/* ---------------- lock families ---------------- */

const seenFamilyIds = new Set();
for (const { file, data } of families) {
  const where = `lock-families/${file}`;
  if (!data.id) { err(`${where}: missing id`); continue; }
  if (seenFamilyIds.has(data.id)) err(`${where}: duplicate id "${data.id}"`);
  seenFamilyIds.add(data.id);
  if (!file.startsWith(data.id)) warn(`${where}: filename does not match id "${data.id}"`);
  if (!STATUS.has(data.status)) err(`${where}: status must be verified or needs-review, got "${data.status}"`);
  if (!Array.isArray(data.regions) || !data.regions.length) err(`${where}: regions must be a non-empty array`);

  hasLang(data.title, 'title', where);
  hasLang(data.summary, 'summary', where);

  if (data.status === 'verified' && !(data.sources || []).length) {
    err(`${where}: status is verified but there are no sources to check it against`);
  }
  for (const src of data.sources || []) {
    if (!src.url || !/^https?:\/\//.test(src.url)) err(`${where}: source has no valid url`);
  }

  const keys = new Set();
  for (const m of data.measurements || []) {
    if (!measurementKeys.has(m.key)) {
      err(`${where}: measurement key "${m.key}" is not defined in content/i18n/terms.json`);
    }
    if (keys.has(m.key)) warn(`${where}: measurement "${m.key}" listed twice`);
    keys.add(m.key);
    if (!m.typical) err(`${where}: measurement "${m.key}" has no typical value`);
    if (!m.how?.en) err(`${where}: measurement "${m.key}" has no English how-to`);
    if (!m.how?.zh) warn(`${where}: measurement "${m.key}" has no Chinese how-to`);
  }

  for (const k of data.measureOrder || []) {
    if (!keys.has(k)) err(`${where}: measureOrder references "${k}", which is not in measurements`);
  }

  for (const s of data.standards || []) {
    if (!stdIds.has(s)) err(`${where}: unknown standard id "${s}"`);
  }

  if (!data.retrofit) {
    err(`${where}: missing retrofit section`);
  } else {
    if (!Array.isArray(data.retrofit.architectures)) {
      err(`${where}: retrofit.architectures must be an array (use [] when there is no clean path)`);
    } else {
      for (const a of data.retrofit.architectures) {
        if (!archIds.has(a)) err(`${where}: unknown retrofit architecture "${a}"`);
      }
      if (!data.retrofit.architectures.length && !data.retrofit.notes?.en) {
        err(`${where}: no retrofit architectures listed and no note explaining why`);
      }
    }
  }

  for (const faq of (data.faq?.en || [])) {
    if (!faq.q || !faq.a) err(`${where}: FAQ entry needs both q and a`);
  }
}

/* ---------------- standards ---------------- */

const seenStd = new Set();
for (const s of stdDoc.standards) {
  const where = `standards.json/${s.id}`;
  if (seenStd.has(s.id)) err(`${where}: duplicate id`);
  seenStd.add(s.id);
  if (!s.code) err(`${where}: missing code`);
  if (!STATUS.has(s.status)) err(`${where}: status must be verified or needs-review, got "${s.status}"`);
  hasLang(s.title, 'title', where);
  hasLang(s.scope, 'scope', where);
  hasLang(s.whyItMattersForRetrofit, 'whyItMattersForRetrofit', where);
  if (!(s.decides?.en || []).length) err(`${where}: decides must list at least one item in English`);
  for (const f of s.appliesTo || []) {
    if (!familyIds.has(f)) err(`${where}: appliesTo references unknown lock family "${f}"`);
  }
  if (s.status === 'verified' && !(s.sources || []).length) {
    err(`${where}: status is verified but there are no sources`);
  }
}

/* ---------------- retrofit architectures ---------------- */

const seenArch = new Set();
for (const a of archDoc.architectures) {
  const where = `retrofit-architectures.json/${a.id}`;
  if (seenArch.has(a.id)) err(`${where}: duplicate id`);
  seenArch.add(a.id);
  if (!archTermKeys.has(a.id)) err(`${where}: id "${a.id}" has no entry in terms.architecture (needed for the label)`);
  hasLang(a.principle, 'principle', where);
  if (typeof a.difficulty !== 'number' || a.difficulty < 1 || a.difficulty > 4) {
    err(`${where}: difficulty must be a number from 1 to 4`);
  }
  if (typeof a.doorUntouched !== 'boolean') err(`${where}: doorUntouched must be true or false`);
  if (typeof a.keepsMechanicalKey !== 'boolean') err(`${where}: keepsMechanicalKey must be true or false`);

  for (const f of a.worksWith || []) {
    if (!familyIds.has(f)) err(`${where}: worksWith references unknown lock family "${f}"`);
  }
  if (!(a.worksWith || []).length) err(`${where}: worksWith must name at least one lock family`);

  for (const k of a.requiredMeasurements || []) {
    if (!measurementKeys.has(k)) err(`${where}: requiredMeasurements has unknown key "${k}"`);
  }
  for (const iface of a.adapterInterfaces || []) {
    if (!iface.en) err(`${where}: adapter interface has no English text`);
    if (!iface.zh) warn(`${where}: adapter interface has no Chinese text`);
  }
  for (const target of a.targets || []) {
    if (!target.label?.en) err(`${where}: design target has no English label`);
    if (!target.value) err(`${where}: design target "${target.label?.en}" has no value`);
    if (!['standard', 'practice'].includes(target.basis)) {
      err(`${where}: design target "${target.label?.en}" basis must be "standard" or "practice"`);
    }
  }
  if (!(a.designChecklist?.en || []).length) err(`${where}: designChecklist must have at least one item`);
  for (const ex of a.examples || []) {
    if (!devIds.has(ex)) err(`${where}: examples references unknown device "${ex}"`);
  }
}

/* ---------------- devices ---------------- */

const seenDev = new Set();
for (const d of devDoc.devices) {
  const where = `smart-locks.json/${d.id}`;
  if (seenDev.has(d.id)) err(`${where}: duplicate id`);
  seenDev.add(d.id);
  if (!d.name) err(`${where}: missing name`);
  if (!archIds.has(d.architecture)) err(`${where}: unknown architecture "${d.architecture}"`);
  if (!STATUS.has(d.status)) err(`${where}: status must be verified or needs-review, got "${d.status}"`);
  if (!d.checkedOn) err(`${where}: missing checkedOn date`);
  if (!(d.fits || []).length) err(`${where}: fits must name at least one lock family`);
  for (const f of d.fits || []) {
    if (!familyIds.has(f)) err(`${where}: fits references unknown lock family "${f}"`);
  }
  if (!(d.keyConstraints?.en || []).length) err(`${where}: keyConstraints must have at least one item in English`);
}

/* ---------------- decision tree ---------------- */

if (!(tree.questions || []).length) err('decision-tree.json: no questions');
for (const q of tree.questions || []) {
  const where = `decision-tree.json/${q.id}`;
  if (!q.prompt?.en) err(`${where}: missing English prompt`);
  if (!q.prompt?.zh) warn(`${where}: missing Chinese prompt`);
  if (!(q.options || []).length) err(`${where}: no options`);
  for (const o of q.options || []) {
    if (!o.label?.en) err(`${where}: option "${o.id}" has no English label`);
    for (const famId of Object.keys(o.add || {})) {
      if (!familyIds.has(famId)) err(`${where}: option "${o.id}" scores unknown lock family "${famId}"`);
      if (typeof o.add[famId] !== 'number' || o.add[famId] <= 0) {
        err(`${where}: option "${o.id}" score for "${famId}" must be a positive number`);
      }
    }
  }
}

/* Every family should be reachable from the wizard, or it cannot be identified. */
const reachable = new Set();
for (const q of tree.questions || []) {
  for (const o of q.options || []) {
    for (const famId of Object.keys(o.add || {})) reachable.add(famId);
  }
}
for (const id of familyIds) {
  if (!reachable.has(id)) warn(`decision-tree.json: lock family "${id}" can never be identified by the wizard`);
}

/* ---------------- site config ---------------- */

const langs = Object.keys(site.languages || {});
if (!langs.includes(site.defaultLang)) err('site.json: defaultLang is not one of languages');
for (const lang of langs) {
  if (!(site.navigation[lang] || []).length) err(`site.json: navigation has no entries for "${lang}"`);
  for (const item of site.navigation[lang] || []) {
    if (!item.label || !item.href) err(`site.json: navigation item for "${lang}" needs label and href`);
  }
  if (!site.description[lang]) warn(`site.json: no description for "${lang}"`);
}
for (const lang of langs) {
  const dir = join(CONTENT, 'pages', lang);
  let found = 0;
  try { found = readdirSync(dir).filter((f) => f.endsWith('.md')).length; } catch { found = 0; }
  if (!found) err(`site.json declares language "${lang}" but content/pages/${lang}/ has no markdown pages`);
}

/* ---------------- translation coverage ---------------- */

/**
 * Measurement values may be a plain string (English only) or { en, zh }.
 * A plain string is legal — but on a bilingual site it means the Chinese page
 * shows an English value, so the gap is counted and reported rather than hidden.
 */
const needsLangs = Object.keys(site.languages || {}).filter((l) => l !== 'en');
let valueFields = 0;
let untranslated = 0;
const untranslatedByFamily = [];
for (const { data } of families) {
  let count = 0;
  for (const m of data.measurements || []) {
    for (const field of ['typical', 'tolerance']) {
      const v = m[field];
      if (v === undefined) continue;
      valueFields++;
      if (typeof v === 'string') { untranslated++; count++; continue; }
      for (const lang of needsLangs) {
        if (!v[lang]) { untranslated++; count++; }
      }
    }
  }
  if (count) untranslatedByFamily.push(`${data.id} (${count})`);
}

/* ---------------- report ---------------- */

const summary = [
  `${families.length} lock families, ${stdDoc.standards.length} standards, ${archDoc.architectures.length} retrofit architectures, ${devDoc.devices.length} devices, ${tree.questions.length} wizard questions`,
];
console.log(`catalog: ${summary.join('; ')}`);

if (needsLangs.length) {
  const pct = valueFields ? Math.round(((valueFields - untranslated) / valueFields) * 100) : 100;
  console.log(`translation: ${valueFields - untranslated}/${valueFields} measurement values localised (${pct}%)`);
  if (untranslatedByFamily.length) {
    console.log(`  still English-only: ${untranslatedByFamily.join(', ')}`);
  }
}

const needsReview = [
  ...families.filter((f) => f.data.status === 'needs-review').map((f) => `lock:${f.data.id}`),
  ...stdDoc.standards.filter((s) => s.status === 'needs-review').map((s) => `standard:${s.id}`),
  ...devDoc.devices.filter((d) => d.status === 'needs-review').map((d) => `device:${d.id}`),
];
if (needsReview.length) {
  console.log(`needs-review records published with a visible warning (${needsReview.length}): ${needsReview.join(', ')}`);
}

for (const w of warnings) console.warn(`WARN  ${w}`);
for (const e of errors) console.error(`ERROR ${e}`);

if (errors.length) {
  console.error(`\n${errors.length} error(s), ${warnings.length} warning(s) — catalog data is not consistent`);
  process.exit(1);
}
console.log(`\nOK  no errors, ${warnings.length} warning(s)`);
