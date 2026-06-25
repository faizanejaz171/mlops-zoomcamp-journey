import os
from pathlib import Path

image_dir = Path("data/images")
label_dir = Path("data/labels")

images = list(image_dir.glob("*.jpg"))
print(f"Total images: {len(images)}")

# Label stats
class_counts = {}
for lbl in label_dir.glob("*.txt"):
    with open(lbl) as f:
        for line in f:
            cls = line.split()[0]
            class_counts[cls] = class_counts.get(cls, 0) + 1

print(f"Class distribution: {class_counts}")
print(f"Images with labels: {len(list(label_dir.glob('*.txt')))}")
