# Raspberry Pi Kiosk Testing Guide

This guide details how to set up, configure, and test the CopyFlow Kiosk software on a Raspberry Pi.

## 1. System Requirements & Prerequisites
**Hardware**: Raspberry Pi 3B+ / 4 / 5 or Zero 2 W (with Wi-Fi).
**OS**: Raspberry Pi OS (Bookworm or Bullseye recommend).

### Install System Packages
Open a terminal on your Pi and install the necessary system tools:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip hostapd dnsmasq iptables cups
```
* `hostapd`: Creates the Wi-Fi Hotspot.
* `dnsmasq`: Handles DHCP and DNS (Captive Portal).
* `cups`: Common Unix Printing System.

## 2. Project Setup

Navigate to the project directory:

```bash
cd ~/Projects/CopyFlow/PI_Kiosk  # Adjust path if different
```

### Setup Python Environment
Create a virtual environment to isolate dependencies:

```bash
# Create venv
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

> **Note**: If you see an error `ensurepip is not available`, ensure you ran `sudo apt install python3-venv`.

## 3. Configuration

1. **Environment Variables**:
   Copy the example configuration:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` using `nano .env`:
   - Set `ENABLE_HOTSPOT=true` to enable the hotspot features.
   - Set `KIOSK_ID=pi-01`.
   - Ensure `BACKEND_URL` points to your main backend (or leave mock URL for offline testing).

2. **Network Config Check**:
   Verify `scripts/config/hostapd.conf` contains:
   - SSID: `CopyFlow-Print`
   - Password: `copyflow123`

## 4. Verification (Dry Run)

We have provided a script to verify the application logic (API, Uploads, Printing Logic) works correctly before enabling hardware.

**Run the Verification Script**:
```bash
# Ensure venv is active
source venv/bin/activate

python verify_deployment.py
```

**Expected Output**:
```
🚀 Starting CopyFlow Kiosk Verification
...
[1/4] Testing Health Check... ✅
[2/4] Testing File Upload... ✅
...
✨ VERIFICATION COMPLETE - SYSTEM READY ✨
```
If this script fails, check the error message. It usually indicates missing dependencies or a crash in the app.

## 5. Live Testing (Manual)

### Step A: Start the Hotspot manually
To test if the Wi-Fi creates successfully without running the full app:

```bash
sudo ./scripts/hotspot_start.sh
```
* **Verify**: Use your phone to search for Wi-Fi networks. You should see `CopyFlow-Print`. Connect to it (Pass: `copyflow123`).
* **Captive Portal**: Try checking `http://neverssl.com` on your phone; it should redirect to the Kiosk.

### Step B: Start the Application
Run the main server:

```bash
# In the project root with venv active
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
* The app logs should show `🔥 [Network] Enabling Hotspot Mode...` (if configured in .env).

### Step C: Stop the Hotspot
When finished:
```bash
sudo ./scripts/hotspot_stop.sh
```

## 6. Troubleshooting Common Errors

### "bind: Address already in use"
Another service (like `wpa_supplicant` or generic NetworkManager) might be using `wlan0`.
* **Fix**: The `hotspot_start.sh` attempts to kill conflicts, but you may need to manually `sudo systemctl stop NetworkManager`.

### "Permission denied" logic errors
Network scripts require `sudo`.
* **Fix**: Ensure the user running the app has permissions, or run the scripts manualy with sudo as shown above.

### "ModuleNotFoundError: No module named 'requests'"
* **Fix**: `pip install -r requirements.txt`.

### "ensurepip is not available"
* **Fix**: `sudo apt install python3-venv`.

