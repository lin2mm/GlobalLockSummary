import json

with open('content/site.json', 'r', encoding='utf-8') as f:
    site = json.load(f)

for item in site['navigation']['zh']:
    if 'patent-avoidance.html' in item['href']:
        item['label'] = '后装专利规避'

for item in site['navigation']['en']:
    if 'patent-avoidance.html' in item['href']:
        item['label'] = 'Retrofit FTO'

with open('content/site.json', 'w', encoding='utf-8') as f:
    json.dump(site, f, indent=2, ensure_ascii=False)

print("Updated site.json navigation labels to Retrofit 后装专利规避!")

