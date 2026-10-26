import json
import re

# 1. 更新 content/i18n/terms.json
with open('content/i18n/terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

# 确保 retrofit 的专业术语映射准确
if 'retrofit' in terms:
    terms['retrofit']['zh'] = "后装智能锁"
    terms['retrofit']['en'] = "Retrofit Smart Lock"

with open('content/i18n/terms.json', 'w', encoding='utf-8') as f:
    json.dump(terms, f, indent=2, ensure_ascii=False)
print("Updated terms.json!")

# 2. 更新 content/site.json 中的描述和产品文案
with open('content/site.json', 'r', encoding='utf-8') as f:
    site = json.load(f)

site['product']['label']['zh'] = "后装智能锁"
site['product']['label']['en'] = "Retrofit Smart Lock"
site['description']['zh'] = "全球机械门锁开放知识库：识别现有门锁、记录尺寸公差，设计与之匹配的后装智能锁（免换锁 / 租客无损加装）。"

with open('content/site.json', 'w', encoding='utf-8') as f:
    json.dump(site, f, indent=2, ensure_ascii=False)
print("Updated site.json!")

