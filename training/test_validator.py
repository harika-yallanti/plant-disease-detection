from pathlib import Path
import sys

import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model


# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "leaf_validator.keras"

# ==========================================
# Load model
# ==========================================

print("Loading leaf validator...")

model = load_model(MODEL_PATH)

print("Validator loaded successfully!")


# ==========================================
# Check command-line argument
# ==========================================

if len(sys.argv) < 2:
    print("\nUsage:")
    print("python training\\test_validator.py \"path_to_image\"")
    sys.exit(1)

image_path = Path(sys.argv[1])

if not image_path.exists():
    print("\nImage not found:")
    print(image_path)
    sys.exit(1)


# ==========================================
# Load image
# ==========================================

try:

    image = Image.open(image_path).convert("RGB")

    image = image.resize((224, 224))

    image_array = np.array(image)

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

except Exception as error:

    print("\nCould not process image:")
    print(error)

    sys.exit(1)


# ==========================================
# Prediction
# ==========================================

prediction = float(
    model.predict(
        image_array,
        verbose=0
    )[0][0]
)


# ==========================================
# Interpret prediction
# ==========================================

# sigmoid output:
# 0 = leaf
# 1 = non-leaf

if prediction >= 0.5:

    result = "NON-LEAF"

    confidence = prediction * 100

else:

    result = "LEAF"

    confidence = (1 - prediction) * 100


# ==========================================
# Display result
# ==========================================

print("\n====================================")
print("Leaf Validator Result")
print("====================================")

print("Image:", image_path.name)
print("Prediction:", result)
print(f"Confidence: {confidence:.2f}%")
print(f"Raw model output: {prediction:.6f}")

print("====================================")