from src.config import settings, PrinterDriver
from .base import BasePrinter
from .dummy import DummyPrinter
from .cups import CupsPrinter
from functools import lru_cache

@lru_cache()
def get_printer() -> BasePrinter:
    driver = settings.PRINTER_DRIVER
    
    if driver == PrinterDriver.DUMMY:
        return DummyPrinter()
    elif driver == PrinterDriver.CUPS:
        return CupsPrinter()
    else:
        # Fallback to Dummy if unknown, though Enum should catch this
        return DummyPrinter()
