from pathlib import Path
import shutil
import random


# ============================================================
# Configuration
# ============================================================

SOURCE_DIR = Path("dataset/processed")
OUTPUT_DIR = Path("dataset/split")

VALIDATION_RATIO = 0.20
SEED = 42


# ============================================================
# Set random seed
# ============================================================

random.seed(SEED)


# ============================================================
# Remove previous split
# ============================================================

if OUTPUT_DIR.exists():
    print("Removing previous split...")
    shutil.rmtree(OUTPUT_DIR)


# ============================================================
# Create output folders
# ============================================================

TRAIN_DIR = OUTPUT_DIR / "train"
VALIDATION_DIR = OUTPUT_DIR / "validation"

TRAIN_DIR.mkdir(parents=True)
VALIDATION_DIR.mkdir(parents=True)


# ============================================================
# Process every class
# ============================================================

total_train = 0
total_validation = 0

class_directories = sorted(
    [
        directory
        for directory in SOURCE_DIR.iterdir()
        if directory.is_dir()
    ]
)


print("\nCreating stratified train/validation split...\n")


for class_dir in class_directories:

    class_name = class_dir.name

    images = sorted(
        [
            image
            for image in class_dir.iterdir()
            if image.suffix.lower() in [
                ".jpg",
                ".jpeg",
                ".png"
            ]
        ]
    )

    random.shuffle(images)

    validation_count = max(
        1,
        int(len(images) * VALIDATION_RATIO)
    )

    validation_images = images[:validation_count]
    train_images = images[validation_count:]

    train_class_dir = TRAIN_DIR / class_name
    validation_class_dir = VALIDATION_DIR / class_name

    train_class_dir.mkdir(parents=True)
    validation_class_dir.mkdir(parents=True)

    for image in train_images:
        shutil.copy2(
            image,
            train_class_dir / image.name
        )

    for image in validation_images:
        shutil.copy2(
            image,
            validation_class_dir / image.name
        )

    total_train += len(train_images)
    total_validation += len(validation_images)

    print(
        f"{class_name}: "
        f"{len(train_images)} train, "
        f"{len(validation_images)} validation"
    )


# ============================================================
# Summary
# ============================================================

print("\n===================================")
print("Split completed!")
print("===================================")

print(f"Training images: {total_train}")
print(f"Validation images: {total_validation}")

print(
    f"\nTrain directory: {TRAIN_DIR}"
)

print(
    f"Validation directory: {VALIDATION_DIR}"
)