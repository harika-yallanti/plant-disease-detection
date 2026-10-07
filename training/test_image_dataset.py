from datasets import load_dataset


print("Loading PlantVillage image dataset...")

dataset = load_dataset(
    "geraldmc/plantvillage-full",
    revision="v0.1.0",
    split="train"
)

print("\nDataset loaded successfully!")
print("Number of images:", len(dataset))

print("\nDataset features:")
print(dataset.features)

print("\nFirst image:")
print(dataset[0]["image"])

print("\nFirst class:")
print(dataset[0]["class_label"])