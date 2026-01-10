import subprocess
import os
from src.logger import app_logger

class NetworkManager:
    def __init__(self):
        self.script_dir = os.path.join(os.getcwd(), "scripts")
    
    def start_hotspot(self):
        app_logger.info("🔥 [Network] Enabling Hotspot Mode...")
        script_path = os.path.join(self.script_dir, "hotspot_start.sh")
        
        try:
            # Note: In a real deployment, the user running this (e.g., pi) needs sudoers NOPASSWD for these scripts.
            # We assume sudo is available and interactive-less.
            result = subprocess.run(["sudo", script_path], check=True, capture_output=True, text=True)
            app_logger.info(f"✅ [Network] Hotspot Started: {result.stdout}")
        except subprocess.CalledProcessError as e:
            app_logger.error(f"❌ [Network] Failed to start Hotspot: {e.stderr}")
        except Exception as e:
            app_logger.error(f"❌ [Network] Unexpected error starting hotspot: {e}")

    def stop_hotspot(self):
        app_logger.info("❄️  [Network] Disabling Hotspot Mode...")
        script_path = os.path.join(self.script_dir, "hotspot_stop.sh")
        
        try:
            result = subprocess.run(["sudo", script_path], check=True, capture_output=True, text=True)
            app_logger.info(f"✅ [Network] Hotspot Stopped: {result.stdout}")
        except subprocess.CalledProcessError as e:
            app_logger.error(f"❌ [Network] Failed to stop Hotspot: {e.stderr}")
        except Exception as e:
            app_logger.error(f"❌ [Network] Unexpected error stopping hotspot: {e}")
