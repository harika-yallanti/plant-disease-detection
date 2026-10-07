import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import load_model


# ==============================
# Paths
# ==============================

VALIDATION_DIR = Path("dataset/split/validation")
MODEL_PATH = Path("models/plant_disease_model.keras")
CLASS_NAMES_PATH = Path("models/class_names.json")

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32


# ==============================
# Load class names
# ==============================

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
    class_names = json.load(file)

print("Classes:")

for index, class_name in enumerate(class_names):
    print(f"{index}: {class_name}")


# ==============================
# Load validation dataset
# ==============================

print("\nLoading validation dataset...")

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    VALIDATION_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
)

print(f"\nValidation images: {len(validation_dataset.file_paths)}")


# ==============================
# Load trained model
# ==============================

print("\nLoading trained model...")

model = load_model(MODEL_PATH)


# ==============================
# Generate predictions
# ==============================

print("\nGenerating predictions...")

true_labels = []
predicted_labels = []

for images, labels in validation_dataset:

    predictions = model.predict(images, verbose=0)

    predicted_classes = np.argmax(predictions, axis=1)

    true_labels.extend(labels.numpy())
    predicted_labels.extend(predicted_classes)


true_labels = np.array(true_labels)
predicted_labels = np.array(predicted_labels)


# ==============================
# Classification Report
# ==============================

print("\n==========================================")
print("Classification Report")
print("==========================================")

report = classification_report(
    true_labels,
    predicted_labels,
    labels=list(range(len(class_names))),
    target_names=class_names,
    zero_division=0,
)

print(report)


# ==============================
# Confusion Matrix
# ==============================

print("\n==========================================")
print("Confusion Matrix")
print("==========================================")

matrix = confusion_matrix(
    true_labels,
    predicted_labels,
    labels=list(range(len(class_names))),
)

print(matrix)


# ==============================
# Overall Accuracy
# ==============================

accuracy = np.mean(true_labels == predicted_labels)

print("\n==========================================")
print(f"Overall Accuracy: {accuracy * 100:.2f}%")
print("==========================================")

print("\nEvaluation completed successfully!")