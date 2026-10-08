from datasets import load_dataset
from pathlib import Path
import shutil



# Configuration


MAX_IMAGES_PER_CLASS = 500

OUTPUT_DIR = Path("dataset/processed")

selected_classes = [
    "Apple___Apple_scab",
    "Apple___healthy",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___healthy",
]



# Load dataset


print("Loading PlantVillage dataset...")

dataset = load_dataset(
    "geraldmc/plantvillage-full",
    revision="v0.1.0",
    split="train"
)

print(f"Total images: {len(dataset)}")



# Filter selected classes


print("\nFiltering selected classes...")

dataset = dataset.filter(
    lambda example: example["class_label"] in selected_classes
)

print(f"Filtered images: {len(dataset)}")



# Remove old processed dataset


if OUTPUT_DIR.exists():
    print("\nRemoving previous processed dataset...")
    shutil.rmtree(OUTPUT_DIR)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)



# Save images


class_counts = {}

for class_name in selected_classes:

    print(f"\nProcessing: {class_name}")

    class_dataset = dataset.filter(
        lambda example: example["class_label"] == class_name
    )

    total = len(class_dataset)

    number_to_use = min(
        MAX_IMAGES_PER_CLASS,
        total
    )

    print(f"Available: {total}")
    print(f"Using: {number_to_use}")

    class_output_dir = OUTPUT_DIR / class_name
    class_output_dir.mkdir(parents=True, exist_ok=True)

    selected = class_dataset.select(
        range(number_to_use)
    )

    for index, example in enumerate(selected):

        image = example["image"]

        # Make sure image is RGB
        image = image.convert("RGB")

        image_path = (
            class_output_dir /
            f"{index:05d}.jpg"
        )

        image.save(
            image_path,
            format="JPEG",
            quality=95
        )

    class_counts[class_name] = number_to_use



# Summary


print("\n===================================")
print("Dataset preparation completed!")
print("===================================")

total_saved = 0

for class_name, count in class_counts.items():

    print(f"{class_name}: {count}")

    total_saved += count

print("-----------------------------------")
print(f"Total images saved: {total_saved}")
print(f"Location: {OUTPUT_DIR}")