"""
Disease Detection Endpoint
Orchestrates: Image Upload → ML Prediction → DB Lookup → Response
"""
import io
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from PIL import Image
from app.database import get_db
from app.models.disease import Disease
from app.services.ml_service import ml_service
from app.schemas.disease import DetectionResponse
from app.config import settings
from app.services.auth_service import get_current_user
from app.models.user import User
from app.core.limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/detect",
    response_model=DetectionResponse,
    responses={
        400: {"description": "Invalid image file or format"},
        413: {"description": "Image exceeds 5MB limit"},
        422: {"description": "Missing required file field"},
        500: {"description": "ML prediction or database failure"},
    },
)
@limiter.limit("10/minute")
async def detect_disease(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image (JPEG/PNG).")

    # 2. Read and validate file size
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="Image exceeds 5MB limit.")

    # 3. Parse image
    try:
        image = Image.open(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read image. Ensure it is a valid JPEG/PNG.")

    # 4. ML Model Prediction
    try:
        disease_name, confidence = ml_service.predict(image)
        logger.info(f"Detection successful for {current_user.email}", extra={
            "disease": disease_name,
            "confidence": round(confidence, 4),
            "user_email": current_user.email
        })
    except Exception as e:
        logger.error(f"ML prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"ML prediction failed: {e}")

    # 5. Disease DB Lookup
    try:
        disease_record = db.query(Disease).filter(Disease.name == disease_name).first()
    except Exception as e:
        logger.error(f"Database lookup failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database lookup failed: {e}")

    # 6. Build response
    response_data = {
        "success": True,
        "disease_name": disease_name,
        "confidence": confidence,
    }

    if disease_record:
        # Treatment is stored as newline-separated text in the DB.
        response_data.update({
            "disease_name_hi": disease_record.name_hi,
            "severity": disease_record.severity,
            "treatment": {
                "steps": disease_record.treatment.split('\n') if disease_record.treatment else []
            }
        })
    else:
        response_data.update({
            "disease_name_hi": None,
            "severity": "UNKNOWN",
            "treatment": {
                "steps": ["Consult a local agricultural expert."]
            }
        })

    return response_data
