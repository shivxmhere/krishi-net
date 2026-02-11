import requests
import os
import sys

# Configuration
BASE_URL = "http://localhost:8000"
HEALTH_URL = f"{BASE_URL}/health"
DETECT_URL = f"{BASE_URL}/api/detect"
SAMPLE_IMAGE = os.path.join(os.path.dirname(__file__), "sample_leaf.jpg")

def test_health():
    print("Testing /health endpoint...", end=" ")
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Validation
        assert data.get("status") == "ok"
        assert "app" in data
        assert "version" in data
        
        print("✅ PASS")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_detect():
    print("Testing POST /api/detect endpoint...", end=" ")
    if not os.path.exists(SAMPLE_IMAGE):
        print(f"❌ FAIL: {SAMPLE_IMAGE} not found.")
        return False

    try:
        with open(SAMPLE_IMAGE, "rb") as f:
            files = {"file": ("sample_leaf.jpg", f, "image/jpeg")}
            response = requests.post(DETECT_URL, files=files, timeout=10)
        
        response.raise_for_status()
        data = response.json()
        
        # Validation based on FRONTEND_INTEGRATION.md
        required_fields = ["success", "disease_name", "confidence", "severity", "treatment"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        assert data["success"] is True
        assert isinstance(data["treatment"], dict)
        assert "steps" in data["treatment"]
        assert isinstance(data["treatment"]["steps"], list)
        
        print(f"✅ PASS (Detected: {data['disease_name']})")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
        return False

if __name__ == "__main__":
    print(f"Starting Integration Tests on {BASE_URL}\n" + "-"*40)
    
    health_pass = test_health()
    detect_pass = test_detect()
    
    print("-"*40)
    if health_pass and detect_pass:
        print("OVERALL RESULT: ✅ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("OVERALL RESULT: ❌ SOME TESTS FAILED")
        sys.exit(1)
