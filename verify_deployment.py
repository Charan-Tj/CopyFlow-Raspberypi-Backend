import requests
import hmac
import hashlib
import time
import os
import shutil
from unittest.mock import MagicMock
import sys
from fastapi.testclient import TestClient
from src.main import app, backend_client

# Setup
client = TestClient(app)
kiosk_secret = "supersecret123".encode()
job_id = "test-job-autogen"
file_path = f"temp_uploads/{job_id}.pdf"

# Clean up previous run
if os.path.exists(file_path):
    os.remove(file_path)

print("[*] Starting CopyFlow Kiosk Verification")

# 1. Test Health
print("\n[1/4] Testing Health Check...")
resp = client.get("/health")
if resp.status_code == 200:
    print(f"[OK] Online: {resp.json()}")
else:
    print(f"[FAILED] Failed: {resp.status_code}")
    sys.exit(1)

# 2. Test Upload (Mocking Backend Register)
print("\n[2/4] Testing File Upload...")
# Mock register_job to return our specific job_id
backend_client.register_job = MagicMock(return_value={
    "job_id": job_id,
    "payable_amount": 50,
    "currency": "INR"
})

# Create dummy PDF
dummy_pdf = "test_data.pdf"
with open(dummy_pdf, "wb") as f:
    f.write(b"%PDF-1.4 ... dummy content ...")

with open(dummy_pdf, "rb") as f:
    resp = client.post("/upload", files={"file": (dummy_pdf, f, "application/pdf")})

# Cleanup dummy source
if os.path.exists(dummy_pdf):
    os.remove(dummy_pdf)

if resp.status_code == 200 and resp.json().get("job_id") == job_id:
    print("[OK] Upload Successful")
    # Verify the file was moved to temp_uploads/{job_id}.pdf
    if os.path.exists(file_path):
        print(f"[OK] Internal File Stored: {file_path}")
    else:
        print("[FAILED] Internal File Missing!")
        sys.exit(1)
else:
    print(f"[FAILED] Upload Failed: {resp.text}")
    sys.exit(1)

# 3. Test Print with Valid Token
print("\n[3/4] Testing Print (Authorized)...")

# Generate Valid Token
expiry = int(time.time()) + 3600
payload = f"{job_id}|{expiry}".encode('utf-8')
signature = hmac.new(kiosk_secret, payload, hashlib.sha256).hexdigest()
valid_token = f"{job_id}|{expiry}|{signature}"

# Mock get_print_token
backend_client.get_print_token = MagicMock(return_value=valid_token)

resp = client.post(f"/print/{job_id}")

if resp.status_code == 200 and resp.json()["status"] == "printed":
    print("[OK] Print Request Successful")
else:
    print(f"[FAILED] Print Failed: {resp.text}")
    sys.exit(1)

# 4. Verify Cleanup
print("\n[4/4] Verifying Cleanup...")
if not os.path.exists(file_path):
    print("[OK] File removed from temp storage")
else:
    print("[FAILED] File still exists! (Security Risk)")
    sys.exit(1)

print("\n[*] VERIFICATION COMPLETE - SYSTEM READY [*]")
