#!/bin/bash
set -e

# Activate Virtual Env
source venv/bin/activate

echo "[*] Starting CopyFlow Kiosk System..."

# Pre-cleanup ports
fuser -k 8000/tcp >/dev/null 2>&1 || true
fuser -k 3000/tcp >/dev/null 2>&1 || true

# 1. Start Mock Backend in Background
echo "[*] Starting Mock Backend (Port 3000)..."
python mock_backend.py > mock_backend.log 2>&1 &
MOCK_PID=$!

# 2. Wait for Mock Backend to be ready
echo "   Waiting for Mock Backend..."
sleep 2

# 3. Start Kiosk API (Main App)
echo "[*] Starting Kiosk API (Port 8000)..."
# We use exec so uvicorn takes over this shell process, 
# BUT we want to trap SIGINT to kill the mock backend first.

cleanup() {
    echo ""
    echo "[*] Shutting down..."
    kill $MOCK_PID 2>/dev/null || true
    # Stop hotspot if it was started by the app (app handles that on shutdown usually, but let's be safe)
    # sudo ./scripts/hotspot_stop.sh # Optional: let the user decide if they want to stop wifi
}

trap cleanup EXIT INT TERM

uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

