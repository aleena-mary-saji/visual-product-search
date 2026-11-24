import os
from encoder import encode_images, encode_text

folder = "images"
files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))][:4]
paths = [os.path.join(folder, f) for f in files]

img_vecs = encode_images(paths)
print("Image vectors shape:", img_vecs.shape)      # expect (4, 512)

txt_vec = encode_text("red sneakers")
print("Text vector shape:", txt_vec.shape)         # expect (512,)

# Similarity of the text to each test image (dot product = cosine, since normalized)
for f, score in zip(files, img_vecs @ txt_vec):
    print(f, round(float(score), 4))