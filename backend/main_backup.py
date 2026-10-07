from pathlib import Path
import json

import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from tensorflow.keras.models import load_model


# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "plant_disease_model.keras"
CLASS_NAMES_PATH = BASE_DIR / "models" / "class_names.json"


# ==========================================
# Load model and class names
# ==========================================

print("Loading plant disease model...")

model = load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
    class_names = json.load(file)

print("Model loaded successfully!")
print("Number of classes:", len(class_names))


# ==========================================
# FastAPI application
# ==========================================

app = FastAPI(
    title="Plant Disease Detection API",
    description="AI-based plant disease detection from leaf images",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Disease information
# ==========================================

DISEASE_INFO = {
    "Apple___Apple_scab": {
        "disease": "Apple Scab",
        "description": "A fungal disease that causes dark olive or brown spots on apple leaves and fruit.",
        "treatment": "Remove infected leaves and fruit. Use an appropriate fungicide according to local agricultural guidance.",
        "prevention": "Keep the orchard clean, remove fallen infected leaves, and maintain good air circulation."
    },

    "Apple___healthy": {
        "disease": "Healthy Apple Leaf",
        "description": "The uploaded apple leaf appears healthy.",
        "treatment": "No disease treatment is required.",
        "prevention": "Continue regular monitoring, proper watering, nutrition, and good orchard hygiene."
    },

    "Corn_(maize)___Common_rust_": {
        "disease": "Corn Common Rust",
        "description": "A fungal disease that produces small reddish-brown rust-colored spots on corn leaves.",
        "treatment": "Use suitable fungicide treatment when recommended and manage heavily affected plants.",
        "prevention": "Use resistant varieties and maintain good field management practices."
    },

    "Corn_(maize)___healthy": {
        "disease": "Healthy Corn Leaf",
        "description": "The uploaded corn leaf appears healthy.",
        "treatment": "No disease treatment is required.",
        "prevention": "Maintain proper irrigation, nutrition, and regular crop monitoring."
    },

    "Potato___Early_blight": {
        "disease": "Potato Early Blight",
        "description": "A fungal disease that causes dark spots and target-like rings on potato leaves.",
        "treatment": "Remove severely affected plant material and use an appropriate fungicide when recommended.",
        "prevention": "Use healthy planting material, rotate crops, and avoid prolonged leaf wetness."
    },

    "Potato___Late_blight": {
        "disease": "Potato Late Blight",
        "description": "A serious disease that causes dark, water-soaked lesions on potato leaves.",
        "treatment": "Remove severely infected material and use appropriate fungicide management according to agricultural guidance.",
        "prevention": "Use resistant varieties where available, avoid excessive moisture, and monitor crops regularly."
    },

    "Potato___healthy": {
        "disease": "Healthy Potato Leaf",
        "description": "The uploaded potato leaf appears healthy.",
        "treatment": "No disease treatment is required.",
        "prevention": "Continue proper irrigation, nutrition, crop rotation, and regular monitoring."
    },

    "Tomato___Early_blight": {
        "disease": "Tomato Early Blight",
        "description": "A fungal disease that commonly causes dark spots with concentric rings on tomato leaves.",
        "treatment": "Remove affected leaves and use an appropriate fungicide when recommended.",
        "prevention": "Improve air circulation, avoid overhead watering, and remove infected plant debris."
    },

    "Tomato___Late_blight": {
        "disease": "Tomato Late Blight",
        "description": "A disease that can cause dark, water-soaked lesions on tomato leaves and stems.",
        "treatment": "Remove infected plant material and use appropriate fungicide management according to agricultural guidance.",
        "prevention": "Avoid prolonged leaf wetness, provide good air circulation, and monitor plants regularly."
    },

    "Tomato___healthy": {
        "disease": "Healthy Tomato Leaf",
        "description": "The uploaded tomato leaf appears healthy.",
        "treatment": "No disease treatment is required.",
        "prevention": "Maintain proper watering, nutrition, air circulation, and regular monitoring."
    }
}


# ==========================================
# Home endpoint
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Plant Disease Detection API is running"
    }


# ==========================================
# Prediction endpoint
# ==========================================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Check file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image file."
        )

    try:
        # Read uploaded image
        image_data = await file.read()

        image = Image.open(
            __import__("io").BytesIO(image_data)
        ).convert("RGB")

        # Resize image
        image = image.resize((224, 224))

        # Convert image to NumPy array
        image_array = np.array(image)

        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)

        
        # Make prediction
        predictions = model.predict(image_array, verbose=0)

        predicted_index = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_index])

        predicted_class = class_names[predicted_index]

        # Get disease information
        info = DISEASE_INFO.get(
            predicted_class,
            {
                "disease": predicted_class,
                "description": "Information is not available.",
                "treatment": "Consult a qualified agricultural professional.",
                "prevention": "Monitor the plant regularly."
            }
        )

        return {
            "prediction": predicted_class,
            "confidence": round(confidence * 100, 2),
            "disease": info["disease"],
            "description": info["description"],
            "treatment": info["treatment"],
            "prevention": info["prevention"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )