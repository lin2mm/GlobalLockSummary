/**
 * Tests for the identification logic and the decision data that drives it.
 *
 * This runs the same assets/js/scoring.js the browser loads (evaluated in a VM
 * with a CommonJS shim, since the repo is ESM) against the same catalog.json the
 * site publishes. So a change to the decision tree that breaks identification
 * fails here, not in front of a user.
 *
 *   npm test     # builds first, then runs this
 */

import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');

/* Load the shipped scoring.js exactly as the browser sees it. */
function loadScoring() {
  const source = readFileSync(resolve(ROOT, 'assets/js/scoring.js'), 'utf8');
  const moduleShim = { exports: {} };
  const context = { module: moduleShim, globalThis: {} };
  vm.createContext(context);
  vm.runInContext(source, context, { filename: 'assets/js/scoring.js' });
  if (!moduleShim.exports.rank) throw new Error('scoring.js did not export its API via the CommonJS branch');
  return moduleShim.exports;
}

const scoring = loadScoring();

let catalogPath;
try {
  catalogPath = resolve(ROOT, '_site/data/catalog.json');
  readFileSync(catalogPath);
} catch {
  console.error('FAIL  _site/data/catalog.json not found — run `node build.mjs` (or `npm test`) first');
  process.exit(1);
}
const catalog = JSON.parse(readFileSync(catalogPath, 'utf8'));
const families = catalog.lockFamilies;
const questions = catalog.decisionTree.questions.map((q) => ({
  id: q.id,
  prompt: q.prompt.en,
  options: q.options.map((o) => ({ id: o.id, label: o.label.en, add: o.add })),
}));

let passed = 0;
const failures = [];
function check(name, condition, detail) {
  if (condition) { passed++; return; }
  failures.push(`${name}${detail ? ` — ${detail}` : ''}`);
}

function decideWith(choices) {
  const answers = scoring.answersFrom(questions, choices);
  if (!answers) throw new Error(`invalid choice set: ${JSON.stringify(choices)}`);
  return scoring.decide(answers, families);
}

/* ---------- 1. Realistic answer paths identify the right family ---------- */

const paths = [
  {
    name: 'Continental European interior door with a euro cylinder',
    choices: { region: 'eu', door: 'timber', keyhole: 'euro-cyl', inside: 'thumbturn', backset: '55_60' },
    expect: 'euro-cylinder-mortise',
  },
  {
    name: 'British uPVC door with a lift-up handle',
    choices: { region: 'uk', door: 'upvc', keyhole: 'oval-cyl', inside: 'lift', backset: 'lt50' },
    expect: 'multipoint-upvc',
  },
  {
    name: 'British timber door with a keyhole in the faceplate',
    choices: { region: 'uk', door: 'timber', keyhole: 'faceplate', inside: 'knob', backset: 'unknown' },
    expect: 'uk-5-lever-mortice',
  },
  {
    name: 'North American deadbolt above the handle',
    choices: { region: 'na', door: 'timber', keyhole: 'deadbolt', inside: 'thumbturn', backset: '70' },
    expect: 'us-deadbolt',
  },
  {
    name: 'North American lockset with the key in the knob',
    choices: { region: 'na', door: 'timber', keyhole: 'knob', inside: 'knob', backset: '70' },
    expect: 'us-bored-lever',
  },
  {
    name: 'Singapore HDB door opening onto a metal gate',
    choices: { region: 'sg', door: 'metal', keyhole: 'none', inside: 'pushpull', backset: '55_60' },
    expect: 'sg-hdb-mortise',
  },
  {
    name: 'Japanese door with a 64 mm backset',
    choices: { region: 'jpkr', door: 'timber', keyhole: 'none', inside: 'lever', backset: '64' },
    expect: 'jp-miwa-case',
  },
  {
    name: 'Australian deadlatch with a slide inside',
    choices: { region: 'anz', door: 'timber', keyhole: 'rim', inside: 'slide', backset: '55_60' },
    expect: 'au-deadlatch',
  },
  {
    name: 'Padlock on a hasp',
    choices: { region: 'other', door: 'metal', keyhole: 'padlock', inside: 'unknown', backset: 'unknown' },
    expect: 'padlock-hasppad',
  },
  {
    name: 'Singapore metal security gate in front of the main door',
    choices: { region: 'sg', door: 'gate', keyhole: 'none', inside: 'lever', backset: 'unknown' },
    expect: 'sg-metal-gate-lock',
  },
  {
    name: 'Singapore metal gate even when the rest of the answers favour the main door',
    choices: { region: 'sg', door: 'gate', keyhole: 'euro-cyl', inside: 'lever', backset: '55_60' },
    expect: 'sg-metal-gate-lock',
  },
  {
    name: 'Indian mortise handle set with a 50 mm backset',
    choices: { region: 'in', door: 'timber', keyhole: 'euro-cyl', inside: 'lever', backset: '50' },
    expect: 'in-mortise-rim',
  },
  {
    name: 'Indian rim nightlatch',
    choices: { region: 'in', door: 'timber', keyhole: 'rim', inside: 'knob', backset: 'unknown' },
    expect: 'in-mortise-rim',
  },
];

