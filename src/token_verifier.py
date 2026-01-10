import hmac
import hashlib
import time
from src.config import settings

class TokenVerifier:
    def __init__(self):
        self.secret = settings.KIOSK_SECRET.encode('utf-8')

    def verify(self, token: str, job_id: str) -> bool:
        """
        Verifies the print token.
        Expected format: "job_id|expiry_timestamp|signature"
        """
        try:
            parts = token.split('|')
            if len(parts) != 3:
                print("Token format invalid")
                return False
            
            token_job_id, expiry, signature = parts
            
            # 1. Verify Job ID matches
            if token_job_id != job_id:
                print("Token job_id mismatch")
                return False
            
            # 2. Check Expiry
            if int(expiry) < time.time():
                print("Token expired")
                return False
            
            # 3. Verify Signature
            payload = f"{token_job_id}|{expiry}".encode('utf-8')
            expected_signature = hmac.new(self.secret, payload, hashlib.sha256).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                print("Signature mismatch")
                return False
                
            return True
            
        except ValueError:
            return False
