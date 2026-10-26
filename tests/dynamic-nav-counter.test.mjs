import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';
import assert from 'node:assert';

test('Dynamic Navigation Counters Assertion — 100% Sync with JSON Data', () => {
  const zhIndex = readFileSync('_site/zh/index.html', 'utf8');
  const gallery = JSON.parse(readFileSync('content/catalog/gallery.json', 'utf8'));
  const adapters = JSON.parse(readFileSync('content/catalog/adapters-bom.json', 'utf8'));
  const cases = JSON.parse(readFileSync('content/catalog/installation-cases.json', 'utf8'));

  // 1. 断言锁型总览数字严格等于 gallery.json 真实长度
  const expectedLocks = `锁型总览 (${gallery.length})`;
  assert.ok(zhIndex.includes(expectedLocks), `Nav MUST dynamically contain '${expectedLocks}'!`);

  // 2. 断言转接工具数字严格等于 adapters-bom.json 真实长度
  const expectedAdapters = `转接工具 (${adapters.length})`;
  assert.ok(zhIndex.includes(expectedAdapters), `Nav MUST dynamically contain '${expectedAdapters}'!`);

  // 3. 断言工程实录数字严格等于 installation-cases.json 真实长度
  const expectedCases = `工程实录 (${cases.length})`;
  assert.ok(zhIndex.includes(expectedCases), `Nav MUST dynamically contain '${expectedCases}'!`);

  console.log(`✓ All dynamic nav counters verified: Locks=${gallery.length}, Adapters=${adapters.length}, Cases=${cases.length}`);
});
