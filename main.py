from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from search import search

app = FastAPI(title="Visual Product Search")

# Makes files in the images folder available at /images/<filename>
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/search")
def search_endpoint(
    q: str = Query(..., min_length=1, description="Plain-English description"),
    top_k: int = Query(10, ge=1, le=50),
):
    results = search(q, top_k)
    for r in results:
        r["url"] = f"/images/{r['filename']}"
    return {"query": q, "results": results}


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Visual Product Search</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 30px; background: #fafafa; }
    input { padding: 10px; width: 320px; font-size: 16px; }
    button { padding: 10px 18px; font-size: 16px; cursor: pointer; }
    #grid { display: grid; grid-template-columns: repeat(auto-fill, 180px);
            gap: 16px; margin-top: 24px; }
    .card { background: #fff; border: 1px solid #ddd; border-radius: 8px;
            padding: 8px; text-align: center; font-size: 13px; }
    .card img { width: 100%; height: 180px; object-fit: contain; }
  </style>
</head>
<body>
  <h2>Visual Product Search</h2>
  <input id="q" placeholder="e.g. red sneakers with white sole"
         onkeydown="if(event.key==='Enter') go()">
  <button onclick="go()">Search</button>
  <div id="status"></div>
  <div id="grid"></div>

  <script>
    async function go() {
      const q = document.getElementById('q').value.trim();
      if (!q) return;
      document.getElementById('status').textContent = 'Searching...';
      const res = await fetch('/search?q=' + encodeURIComponent(q) + '&top_k=12');
      const data = await res.json();
      document.getElementById('status').textContent =
        data.results.length + ' results for "' + data.query + '"';
      document.getElementById('grid').innerHTML = data.results.map(r =>
        '<div class="card"><img src="' + r.url + '">' +
        '<div>score: ' + r.score + '</div></div>').join('');
    }
  </script>
</body>
</html>
"""