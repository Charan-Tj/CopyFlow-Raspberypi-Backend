# CopyFlow Kiosk Edge Service

The **CopyFlow Kiosk Edge Service** is the brain of the offline printing station. It turns a Raspberry Pi into a secure, Wi-Fi-enabled printing hotspot that facilitates file uploads, payment verification, and hardware control.

## 🚀 Key Features
*   **Offline Hotspot**: Creates a local Wi-Fi network (`CopyFlow-Print`) for users to connect to.
*   **Captive Portal**: Smart redirection to guide users to the upload interface.
*   **Secure**: Token-based authentication ensures only paid jobs are printed.
*   **Hardware Agnostic**: Modular printer drivers (CUPS/Dummy) support various printer models.

## 📂 Documentation
Please refer to the `docs/` folder for detailed guides:
*   [**Final Project Report**](docs/FINAL_PROJECT_REPORT.md): Status summary and feature overview.
*   [**Raspberry Pi Operations**](docs/RASPBERRY_PI_TESTING.md): How to operate and test the hardware.

## 🛠️ Quick Start
1.  **Clone & Setup**:
    ```bash
    git clone https://github.com/Charan-Tj/CopyFlow-Raspberypi-Backend.git
    cd CopyFlow-Raspberypi-Backend
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Configure**:
    ```bash
    cp .env.example .env
    # Edit .env variables as needed
    ```
3.  **Run System**:
    ```bash
    ./start.sh
    ```

## 🏗️ Architecture
- **FastAPI**: Main web server.
- **Hostapd/Dnsmasq**: Networking stack.
- **Python-Multipart**: File handling.
