from pathlib import Path
import json

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint
)



# Paths


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "dataset" / "validator"
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "leaf_validator.keras"
CLASS_NAMES_PATH = MODEL_DIR / "validator_class_names.json"

MODEL_DIR.mkdir(parents=True, exist_ok=True)



# Configuration


IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
SEED = 42



# Load dataset


print("Loading validator dataset...")

train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary"
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary",
    shuffle=False
)

class_names = train_dataset.class_names

print("Class names:", class_names)

# Save class names for the backend
with open(CLASS_NAMES_PATH, "w", encoding="utf-8") as file:
    json.dump(class_names, file, indent=4)


# Improve data-loading performance
AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    buffer_size=AUTOTUNE
)



# Data augmentation


data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1)
])



# Load MobileNetV2


print("\nLoading MobileNetV2...")

base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze pretrained layers
base_model.trainable = False



# Build validator model


inputs = layers.Input(shape=(224, 224, 3))

x = data_augmentation(inputs)

# Convert pixel values from [0, 255] to [-1, 1]
x = layers.Rescaling(
    scale=1.0 / 127.5,
    offset=-1
)(x)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.3)(x)

# Binary classification output
outputs = layers.Dense(
    1,
    activation="sigmoid"
)(x)

validator_model = models.Model(
    inputs,
    outputs
)



# Compile model


validator_model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

validator_model.summary()



# Callbacks


early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)

model_checkpoint = ModelCheckpoint(
    filepath=MODEL_PATH,
    monitor="val_loss",
    save_best_only=True,
    verbose=1
)



# Train model


print("\nStarting validator training...")

history = validator_model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
    callbacks=[
        early_stopping,
        model_checkpoint
    ]
)



# Final evaluation


print("\nEvaluating validator...")

loss, accuracy = validator_model.evaluate(
    validation_dataset,
    verbose=1
)

print("\n====================================")
print("Validator training completed!")
print("====================================")

print(f"Validation Accuracy: {accuracy * 100:.2f}%")
print(f"Model saved at: {MODEL_PATH}")
print(f"Class names saved at: {CLASS_NAMES_PATH}")