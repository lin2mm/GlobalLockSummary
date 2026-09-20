with open("_site/zh/locks/euro-cylinder-mortise.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find("spec-cluster-bar")
if idx != -1:
    print("Found spec-cluster-bar:")
    print(html[idx:idx+1200])
else:
    print("spec-cluster-bar NOT FOUND!")

toc_idx = html.find("toc__list")
if toc_idx != -1:
    print("\nTOC contents:")
    print(html[toc_idx:toc_idx+800])
