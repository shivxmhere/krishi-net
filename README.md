# 🪴 Krishi-Net: AI-Powered Crop Disease Detection

Krishi-Net is a production-grade AI platform designed to empower farmers in Jammu & Kashmir. It provides real-time crop disease detection and localized treatment recommendations using deep learning (MobileNetV2) and a robust FastAPI backend.

## 🚀 Key Features
- **AI-Driven Detection**: Support for 38 classes of diseases/healthy states across 14 crops (Apple, Corn, Tomato, etc.).
- **Localized Support**: Hindi/local language naming and treatment steps.
- **Secure by Design**: JWT-based authentication, password hashing (bcrypt), and rate limiting.
- **Production Ready**: Structured JSON logging, request tracking, and health monitoring.
- **Market Intelligence**: (Experimental) Price tracking and forecasting architecture.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python 3.11)
- **ML Engine**: TensorFlow 2.15 (MobileNetV2 Model)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Security**: JWT (python-jose), Bcrypt, SlowAPI (Rate Limiting)
- **Monitoring**: Structured Logging with JSON format

## ⚙️ Quick Start

### 1. Prerequisites
- Python 3.11+
- PostgreSQL
- TensorFlow compatible environment

### 2. Installation
```bash
git clone https://github.com/shiva/krishi-net.git
cd krishi-net/backend
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the `backend/` directory:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/krishinet_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
DISEASE_MODEL_PATH=../ai-models/trained_models/disease_model.h5
```

### 4. Running the App
```bash
uvicorn app.main:app --reload
```
View Interactive Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📖 API Documentation
Detailed endpoint documentation can be found in [frontend_integration_guide.md](./backend/frontend_integration_guide.md).

## 🛡️ Security
The API is protected by JWT. Register at `/api/auth/register` and obtain a token at `/api/auth/login`. Use this token in the `Authorization: Bearer <token>` header for detection requests.
