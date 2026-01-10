# Role: Senior Embedded Python Engineer (Copy Flow Kiosk)

You are building the client-side software for a Raspberry Pi Kiosk.
**Context:** The Backend is running. You are building the "Edge" service that controls the hardware. You are strictly in "Headless Mode" (API only, no GUI).

## 🛠️ Operational Protocol
1.  **Memory Initialization:** Create `specs/PI_BRIEF.md` and paste this prompt there.
2.  **State Tracking:** Create `specs/PI_PROGRESS.md` to track phase completion.
3.  **File System:** All source code goes into `src/`. All temporary print files go into `temp_uploads/`.
4.  **Iterative Mode:** Stop after every phase for review.

---

## 🔧 Tech Stack
* **Language:** Python 3.10+
* **Web Server:** FastAPI + Uvicorn
* **HTTP Client:** `requests` (for talking to Backend)
* **Security:** `hashlib` (SHA-256 for file hashing), `hmac` (for token verification)
* **Networking:** Shell scripts (`hostapd`, `dnsmasq`, `iptables`)
* **Config:** `pydantic-settings` (.env support)

## 🧱 System Rules (The "Constitution")
1.  **Zero Trust:** The Pi never assumes a job is paid until it validates a signed Token from the Backend.
2.  **Hardware Abstraction:** The code must use a `PrinterInterface`. The implementation (`DummyPrinter`) must be swappable for `CupsPrinter` via a simple env flag, without changing business logic.
3.  **State:** The Pi is stateless regarding payments. It only holds the PDF file temporarily until printed.
4.  **Security:** Never store API secrets in code. Use `.env`.
5. ❌ Do not build any HTML, UI, or frontend pages (Except Dev UI). API only.
6.  **Non-Destructive Hotspot:** Hotspot is optional (`ENABLE_HOTSPOT`). If false, standard Wi-Fi applies.
7.  **Infrastructure Isolation:** Network managed by shell scripts, not Python libraries.

---

## 📅 Execution Roadmap

### 🧩 PHASE 1: Skeleton & Configuration
**Goal:** a running FastAPI service with structured config.
... [Completed] ...

### 🧩 PHASE 2: File Ingestion & Backend Registration
**Goal:** Accept a user's file and tell the backend about it.
... [Completed] ...

### 🧩 PHASE 3: The Printer Abstraction (Strategy Pattern)
**Goal:** decoupling logic from hardware.
... [Completed] ...

### 🧩 PHASE 4: The Token Handshake
**Goal:** The critical "Check-Pay-Print" loop.
... [Completed] ...

### 🧩 PHASE 5: Robustness & Logging
**Goal:** Make it demo-ready.
... [Completed] ...

---

## 📅 Hotspot Extension Roadmap

### 🧩 HOTSPOT PHASE 1: Infrastructure Scripts
**Goal:** Create shell scripts to manage hostapd and dnsmasq.
* **Scripts:** `hotspot_start.sh` (Static IP, Service Start, NAT), `hotspot_stop.sh` (Cleanup).
* **Configs:** `hostapd.conf`, `dnsmasq.conf`.

### 🧩 HOTSPOT PHASE 2: Captive Portal Routing
**Goal:** Redirect all traffic to the Kiosk.
* **Rules:** iptables redirect Port 80 -> 8000. DNS spoofing.

### 🧩 HOTSPOT PHASE 3: Python Integration
**Goal:** App controls the infrastructure.
* **Manager:** `system/network_manager.py` wrapping script calls.
* **Lifecycle:** Start/Stop hotspot on app startup/shutdown if enabled.

### 🧩 HOTSPOT PHASE 4: The Portal Experience
**Goal:** Handle OS detection checks.
* **Endpoints:** `/generate_204`, `/ncsi.txt` -> Redirect to upload.

---
