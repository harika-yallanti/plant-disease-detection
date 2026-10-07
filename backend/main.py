from pathlib import Path
import json

import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "plant_disease_model.keras"
CLASS_NAMES_PATH = BASE_DIR / "models" / "class_names.json"

VALIDATOR_MODEL_PATH = BASE_DIR / "models" / "leaf_validator.keras"


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Plant Disease Detection API",
    description="AI-based plant leaf disease detection API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# LOAD PLANT DISEASE MODEL
# ============================================================

print("Loading plant disease model...")

model = load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
    class_names = json.load(file)

print("Plant disease model loaded successfully!")
print("Number of disease classes:", len(class_names))


# ============================================================
# LOAD LEAF VALIDATOR MODEL
# ============================================================

print("Loading leaf validator...")

validator_model = load_model(VALIDATOR_MODEL_PATH)

print("Leaf validator loaded successfully!")


# ============================================================
# DISEASE INFORMATION
# ============================================================

DISEASE_INFO = {

    "Apple___Apple_scab": {
        "disease": "Apple Scab",
        "description": (
            "Apple scab is a fungal disease that causes dark "
            "spots and lesions on apple leaves."
        ),
        "treatment": (
            "Remove affected leaves and use an appropriate "
            "fungicide as recommended for apple trees."
        ),
        "prevention": (
            "Keep the area clean, remove fallen leaves, "
            "and maintain good air circulation."
        )
    },

    "Apple___healthy": {
        "disease": "Healthy Apple Leaf",
        "description": (
            "The uploaded apple leaf appears healthy "
            "with no visible signs of the supported diseases."
        ),
        "treatment": (
            "No disease treatment is required."
        ),
        "prevention": (
            "Continue proper watering, nutrition, sunlight, "
            "and regular monitoring."
        )
    },

    "Corn_(maize)___Common_rust_": {
        "disease": "Corn Common Rust",
        "description": (
            "Common rust is a fungal disease that produces "
            "small reddish-brown rust-colored spots on corn leaves."
        ),
        "treatment": (
            "Use an appropriate fungicide when recommended "
            "and remove severely affected plant material."
        ),
        "prevention": (
            "Use resistant varieties, maintain proper spacing, "
            "and monitor plants regularly."
        )
    },

    "Corn_(maize)___healthy": {
        "disease": "Healthy Corn Leaf",
        "description": (
            "The uploaded corn leaf appears healthy "
            "with no visible signs of the supported diseases."
        ),
        "treatment": (
            "No disease treatment is required."
        ),
        "prevention": (
            "Maintain proper irrigation, nutrition, spacing, "
            "and regular crop monitoring."
        )
    },

    "Potato___Early_blight": {
        "disease": "Potato Early Blight",
        "description": (
            "Early blight is a fungal disease that can cause "
            "dark circular spots on potato leaves."
        ),
        "treatment": (
            "Remove severely affected leaves and use an "
            "appropriate fungicide according to local guidance."
        ),
        "prevention": (
            "Maintain good plant spacing, avoid prolonged leaf "
            "wetness, and remove infected plant debris."
        )
    },

    "Potato___Late_blight": {
        "disease": "Potato Late Blight",
        "description": (
            "Late blight is a serious disease that can cause "
            "dark water-soaked lesions on potato leaves."
        ),
        "treatment": (
            "Remove severely affected plant material and use "
            "an appropriate fungicide when recommended."
        ),
        "prevention": (
            "Use healthy planting material, provide good air "
            "circulation, and avoid excessive leaf moisture."
        )
    },

    "Potato___healthy": {
        "disease": "Healthy Potato Leaf",
        "description": (
            "The uploaded potato leaf appears healthy "
            "with no visible signs of the supported diseases."
        ),
        "treatment": (
            "No disease treatment is required."
        ),
        "prevention": (
            "Maintain proper watering, nutrition, spacing, "
            "and regular monitoring."
        )
    },

    "Tomato___Early_blight": {
        "disease": "Tomato Early Blight",
        "description": (
            "Early blight is a fungal disease that can cause "
            "dark spots and concentric ring patterns on tomato leaves."
        ),
        "treatment": (
            "Remove affected leaves and use an appropriate "
            "fungicide according to local agricultural guidance."
        ),
        "prevention": (
            "Avoid overhead watering, maintain good spacing, "
            "and remove infected plant debris."
        )
    },

    "Tomato___Late_blight": {
        "disease": "Tomato Late Blight",
        "description": (
            "Late blight can cause dark, irregular lesions "
            "on tomato leaves and can spread rapidly."
        ),
        "treatment": (
            "Remove affected plant material and use an "
            "appropriate fungicide when recommended."
        ),
        "prevention": (
            "Maintain good air circulation, avoid prolonged "
            "leaf moisture, and monitor plants frequently."
        )
    },

    "Tomato___healthy": {
        "disease": "Healthy Tomato Leaf",
        "description": (
            "The uploaded tomato leaf appears healthy "
            "with no visible signs of the supported diseases."
        ),
        "treatment": (
            "No disease treatment is required."
        ),
        "prevention": (
            "Continue proper watering, nutrition, sunlight, "
            "and regular monitoring."
        )
    }
}


