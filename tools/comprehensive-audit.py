import os
import re
import json

print("=== 1. Checking Broken Images in _site ===")
broken_images = []
for root, dirs, files in os.walk('_site'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as hf:
                content = hf.read()
            for m in re.finditer(r'src=["\']([^"\']+\.(?:jpg|png|webp|svg))["\']', content):
                src = m.group(1)
                if src.startswith('http'): continue
                if src.startswith('/'):
                    disk_target = os.path.join('_site', src[1:])
                else:
                    disk_target = os.path.normpath(os.path.join(root, src))
                if not os.path.exists(disk_target):
                    broken_images.append((path, src))

print(f"Total broken image references: {len(broken_images)}")
if broken_images:
    for b in broken_images[:5]:
        print("Broken:", b)

print("\n=== 2. Checking HTML Validation & Titles ===")
duplicate_titles = []
for root, dirs, files in os.walk('_site'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as hf:
                c = hf.read()
            h1s = re.findall(r'<h1[\s>](.*?)</h1>', c, re.DOTALL)
            if len(h1s) > 1:
                duplicate_titles.append((path, len(h1s)))

print(f"Total pages with duplicate H1: {len(duplicate_titles)}")

print("\n=== 3. Checking Legacy '5 大' mentions in _site ===")
legacy_mentions = []
for root, dirs, files in os.walk('_site'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as hf:
                c = hf.read()
            if '5 大板块' in c or '5大板块' in c or '5 Major Divisions' in c:
                legacy_mentions.append(path)

print(f"Total pages with legacy 5-division mentions: {len(legacy_mentions)}")
if legacy_mentions:
    for lm in legacy_mentions[:5]:
        print("Legacy mention in:", lm)

print("\n=== 4. Checking Navigation Counter Sync ===")
with open('content/catalog/gallery.json') as f:
    locks_count = len(json.load(f))
with open('content/catalog/adapters-bom.json') as f:
    adapters_count = len(json.load(f))
with open('content/catalog/installation-cases.json') as f:
    cases_count = len(json.load(f))

print(f"JSON datasets: Locks={locks_count}, Adapters={adapters_count}, Cases={cases_count}")
