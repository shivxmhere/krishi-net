"""
Database Seeder
Populates the diseases table with initial data on first startup.
"""
import logging
from app.database import SessionLocal
from app.models.disease import Disease

logger = logging.getLogger(__name__)


def init_db():
    """Seed diseases table if empty."""
    db = SessionLocal()
    try:
        existing = db.query(Disease).first()

        if not existing:
            diseases = [
                Disease(
                    name="Apple scab",
                    name_hi="सेब की पपड़ी (Apple Scab)",
                    symptoms="Velvety, olive-green to black spots on leaves and fruit.",
                    treatment="Remove infected leaves.\nApply Mancozeb 75% WP @ 2g/liter.",
                    severity="MEDIUM"
                ),
                Disease(
                    name="Black rot",
                    name_hi="काला सड़न (Black Rot)",
                    symptoms="Brown, circular spots on leaves; rotting fruit.",
                    treatment="Prune dead wood.\nApply Captan or Thiram.",
                    severity="HIGH"
                ),
                Disease(
                    name="healthy",
                    name_hi="स्वस्थ (Healthy)",
                    symptoms="None. The plant looks vigorous.",
                    treatment="Continue regular care and monitoring.",
                    severity="LOW"
                )
            ]

            db.add_all(diseases)
            db.commit()
            logger.info("Database seeded with %d diseases.", len(diseases))
        else:
            logger.info("Database already seeded. Skipping.")
    finally:
        db.close()
