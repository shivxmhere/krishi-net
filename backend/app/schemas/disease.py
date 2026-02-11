"""
Pydantic Response Schemas — Disease Detection
Defines the exact shape of API responses for Swagger documentation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class TreatmentSchema(BaseModel):
    """Treatment steps returned as part of a detection result."""
    steps: List[str] = Field(..., description="Ordered list of treatment instructions")


class DetectionResponse(BaseModel):
    """Response schema for POST /api/detect"""
    success: bool = Field(..., description="Whether the detection completed successfully")
    disease_name: str = Field(..., description="Predicted disease name in English")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence score (0.0–1.0)")
    disease_name_hi: Optional[str] = Field(None, description="Disease name in Hindi (if available)")
    severity: str = Field("UNKNOWN", description="Severity level: LOW, MEDIUM, HIGH, or UNKNOWN")
    treatment: TreatmentSchema = Field(..., description="Treatment recommendation")

    model_config = {"from_attributes": True}
