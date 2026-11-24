from qdrant_client import QdrantClient
from encoder import encode_text

COLLECTION = "products"
client = QdrantClient(path="qdrant_data")


def search(query: str, top_k: int = 10):
    vec = [float(x) for x in encode_text("a photo of " + query)]

    # Newer qdrant-client uses query_points; older versions use search
    if hasattr(client, "query_points"):
        hits = client.query_points(
            collection_name=COLLECTION, query=vec, limit=top_k
        ).points
    else:
        hits = client.search(
            collection_name=COLLECTION, query_vector=vec, limit=top_k
        )

    return [
        {
            "filename": h.payload["filename"],
            "path": h.payload["path"],
            "score": round(h.score, 4),
        }
        for h in hits
    ]


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) or "red sneakers with white sole"
    print("Query:", query)
    for r in search(query, top_k=5):
        print(r["score"], r["filename"])