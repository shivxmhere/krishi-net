# Backend Integration Tests

This directory contains integration tests for the Krishi-Net FastAPI backend. These tests verify the core API contract as documented in `FRONTEND_INTEGRATION.md`.

## 📂 Contents
- `integration_test.py`: Main Python test script using the `requests` library.
- `sample_leaf.jpg`: A 224x224 sample image generated for testing the detection endpoint.

## 🛠️ Prerequisites
- Python 3.10+
- `requests` library installed:
  ```bash
  pip install requests
  ```
- **Backend must be running** at `http://localhost:8000`.
  ```bash
  cd backend
  uvicorn app.main:app --reload
  ```

## 🚀 How to Run
From the root of the project:
```bash
python tests/integration_test.py
```

## ✅ What is tested?
1. **Health Check**: `GET /health` must return `200 OK` and valid app metadata.
2. **Disease Detection**: `POST /api/detect` with an image file must return `200 OK` and follow the exact JSON schema (including `success`, `disease_name`, `confidence`, `severity`, and `treatment`).
