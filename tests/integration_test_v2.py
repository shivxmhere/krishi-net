"""
Phase 4 Integration Test — Authentication & Protected Disease Detection
Verifies registration, login, and token-based access to /api/detect.
"""
import requests
import os
import sys

BASE_URL = "http://localhost:8000/api"
TEST_ACCOUNT = {
    "email": "testuser@krishinet.com",
    "password": "strong_test_password_123"
}

def test_auth_flow():
    print("--- 🔐 TESTING AUTH FLOW ---")
    
    # 1. Register
    print("1. Registering user...")
    resp = requests.post(f"{BASE_URL}/auth/register", json=TEST_ACCOUNT)
    if resp.status_code == 201:
        print("✅ User Registered Successfully")
    elif resp.status_code == 400:
        print("⚠️ User already exists (OK for test retry)")
    else:
        print(f"❌ Registration Failed: {resp.text}")
        return None

    # 2. Login
    print("2. Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/login", json=TEST_ACCOUNT)
    if resp.status_code != 200:
        print(f"❌ Login Failed: {resp.text}")
        return None
    
    token = resp.json().get("access_token")
    print("✅ Login Successful. Token obtained.")
    return token

def test_protected_detection(token):
    print("\n--- 🪴 TESTING PROTECTED DETECTION ---")
    
    # Generate a sample image if not exists
    sample_path = "sample_leaf.jpg"
    if not os.path.exists(sample_path):
        from PIL import Image
        Image.new('RGB', (256, 256), color='green').save(sample_path)

    # 1. Test Without Token (Expect 401)
    print("1. Testing WITHOUT token (should fail)...")
    with open(sample_path, "rb") as f:
        resp = requests.post(f"{BASE_URL}/detect", files={"file": f})
    if resp.status_code == 401:
        print("✅ Properly Rejected (401 Unauthorized)")
    else:
        print(f"❌ Security Failure: Got {resp.status_code} instead of 401")

    # 2. Test With Token
    print("2. Testing WITH valid token (should pass)...")
    headers = {"Authorization": f"Bearer {token}"}
    with open(sample_path, "rb") as f:
        resp = requests.post(f"{BASE_URL}/detect", files={"file": f}, headers=headers)
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ Detection Success: {data.get('disease_name')} ({data.get('confidence'):.2f})")
    else:
        print(f"❌ Detection Failed: {resp.text}")

if __name__ == "__main__":
    # Ensure server is running (User should have it running or I can startup if needed)
    # For now, we assume local dev server.
    auth_token = test_auth_flow()
    if auth_token:
        test_protected_detection(auth_token)
        print("\n🏆 PHASE 4 VERIFICATION COMPLETE!")
    else:
        print("\n❌ PHASE 4 VERIFICATION FAILED at Auth check.")
