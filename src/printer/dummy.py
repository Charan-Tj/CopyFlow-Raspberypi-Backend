import time
from .base import BasePrinter
from typing import Dict, Any

class DummyPrinter(BasePrinter):
    def print_file(self, file_path: str, settings: Dict[str, Any] = {}) -> bool:
        print(f"[DUMMY] Printing {file_path}...")
        print(f"    Settings: {settings}")
        time.sleep(3) # Simulate printing time
        print(f"[OK] [DUMMY] {file_path} printed successfully.")
        return True
