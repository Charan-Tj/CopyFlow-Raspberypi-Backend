from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.config import settings
from src.logger import get_recent_logs, app_logger
from src.backend_client import BackendClient

router = APIRouter(prefix="/__dev")
public_router = APIRouter() # No prefix for public aliases
templates = Jinja2Templates(directory="src/ui/templates")
backend_client = BackendClient()

@router.get("/", response_class=HTMLResponse)
async def dev_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "kiosk_id": settings.KIOSK_ID,
        "backend_url": settings.BACKEND_URL,
        "printer_driver": settings.PRINTER_DRIVER,
        "logs": get_recent_logs()
    })

@public_router.get("/upload", response_class=HTMLResponse)
async def public_upload_page(request: Request):
    """
    Public alias for the upload page (served via /__dev/ template)
    Used for Captive Portal landing.
    """
    return templates.TemplateResponse("index.html", {
        "request": request,
        "kiosk_id": settings.KIOSK_ID,
        "backend_url": settings.BACKEND_URL,
        "printer_driver": settings.PRINTER_DRIVER,
        "logs": get_recent_logs()
    })


@router.get("/token_status/{job_id}")
async def check_token_status(job_id: str):
    """
    Helper for the UI to safely check if a token exists without consuming it 
    or needing to perform signature verification itself (the UI is untrusted client).
    Actually, we just want to know if the backend HAS a token.
    """
    # Note: backend_client.get_print_token will return the token string or raise error.
    try:
        token = backend_client.get_print_token(job_id)
        if token:
            return {"status": "READY"}
        return {"status": "WAITING"}
    except Exception:
        # If we get 402 or 404 from backend (propagated), it means waiting
        return {"status": "WAITING"}
