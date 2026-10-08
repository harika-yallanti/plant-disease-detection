import json
from pathlib import Path

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers



# Configuration


TRAIN_DIR = Path("dataset/split/train")
VALIDATION_DIR = Path("dataset/split/validation")
MODEL_DIR = Path("models")

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
SEED = 42


MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# Load training dataset


print("Loading training dataset...")

train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=SEED,
)



# Load validation dataset


print("\nLoading validation dataset...")

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    VALIDATION_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
)



# Class names


class_names = train_dataset.class_names

print("\nClasses:")

for index, class_name in enumerate(class_names):
    print(f"{index}: {class_name}")



# Improve performance


AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    AUTOTUNE
)



# Data augmentation


data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
    ],
    name="data_augmentation",
)



# MobileNetV2


print("\nLoading MobileNetV2...")

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet",
)

base_model.trainable = False



# Build model


inputs = keras.Input(
    shape=(224, 224, 3)
)

x = data_augmentation(inputs)

x = tf.keras.applications.mobilenet_v2.preprocess_input(
    x
)

x = base_model(
    x,
    training=False
)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.2)(x)

outputs = layers.Dense(
    len(class_names),
    activation="softmax"
)(x)

model = keras.Model(
    inputs,
    outputs
)



# Compile


model.compile(
    optimizer=keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)



# Callbacks


callbacks = [

    keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True,
    ),

    keras.callbacks.ModelCheckpoint(
        filepath=MODEL_DIR / "plant_disease_model.keras",
        monitor="val_accuracy",
        save_best_only=True,
    ),
]



# Train


print("\nStarting training...")

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
    callbacks=callbacks,
)



# Save class names


with open(
    MODEL_DIR / "class_names.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        class_names,
        file,
        indent=4
    )



# Final evaluation


print("\nEvaluating model...")

loss, accuracy = model.evaluate(
    validation_dataset
)

print(
    f"\nValidation Loss: {loss:.4f}"
)

print(
    f"Validation Accuracy: "
    f"{accuracy * 100:.2f}%"
)


print("\nTraining completed successfully!")

print(
    "Model saved to: "
    "models/plant_disease_model.keras"
)

print(
    "Class names saved to: "
    "models/class_names.json"
)