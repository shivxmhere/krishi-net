"""
Disease Model — SQLAlchemy ORM definition
Maps to the 'diseases' table in PostgreSQL.
"""
from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    name_hi = Column(String, nullable=True)
    symptoms = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    severity = Column(String, default="MEDIUM")
