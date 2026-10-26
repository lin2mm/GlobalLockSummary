import json

with open('content/site.json', 'r', encoding='utf-8') as f:
    site = json.load(f)

# 增加专利规避菜单项
patent_zh = {
    "label": "专利规避",
    "href": "zh/patent-avoidance.html",
    "iconSvg": "<svg class=\"nav__icon\" viewBox=\"0 0 24 24\" width=\"15\" height=\"15\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z\"/></svg>"
}

patent_en = {
    "label": "Patent FTO",
    "href": "patent-avoidance.html",
    "iconSvg": "<svg class=\"nav__icon\" viewBox=\"0 0 24 24\" width=\"15\" height=\"15\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z\"/></svg>"
}

# 检查是否已存在
existing_zh = [item['href'] for item in site['navigation']['zh']]
if 'zh/patent-avoidance.html' not in existing_zh:
    site['navigation']['zh'].append(patent_zh)
    print("Added 专利规避 to navigation.zh")

existing_en = [item['href'] for item in site['navigation']['en']]
if 'patent-avoidance.html' not in existing_en:
    site['navigation']['en'].append(patent_en)
    print("Added Patent FTO to navigation.en")

with open('content/site.json', 'w', encoding='utf-8') as f:
    json.dump(site, f, indent=2, ensure_ascii=False)

