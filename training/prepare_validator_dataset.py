from pathlib import Path
import shutil
import random

import numpy as np
from PIL import Image
from tensorflow.keras.datasets import cifar10


# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

LEAF_SOURCE = BASE_DIR / "dataset" / "split" / "train"
VALIDATOR_DIR = BASE_DIR / "dataset" / "validator"

LEAF_DIR = VALIDATOR_DIR / "leaf"
NON_LEAF_DIR = VALIDATOR_DIR / "non_leaf"
HARD_NEGATIVE_DIR = BASE_DIR / "dataset" / "hard_negative"


# ==========================================
# Configuration
# ==========================================

MAX_LEAF_IMAGES = 3000
MAX_NON_LEAF_IMAGES = 3000

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ==========================================
# Create folders
# ==========================================

LEAF_DIR.mkdir(parents=True, exist_ok=True)
NON_LEAF_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# Clear previous validator dataset
# ==========================================

print("Cleaning previous validator dataset...")

for folder in [LEAF_DIR, NON_LEAF_DIR]:
    for item in folder.iterdir():
        if item.is_file():
            item.unlink()


# ==========================================
# Collect leaf images
# ==========================================

print("\nCollecting leaf images...")

leaf_images = []

for class_folder in LEAF_SOURCE.iterdir():

    if not class_folder.is_dir():
        continue

    for image_path in class_folder.iterdir():

        if image_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            leaf_images.append(image_path)


random.shuffle(leaf_images)

leaf_images = leaf_images[:MAX_LEAF_IMAGES]


print("Leaf images selected:", len(leaf_images))


# ==========================================
# Copy leaf images
# ==========================================

for index, image_path in enumerate(leaf_images):

    destination = LEAF_DIR / f"leaf_{index:05d}{image_path.suffix.lower()}"

    shutil.copy2(image_path, destination)


# ==========================================
# Download CIFAR-10
# ==========================================

print("\nLoading CIFAR-10 dataset...")

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Combine train and test images
x_all = np.concatenate([x_train, x_test], axis=0)

print("CIFAR-10 images available:", len(x_all))

# ==========================================
# Add real-world hard negative images
# ==========================================

print("\nAdding real-world hard negative images...")

hard_negative_images = [
    HARD_NEGATIVE_DIR / "passport.jpg",
    HARD_NEGATIVE_DIR / "id_card.png",
    HARD_NEGATIVE_DIR / "radha_krishna.jpg"
]

hard_negative_count = 0

for image_path in hard_negative_images:

    if image_path.exists():

        destination = (
            NON_LEAF_DIR /
            f"hard_negative_{hard_negative_count:03d}{image_path.suffix.lower()}"
        )

        shutil.copy2(
            image_path,
            destination
        )

        hard_negative_count += 1

print(
    "Real-world hard negative images added:",
    hard_negative_count
)

# ==========================================
# Select non-leaf images
# ==========================================

indices = list(range(len(x_all)))
random.shuffle(indices)

indices = indices[:MAX_NON_LEAF_IMAGES]


# ==========================================
# Save non-leaf images
# ==========================================

print("\nSaving non-leaf images...")

for index, image_index in enumerate(indices):

    image_array = x_all[image_index]

    image = Image.fromarray(image_array)

    destination = NON_LEAF_DIR / f"non_leaf_{index:05d}.jpg"

    image.save(destination, quality=95)


# ==========================================
# Summary
# ==========================================

print("\n==========================================")
print("Validator dataset prepared successfully!")
print("==========================================")

print("Leaf images:", len(list(LEAF_DIR.iterdir())))
print("Non-leaf images:", len(list(NON_LEAF_DIR.iterdir())))

print("\nDataset location:")
print(VALIDATOR_DIR)