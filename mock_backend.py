from fastapi import FastAPI, HTTPException
import uvicorn
import uuid
import hmac
import hashlib
import time
import os

# Configuration matching the Kiosk
KIOSK_SECRET = "supersecret123"
PORT = 3000

app = FastAPI(title="Mock Backend")

@app.post("/kiosks/{kiosk_id}/jobs")
async def register_job(kiosk_id: str, job_data: dict):
    print(f"📦 [MOCK] Registering job for Kiosk {kiosk_id}: {job_data}")
    # Generate a random job ID
    job_id = str(uuid.uuid4())
    return {
        "job_id": job_id,
        "payable_amount": 50,
        "currency": "INR",
        "status": "created"
    }

@app.get("/kiosks/{kiosk_id}/jobs/{job_id}/token")
async def get_token(kiosk_id: str, job_id: str):
    print(f"🔑 [MOCK] Generating token for Job {job_id}")
    
    # Generate valid token
    expiry = int(time.time()) + 3600 # 1 hour
    payload = f"{job_id}|{expiry}".encode('utf-8')
    signature = hmac.new(KIOSK_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    token = f"{job_id}|{expiry}|{signature}"
    
    return {"token": token}

if __name__ == "__main__":
    print(f"🚀 Mock Backend running on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
