from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Literal
import uvicorn
import numpy as np
from PIL import Image
import io
import tensorflow as tf
from model_utils import CLASS_LABELS, TREATMENT_INFO
import os

# Global variable to hold the model
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    global model
    model_path = "model/plant_disease_model.h5"
    if os.path.exists(model_path):
        print(f"Loading model from {model_path}...")
        try:
            model = tf.keras.models.load_model(model_path)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")
            model = None
    else:
        print(f"Model file not found at {model_path}. Please run create_dummy_model.py or upload a real model.")
        model = None
    yield
    # Clean up if needed
    model = None

app = FastAPI(lifespan=lifespan)

# -----------------------------------------------------------------------------
# Data Models
# -----------------------------------------------------------------------------
class PredictionResponse(BaseModel):
    disease: str
    confidence: float
    severity: str
    treatment: List[str]

# -----------------------------------------------------------------------------
# Error Handling
# -----------------------------------------------------------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Internal Error: {exc}")
    return JSONResponse(status_code=500, content={"error": "Internal ML Service Error"})

# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------
@app.get("/health")
def health_check():
    status = "ready" if model is not None else "model_not_loaded"
    return {"status": "ok", "service": "ml-inference", "model_status": status}

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Resize to 224x224 and normalize to [0,1]."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = image_array / 255.0  # Normalize to [0, 1]
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension: (1, 224, 224, 3)
    return image_array

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    global model
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    try:
        contents = await file.read()
        processed_image = preprocess_image(contents)

        # Inference
        predictions = model.predict(processed_image)
        # predictions is typically [[prob1, prob2, ...]]
        
        confidence = float(np.max(predictions[0]))
        class_idx = int(np.argmax(predictions[0]))
        
        disease_name = CLASS_LABELS.get(class_idx, "Unknown")
        
        # Get treatment info
        info = TREATMENT_INFO.get(disease_name, TREATMENT_INFO["Unknown"])

        return {
            "disease": disease_name,
            "confidence": round(confidence, 2),
            "severity": info["severity"],
            "treatment": info["treatments"]
        }

    except Exception as e:
        print(f"Prediction Error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
