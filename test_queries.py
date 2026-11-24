import csv, json, os, urllib.parse, urllib.request
from collections import Counter

BASE = "http://127.0.0.1:8000/search"
TOP_K = 10

# Load product info: id -> row
with open("styles.csv", encoding="utf-8", errors="ignore") as f:
    styles = {row["id"]: row for row in csv.DictReader(f) if row.get("id")}

# What categories are in your 1,000 indexed images?
indexed_ids = [f.split(".")[0] for f in os.listdir("images") if f.lower().endswith(".jpg")]
counts = Counter(styles[i]["articleType"] for i in indexed_ids if i in styles)
print("Most common product types in your images:")
for t, n in counts.most_common(12):
    print(f"  {n:4d}  {t}")
print()

# (query, expected articleType values, expected colour or None)
TESTS = [
    ("red sneakers with white sole", ["Casual Shoes", "Sports Shoes"], "Red"),
    ("formal black watch", ["Watches"], "Black"),
    ("casual summer dress", ["Dresses"], None),
]


def run(query):
    url = f"{BASE}?q={urllib.parse.quote(query)}&top_k={TOP_K}"
    with urllib.request.urlopen(url) as r:
        return json.load(r)["results"]


for query, types, colour in TESTS:
    for prefix in ["", "a photo of "]:
        results = run(prefix + query)
        type_hits = colour_hits = 0
        for r in results:
            row = styles.get(r["filename"].split(".")[0], {})
            if row.get("articleType") in types:
                type_hits += 1
            if colour and row.get("baseColour") == colour:
                colour_hits += 1
        line = f'"{prefix}{query}"  ->  right type: {type_hits}/{len(results)}'
        if colour:
            line += f"  right colour: {colour_hits}/{len(results)}"
        print(line)
    print()