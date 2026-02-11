"""
Phase 3 Verification Script
Tests model loading and inference on a synthetic image.
"""
import os
import sys
import numpy as np
from PIL import Image

# Add backend to path to import ml_service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

try:
    import tensorflow as tf
    from app.services.ml_service import ml_service
except ImportError as e:
    print(f"Error: Missing dependencies or path issue: {e}")
    sys.exit(1)

def verify_model():
    print(f"Checking model at: {os.path.abspath('../ai-models/trained_models/disease_model.h5')}")
    print(f"Current ML Mode: {ml_service.mode}")
    
    if ml_service.mode != "REAL":
        print("❌ FAILED: Model is not in REAL mode. Check logs/paths.")
        return False
    
    print(f"✅ Success: Model loaded with {len(ml_service.classes)} classes.")
    
    # Test Prediction
    print("Running test inference on dummy image...")
    dummy_img = Image.new('RGB', (256, 256), color='green')
    name, conf = ml_service.predict(dummy_img)
    
    print(f"✅ Result: {name} (Confidence: {conf:.2%})")
    return True

if __name__ == "__main__":
    if verify_model():
        print("\n--- PHASE 3 VERIFICATION PASSED ---")
        sys.exit(0)
    else:
        print("\n--- PHASE 3 VERIFICATION FAILED ---")
        sys.exit(1)
