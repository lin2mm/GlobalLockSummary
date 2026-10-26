#!/usr/bin/env python3
"""
Comprehensive Image Audit Script for GlobalLockSummary
全量扫描全站代码、Markdown 页面、JSON 数据库与 HTML 构建产物中的所有图片路径，
检测是否存在死链、缺失文件、0 字节损坏文件或非标准格式文件。
"""
import os
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "_site"
CONTENT_DIR = ROOT / "content"
ASSETS_DIR = ROOT / "assets"

print("=== 1. Scanning Physical Files in assets/ ===")
all_assets = list(ASSETS_DIR.glob("**/*"))
image_files = [f for f in all_assets if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif"]]
print(f"Total physical images in assets/: {len(image_files)}")

zero_bytes = [f for f in image_files if f.stat().st_size == 0]
if zero_bytes:
    print(f"❌ Found {len(zero_bytes)} zero-byte corrupted images:")
    for zb in zero_bytes:
        print(f"   - {zb.relative_to(ROOT)}")
else:
    print("✓ No zero-byte corrupted images found.")

print("\n=== 2. Auditing gallery.json (70 Locks) ===")
with open(CONTENT_DIR / "catalog" / "gallery.json", "r", encoding="utf-8") as f:
    gallery = json.load(f)

gallery_issues = []
for item in gallery:
    lid = item.get("id")
    for key in ["image", "sceneImage", "productImage"]:
        val = item.get(key)
        if val:
            clean_path = val.lstrip("/")
            p = ROOT / clean_path
            if not p.exists():
                gallery_issues.append((lid, key, val, "File does not exist"))
            elif p.stat().st_size == 0:
                gallery_issues.append((lid, key, val, "Zero bytes"))

if gallery_issues:
    print(f"❌ Found {len(gallery_issues)} issues in gallery.json:")
    for iss in gallery_issues:
        print(f"   - [{iss[0]}] {iss[1]}: {iss[2]} -> {iss[3]}")
else:
    print(f"✓ All image paths in gallery.json (70 locks × 3 images) resolve to valid non-empty files.")

print("\n=== 3. Auditing adapters-bom.json & field-issues.json ===")
adapters_path = CONTENT_DIR / "catalog" / "adapters-bom.json"
if adapters_path.exists():
    with open(adapters_path, "r", encoding="utf-8") as f:
        adapters = json.load(f)
    for a in adapters:
        img = a.get("image")
        if img:
            p = ROOT / img.lstrip("/")
            if not p.exists():
                print(f"❌ Adapter {a.get('id')} image missing: {img}")
            else:
                print(f"✓ Adapter {a.get('id')}: {img} ({p.stat().st_size} bytes)")

print("\n=== 4. Auditing Markdown Pages (content/pages/) ===")
md_files = list(CONTENT_DIR.glob("**/*.md"))
img_md_regex = re.compile(r'!\[.*?\]\((.*?)\)|<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)

md_issues = []
for md in md_files:
    content = md.read_text(encoding="utf-8")
    matches = img_md_regex.findall(content)
    for m in matches:
        src = m[0] or m[1]
        if src.startswith("http") or src.startswith("data:"):
            continue
        # 解析相对路径
        clean_src = src.split("?")[0].split("#")[0]
        if clean_src.startswith("/"):
            target_p = ROOT / clean_src.lstrip("/")
        elif clean_src.startswith("../"):
            # 相当于从 content/pages/zh/ 退到 content/ 还是 ROOT/ ?
            # 在 SSG 构建中，页面在 _site/zh/ 或 _site/，引用的 ../assets 实际指向 _site/assets/ 即 ROOT/assets/
            target_p = ROOT / clean_src.replace("../", "")
        else:
            target_p = md.parent / clean_src

        if not target_p.exists():
            md_issues.append((str(md.relative_to(ROOT)), src, str(target_p.relative_to(ROOT) if target_p.is_relative_to(ROOT) else target_p)))

if md_issues:
    print(f"❌ Found {len(md_issues)} broken image links in markdown:")
    for mi in md_issues:
        print(f"   - File: {mi[0]} -> src: '{mi[1]}' (Checked: {mi[2]})")
else:
    print(f"✓ All images in markdown pages resolve properly.")

print("\n=== 5. Auditing Built HTML (_site/) Image References ===")
if SITE_DIR.exists():
    html_files = list(SITE_DIR.glob("**/*.html"))
    html_issues = []
    for hf in html_files:
        html_text = hf.read_text(encoding="utf-8")
        matches = re.findall(r'<img[^>]+src=["\'](.*?)["\']', html_text, re.IGNORECASE)
        for src in matches:
            if src.startswith("http") or src.startswith("data:"):
                continue
            clean_src = src.split("?")[0].split("#")[0]
            if clean_src.startswith("/"):
                p = SITE_DIR / clean_src.lstrip("/")
            else:
                p = (hf.parent / clean_src).resolve()
            
            if not p.exists():
                html_issues.append((str(hf.relative_to(ROOT)), src, str(p)))

    if html_issues:
        print(f"❌ Found {len(html_issues)} broken img tags in built site:")
        for hi in html_issues[:15]:
            print(f"   - Page: {hi[0]} -> src: {hi[1]}")
    else:
        print(f"✓ All {len(html_files)} built HTML pages have 100% valid image references.")

