import os, shutil

SRC = r"C:\Users\user\Downloads\fashion-dataset\images"   # change to your path
DST = r"C:\Users\user\Documents\visual-search\images"
COUNT = 1000

files = [f for f in os.listdir(SRC) if f.lower().endswith(".jpg")][:COUNT]
for f in files:
    shutil.copy(os.path.join(SRC, f), os.path.join(DST, f))
print("Copied", len(files), "images")