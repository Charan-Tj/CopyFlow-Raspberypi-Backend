from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from src.config import settings
from src.logger import get_recent_logs, app_logger
from src.backend_client import BackendClient

# Dev Router (Prefixed with /__dev)
dev_router = APIRouter(prefix="/__dev")

# Public Router (No prefix, for user facing pages)
public_router = APIRouter()

templates = Jinja2Templates(directory="src/ui/templates")
backend_client = BackendClient()

# --- Public User Routes ---

@public_router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """
    Renders the main upload page for the user.
    """
    return templates.TemplateResponse("upload.html", {"request": request})

@public_router.get("/status", response_class=HTMLResponse)
async def status_page(request: Request, job_id: str):
    """
    Renders the status page which polls for payment/print status.
    """
    return templates.TemplateResponse("status.html", {
        "request": request, 
        "job_id": job_id
    })

@public_router.get("/error", response_class=HTMLResponse)
async def error_page(request: Request, detail: str = "Unknown Error"):
    return templates.TemplateResponse("error.html", {
        "request": request,
        "error_detail": detail
    })

@public_router.get("/check_job/{job_id}")
async def check_job_status(job_id: str):
    """
    Used by the Status Polling UI.
    Returns: { "status": "WAITING" | "READY" | "PRINTED" }
    """
    # 1. Check if we already printed it? (Ideally we have state but we are stateless-ish)
    # For now, let's assume if it's not printed, we check the token.
    
    try:
        # Check if backend has a token for this job
        token = backend_client.get_print_token(job_id)
        if token:
            return {"status": "READY"} 
            # READY means we have the token, so we CAN print. 
            # The UI will then trigger /print/{job_id} which verifies the token and prints.
        
        return {"status": "WAITING"}
    except Exception:
        # 402/404 from backend means waiting or invalid
        return {"status": "WAITING"}


# --- Dev Routes ---

@dev_router.get("/", response_class=HTMLResponse)
async def dev_dashboard(request: Request):
    """
    Original Dev Dashboard.
    """
    # Try to verify if index.html exists, else fallback or error?
    # We should keep index.html for dev if we want, but the user didn't ask us to delete it.
    # We'll assume index.html is still there or we can render a simple string if we deleted it.
    # But wait, I didn't delete index.html.
    return templates.TemplateResponse("index.html", {
        "request": request,
        "kiosk_id": settings.KIOSK_ID,
        "backend_url": settings.BACKEND_URL,
        "printer_driver": settings.PRINTER_DRIVER,
        "logs": get_recent_logs()
    })

@dev_router.get("/token_status/{job_id}")
async def dev_token_check(job_id: str):
    return await check_job_status(job_id)
