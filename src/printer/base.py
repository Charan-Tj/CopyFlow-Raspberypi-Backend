from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePrinter(ABC):
    @abstractmethod
    def print_file(self, file_path: str, settings: Dict[str, Any] = {}) -> bool:
        """
        Print a file with the given settings.
        Returns True if successful, raises Exception otherwise.
        """
        pass