# ============================================================
# HOME ROUTE
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Plant Disease Detection API is running",
        "status": "success"
    }


# ============================================================
# PREDICTION ROUTE
# ============================================================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # --------------------------------------------------------
    # CHECK FILE TYPE
    # --------------------------------------------------------

    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="File type could not be determined."
        )

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file."
        )

    # --------------------------------------------------------
    # READ IMAGE
    # --------------------------------------------------------

    try:
        image_bytes = await file.read()

        image = Image.open(
            __import__("io").BytesIO(image_bytes)
        )

        image = image.convert("RGB")

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file."
        )

    # --------------------------------------------------------
    # RESIZE IMAGE
    # --------------------------------------------------------

    image = image.resize((224, 224))

    # Convert image to NumPy array
    image_array = np.array(image, dtype=np.float32)

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    # --------------------------------------------------------
    # LEAF / NON-LEAF VALIDATION
    # --------------------------------------------------------

    validator_output = float(
        validator_model.predict(
            image_array,
            verbose=0
        )[0][0]
    )

    # 0.70 means sufficiently confident that the image
    # belongs to the non-leaf class.
    NON_LEAF_THRESHOLD = 0.70

    if validator_output >= NON_LEAF_THRESHOLD:

        return {
            "valid_leaf": False,
            "message": (
                "Please upload a clear plant leaf image "
                "for disease detection."
            ),
            "validator_confidence": round(
                validator_output * 100,
                2
            )
        }

    # --------------------------------------------------------
    # PLANT DISEASE PREDICTION
    # --------------------------------------------------------

    predictions = model.predict(
        image_array,
        verbose=0
    )

    predicted_index = int(
        np.argmax(predictions[0])
    )

    confidence = float(
        predictions[0][predicted_index]
    )

    predicted_class = class_names[predicted_index]

    # --------------------------------------------------------
    # GET DISEASE INFORMATION
    # --------------------------------------------------------

    info = DISEASE_INFO.get(
        predicted_class,
        {
            "disease": predicted_class,
            "description": "No additional information available.",
            "treatment": "Consult an agricultural expert.",
            "prevention": "Monitor the plant regularly."
        }
    )

    # --------------------------------------------------------
    # SUCCESS RESPONSE
    # --------------------------------------------------------

    return {
        "valid_leaf": True,
        "prediction": predicted_class,
        "confidence": round(
            confidence * 100,
            2
        ),
        "disease": info["disease"],
        "description": info["description"],
        "treatment": info["treatment"],
        "prevention": info["prevention"]
    }