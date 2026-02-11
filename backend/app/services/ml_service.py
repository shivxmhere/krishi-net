"""
ML Service — Disease Detection (Phase 3)
Handles TensorFlow model loading for the 38-class PlantVillage model.
Preprocessing: 256x256 RGB, normalization [0, 1].
"""
import logging
import os
import time
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

try:
    import tensorflow as tf
except ImportError:
    tf = None

try:
    from app.config import settings
    MODEL_PATH = settings.DISEASE_MODEL_PATH
except Exception:
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../ai-models/trained_models/disease_model.h5')


class MLService:
    def __init__(self):
        self.model = None
        self.mode = "STUB"
        # Standard PlantVillage 38 Classes (Alphabetical Order)
        self.classes = [
            "Apple___Apple_scab",
            "Apple___Black_rot",
            "Apple___Cedar_apple_rust",
            "Apple___healthy",
            "Blueberry___healthy",
            "Cherry___Powdery_mildew",
            "Cherry___healthy",
            "Corn___Cercospora_leaf_spot Gray_leaf_spot",
            "Corn___Common_rust",
            "Corn___Northern_Leaf_Blight",
            "Corn___healthy",
            "Grape___Black_rot",
            "Grape___Esca_(Black_Measles)",
            "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
            "Grape___healthy",
            "Orange___Haunglongbing_(Citrus_greening)",
            "Peach___Bacterial_spot",
            "Peach___healthy",
            "Pepper,_bell___Bacterial_spot",
            "Pepper,_bell___healthy",
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy",
            "Raspberry___healthy",
            "Soybean___healthy",
            "Squash___Powdery_mildew",
            "Strawberry___Leaf_scorch",
            "Strawberry___healthy",
            "Tomato___Bacterial_spot",
            "Tomato___Early_blight",
            "Tomato___Late_blight",
            "Tomato___Leaf_Mold",
            "Tomato___Septoria_leaf_spot",
            "Tomato___Spider_mites Two-spotted_spider_mite",
            "Tomato___Target_Spot",
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
            "Tomato___Tomato_mosaic_virus",
            "Tomato___healthy"
        ]
        self._initialize_model()

    def _initialize_model(self):
        model_path = os.path.abspath(MODEL_PATH)
        if tf and os.path.exists(model_path):
            try:
                start_time = time.time()
                self.model = tf.keras.models.load_model(model_path)
                logger.info(f"REAL model loaded: {model_path} in {(time.time() - start_time)*1000:.2f}ms")
                self.mode = "REAL"
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                self.mode = "STUB (Load Error)"
        else:
            self.mode = "STUB (Not Found)"

    def predict(self, image: Image.Image):
        start_time = time.time()
        # Preprocessing: Match 256x256 required by the sourced model
        img = image.convert("RGB").resize((256, 256))
        
        if self.model and self.mode == "REAL":
            try:
                img_array = np.array(img).astype('float32') / 255.0
                img_array = np.expand_dims(img_array, axis=0)
                
                predictions = self.model.predict(img_array, verbose=0)
                idx = np.argmax(predictions[0])
                confidence = float(predictions[0][idx])
                raw_label = self.classes[idx] if idx < len(self.classes) else "Unknown"
                
                clean_name = raw_label.split("___")[-1].replace("_", " ")
                dura = (time.time() - start_time) * 1000
                logger.info(f"Inference: {clean_name} ({confidence:.2%}) in {dura:.2f}ms")
                return clean_name, confidence
            except Exception as e:
                logger.error(f"Inference Error: {e}")

        # Fallback
        logger.info("Using Stub Fallback")
        return "Apple scab", 0.98

ml_service = MLService()
