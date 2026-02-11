"""
Database Configuration
Creates connection to PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True if settings.DEBUG else False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()


def get_db():
    """
    Dependency for FastAPI routes
    Creates new database session for each request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()