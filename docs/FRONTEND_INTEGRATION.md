# Krishi-Net Frontend Integration Guide

**Base URL**: `http://localhost:8000` (Local) / `http://10.0.2.2:8000` (Android Emulator)

---

## 🚀 Quick Check
Run this curl command to verify connectivity:
```bash
curl http://localhost:8000/health
```
**Expected Response:**
```json
{
  "status": "ok",
  "app": "Krishi-Net API",
  "version": "1.0.0"
}
```

---

## 🍃 Disease Detection Endpoint

**POST** `/api/detect`

Upload a leaf image to get disease diagnosis and treatment recommendations.

### 1. Request Format

- **Content-Type**: `multipart/form-data`
- **Auth**: None required (currently open)

| Field | Type | Required | Constraints |
| :--- | :--- | :--- | :--- |
| `file` | File (Binary) | ✅ Yes | • Format: **JPEG** or **PNG**<br>• Max Size: **5MB** |

#### React Native Example (Axios)
```javascript
const formData = new FormData();
formData.append('file', {
  uri: photo.uri,       // e.g. 'file:///...'
  type: 'image/jpeg',   // or 'image/png'
  name: 'photo.jpg',
});

try {
  const response = await axios.post(
    `${API_BASE_URL}/api/detect`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );
  console.log(response.data);
} catch (error) {
  console.error(error.response.data);
}
```

#### Curl Example
```bash
curl -X POST http://localhost:8000/api/detect \
  -F "file=@/path/to/leaf.jpg"
```

---

### 2. Response Examples

#### ✅ 200 OK — Success
```json
{
  "success": true,
  "disease_name": "Apple scab",
  "confidence": 0.98,
  "disease_name_hi": "सेब की पपड़ी (Apple Scab)",
  "severity": "MEDIUM",
  "treatment": {
    "steps": [
      "Remove infected leaves immediately",
      "Apply Mancozeb 75% WP @ 2g/liter",
      "Ensure good air circulation"
    ]
  }
}
```
**Field Breakdown:**
- `success`: Always `true` for 200 OK.
- `disease_name`: English name of the disease.
- `confidence`: Float between 0.0 and 1.0.
- `disease_name_hi`: Localized Hindi name (if available, else null).
- `severity`: `LOW`, `MEDIUM`, `HIGH`, or `UNKNOWN`.
- `treatment.steps`: Array of strings, each representing one step.

---

#### ❌ 400 Bad Request — Invalid File
**Scenario**: Uploading a PDF or non-image file.
```json
{
  "detail": "File must be an image (JPEG/PNG)."
}
```

#### ❌ 413 Payload Too Large
**Scenario**: Image is larger than 5MB.
```json
{
  "detail": "Image exceeds 5MB limit."
}
```

#### ❌ 422 Unprocessable Entity
**Scenario**: Missing the `file` field in the request.
```json
{
  "detail": [
    {
      "loc": ["body", "file"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```
> **⚠️ Note:** 422 errors return `detail` as an **Array** of objects, whereas other errors return `detail` as a **String**. Frontend must handle both types.

#### ❌ 500 Internal Server Error
**Scenario**: Database or ML model failure.
```json
{
  "detail": "ML prediction failed: <error message>"
}
```

---

## 🌐 CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:19006` (Expo Web Preview)
- `http://localhost:8081` (Metro Bundler)

> **Note:** Native Android/iOS apps do not use CORS. This setting only affects web browser testing.

To check your current CORS settings, open `backend/.env` and look for `CORS_ORIGINS`.