for (const path of paths) {
  const decision = decideWith(path.choices);
  check(
    `identifies: ${path.name}`,
    decision.confident && decision.top.id === path.expect,
    decision.top ? `got ${decision.top.id} (score ${decision.top.score}, reason ${decision.reason})` : `no match (reason ${decision.reason})`
  );
}

/* ---------- 2. Weak or tied evidence must not produce a confident answer ---------- */

const weak = decideWith({ region: 'other', door: 'unknown', keyhole: 'none', inside: 'unknown', backset: 'unknown' });
check(
  'an all-unsure path does not claim an identification',
  weak.confident === false && weak.top === null,
  `confident=${weak.confident}, top=${weak.top && weak.top.id}, reason=${weak.reason}`
);
check(
  'an all-unsure path still offers the tied candidates',
  weak.tied.length >= 2,
  `tied=${weak.tied.length}`
);

/* ---------- 3. Decision-tree completeness ---------- */

const optionIds = questions.map((q) => q.options.map((o) => o.id));
const winners = new Set();
let combinations = 0;
(function walk(depth, acc) {
  if (depth === questions.length) {
    combinations++;
    const choices = {};
    questions.forEach((q, i) => { choices[q.id] = acc[i]; });
    const answers = scoring.answersFrom(questions, choices);
    const decision = scoring.decide(answers, families);
    if (decision.confident) winners.add(decision.top.id);
    return;
  }
  for (const option of optionIds[depth]) walk(depth + 1, [...acc, option]);
})(0, []);

const unreachable = families.map((f) => f.id).filter((id) => !winners.has(id));
check(
  'every lock family can be identified by some answer path',
  unreachable.length === 0,
  unreachable.length ? `never reachable: ${unreachable.join(', ')}` : ''
);
check('the tree was exercised exhaustively', combinations > 1000, `only ${combinations} combinations`);

/* ---------- 4. Determinism and input handling ---------- */

const repeatA = decideWith(paths[0].choices);
const repeatB = decideWith(paths[0].choices);
check(
  'the same answers always give the same ranking',
  JSON.stringify(repeatA.ranked.map((r) => r.id)) === JSON.stringify(repeatB.ranked.map((r) => r.id))
);

check('answersFrom rejects an unknown option id', scoring.answersFrom(questions, { region: 'nonsense' }) === null);
check('answersFrom rejects a missing question', scoring.answersFrom(questions, {}) === null);
check('rank ignores non-numeric scores', scoring.rank([{ add: { 'euro-cylinder-mortise': 'many' } }], families).length === 0);
check('rank on no answers returns nothing', scoring.rank([], families).length === 0);

const tally = scoring.tally([{ add: { a: 3, b: 2 } }, { add: { b: 5 } }]);
check('tally sums points across answers', tally.a === 3 && tally.b === 7, JSON.stringify(tally));

/* ---------- report ---------- */

console.log(`wizard logic: ${combinations} answer combinations, ${families.length} lock families, ${winners.size} reachable`);
if (failures.length) {
  for (const f of failures) console.error(`FAIL  ${f}`);
  console.error(`\n${failures.length} failed, ${passed} passed`);
  process.exit(1);
}
console.log(`OK  ${passed} checks passed`);
