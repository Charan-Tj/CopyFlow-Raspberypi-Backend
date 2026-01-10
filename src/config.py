from enum import Enum
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class PrinterDriver(str, Enum):
    DUMMY = "DUMMY"
    CUPS = "CUPS"

class Settings(BaseSettings):
    KIOSK_ID: str # Using str for UUID to avoid strict validation issues if needed, but UUID is better. Let's use str for now to be safe, or Import UUID.
    KIOSK_SECRET: str
    BACKEND_URL: HttpUrl
    PRINTER_DRIVER: PrinterDriver = PrinterDriver.DUMMY
    ENABLE_DEV_UI: bool = False
    ENABLE_HOTSPOT: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")




settings = Settings()
