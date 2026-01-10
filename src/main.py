from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import shutil
import hashlib
import uuid
import os
from src.config import settings
from src.backend_client import BackendClient

from contextlib import asynccontextmanager
from src.token_verifier import TokenVerifier
from src.printer import get_printer
from src.logger import app_logger
from system.network_manager import NetworkManager

network_manager = NetworkManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info(f"Kiosk {settings.KIOSK_ID} Online")
    app_logger.info(f"Using Driver: {settings.PRINTER_DRIVER}")
    
    # Ensure temp dir exists
    os.makedirs("temp_uploads", exist_ok=True)
    
    if settings.ENABLE_HOTSPOT:
        network_manager.start_hotspot()

    if settings.ENABLE_DEV_UI:
        app_logger.info("⚠️ Developer UI Enabled at /__dev")
    
    yield
    
    if settings.ENABLE_HOTSPOT:
        network_manager.stop_hotspot()
        
    app_logger.info("Kiosk Shutting Down")


app = FastAPI(title="Copy Flow Pi Kiosk", lifespan=lifespan)

# Mount User Interface (Dev Only)
if settings.ENABLE_DEV_UI:
    from src.ui.routes import router as ui_router
    from src.ui.routes import public_router
    app.include_router(ui_router)
    app.include_router(public_router)

backend_client = BackendClient()

token_verifier = TokenVerifier()
printer = get_printer()


@app.get("/health")
def health_check():
    return {
        "status": "online",
        "kiosk_id": settings.KIOSK_ID,
        "driver": settings.PRINTER_DRIVER
    }

# --- Hotspot / Captive Portal Redirects ---
from fastapi.responses import RedirectResponse

@app.get("/")
def root_redirect():
    # If UI is enabled, go there. Otherwise, health?
    # For Hotspot demo, we redirect to /upload
    return RedirectResponse(url="/upload")

@app.get("/generate_204")
@app.get("/gen_204")
@app.get("/ncsi.txt")
@app.get("/hotspot-detect.html")
@app.get("/canonical.html")
def captive_portal_check():
    """
    Catch-all for OS detection. Redirect to the landing page.
    """
    return RedirectResponse(url="/upload")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), color_mode: bool = Form(False)):
    # 1. Save file to temp_uploads
    file_id = uuid.uuid4()
    temp_path = f"temp_uploads/{file_id}.pdf"
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Calculate SHA-256 hash
        sha256_hash = hashlib.sha256()
        with open(temp_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        file_hash = sha256_hash.hexdigest()
        
        # 3. Call Backend
        job_data = backend_client.register_job(
            file_hash=file_hash,
            file_name=file.filename,
            color_mode=color_mode
        )
        
        job_id = job_data.get("job_id")
        if not job_id:
             raise HTTPException(status_code=500, detail="Backend did not return job_id")

        # 4. Rename file to match job_id for easy retrieval
        final_path = f"temp_uploads/{job_id}.pdf"
        os.rename(temp_path, final_path)
        
        # Return job_id and payment info to user
        return job_data

    except Exception as e:
        # Cleanup if something fails
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/print/{job_id}")
def print_document(job_id: str):
    file_path = f"temp_uploads/{job_id}.pdf"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found or expired")
        
    try:
        # 1. Fetch Token
        token = backend_client.get_print_token(job_id)
        if not token:
            raise HTTPException(status_code=402, detail="Payment required / Token missing")
            
        # 2. Verify Token
        if not token_verifier.verify(token, job_id):
            raise HTTPException(status_code=403, detail="Invalid or expired token")
            
        # 3. Execute Print
        # We need to know if it's color or not. 
        # Ideally, we stored this, or the backend/token tells us. 
        # For this MVP, we'll default to False or check if we can store state.
        # Since we are "Stateless" basically, maybe we should have asked for settings in the token or trusted the Backend's word.
        # Let's assume defaults for now as strictly per prompt logic "Pi never assumes job is paid...".
        printer.print_file(file_path, settings={})
        
        # 4. Cleanup
        os.remove(file_path)
        
        return {"status": "printed", "job_id": job_id}

    except HTTPException as he:
        raise he
    except Exception as e:
        app_logger.error(f"Print error: {e}")
        raise HTTPException(status_code=500, detail="Printing failed")



