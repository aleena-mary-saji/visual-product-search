import json, urllib.parse, urllib.request, csv
from collections import Counter

with open("styles.csv", encoding="utf-8", errors="ignore") as f:
    styles = {r["id"]: r for r in csv.DictReader(f) if r.get("id")}

print("Dresses in dataset:", sum(1 for r in styles.values() if r["articleType"] == "Dresses"))

for q in ["casual summer dress", "dress", "women's floral dress", "a long maxi dress"]:
    url = "http://127.0.0.1:8000/search?top_k=20&q=" + urllib.parse.quote(q)
    res = json.load(urllib.request.urlopen(url))["results"]
    types = Counter(styles.get(r["filename"].split(".")[0], {}).get("articleType") for r in res)
    print(f'\n"{q}" ->', dict(types))