import requests
from src.config import settings

from src.logger import app_logger

class BackendClient:
    def __init__(self):
        self.base_url = str(settings.BACKEND_URL).rstrip("/")
        self.kiosk_id = settings.KIOSK_ID

    def register_job(self, file_hash: str, file_name: str, color_mode: bool = False, **kwargs):
        """
        Registers a print job with the backend.
        """
        url = f"{self.base_url}/kiosks/{self.kiosk_id}/jobs"
        payload = {
            "file_hash": file_hash,
            "filename": file_name,
            "color": color_mode,
            "num_pages": kwargs.get("num_pages", 0),
            "estimated_cost": kwargs.get("estimated_cost", 0)
        }
        
        # Note: In a real implementation, we might want to calculate page count here or have the backend do it.
        # For this phase, we simply send the metadata we have.
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Log this error in production
            app_logger.error(f"Error connecting to backend: {e}")
            raise e

    def get_print_token(self, job_id: str):
        """
        Fetches the print token for a specific job.
        """
        url = f"{self.base_url}/kiosks/{self.kiosk_id}/jobs/{job_id}/token"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("token")
        except requests.RequestException as e:
            app_logger.error(f"Error fetching token: {e}")
            raise e


