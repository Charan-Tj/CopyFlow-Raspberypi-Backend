# 🚀 CopyFlow Kiosk - Deployment Guide

Follow these steps to get the Kiosk running on your Raspberry Pi.

## 1. System Requirements
Install necessary system packages for Hotspot and Python environment:
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv hostapd dnsmasq
```

## 2. Setup Python Environment
Create a virtual environment to isolate dependencies:
```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Configuration
Create a `.env` file from the example:
```bash
cp .env.example .env
```
Edit `.env` to set your Kiosk ID and Secret (if you have them from the backend), or leave defaults for testing.
```bash
nano .env
```

## 5. Running the Service (Dev/Test Mode)
To run the server manually:
```bash
# If you are in the virtual env
uvicorn src.main:app --host 0.0.0.0 --port 8000
```
Then verify it's working:
- **Health Check**: `curl http://localhost:8000/health`
- **Dev UI**: Open Browser to `http://<PI_IP>:8000/__dev`

## 6. Using Hotspot Mode
To enable the "CopyFlow-Print" Wi-Fi:
1.  Open `.env` and set `ENABLE_HOTSPOT=True`.
2.  Run the server with `sudo` (Hotspot requires root to change Wifi settings):
    ```bash
    # Note: Using sudo with venv requires calling the venv python directly
    sudo ./venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
    ```
3.  Connect your phone to Wi-Fi `CopyFlow-Print` (Pass: `copyflow123`).
4.  It should redirect you to the Upload Page.

## 7. Troubleshooting
- **Port 8000 in use?** Find and kill: `sudo lsof -i :8000` then `kill -9 <PID>`.
- **Hotspot fails?** Run clean up: `sudo scripts/hotspot_stop.sh`.
