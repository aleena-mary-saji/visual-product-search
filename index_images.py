import os
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from encoder import encode_images

IMAGE_DIR = "images"
COLLECTION = "products"
BATCH = 16          # lower to 8 if you get CUDA out-of-memory

client = QdrantClient(path="qdrant_data")   # local folder, no server needed

# Start fresh each time you run this script
if client.collection_exists(COLLECTION):
    client.delete_collection(COLLECTION)
client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=512, distance=Distance.COSINE),
)

files = sorted(
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
)
print("Found", len(files), "images")

indexed = 0
for start in tqdm(range(0, len(files), BATCH)):
    batch_files = files[start:start + BATCH]
    paths = [os.path.join(IMAGE_DIR, f) for f in batch_files]

    try:
        vectors = encode_images(paths)
        ok_files, ok_paths = batch_files, paths
    except Exception as e:
        # One bad image shouldn't kill the whole batch: retry one by one
        vec_list, ok_files, ok_paths = [], [], []
        for f, p in zip(batch_files, paths):
            try:
                vec_list.append(encode_images([p])[0])
                ok_files.append(f)
                ok_paths.append(p)
            except Exception as e2:
                print("Skipping", f, "-", e2)
        if not vec_list:
            continue
        vectors = vec_list

    points = [
        PointStruct(
            id=start + j,
            vector=[float(x) for x in vectors[j]],
            payload={"path": ok_paths[j], "filename": ok_files[j]},
        )
        for j in range(len(ok_files))
    ]
    client.upsert(collection_name=COLLECTION, points=points)
    indexed += len(points)

print("Indexed", indexed, "images")
print("Total in collection:", client.count(COLLECTION).count)
client.close()