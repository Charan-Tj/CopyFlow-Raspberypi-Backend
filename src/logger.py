import logging
import sys
from collections import deque

# Buffer for last 50 logs
log_buffer = deque(maxlen=50)

class buffer_handler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            log_buffer.append(msg)
        except Exception:
            self.handleError(record)

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if handler exists to avoid duplicates
    if not logger.handlers:
        # Stream Handler
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Memory Handler for UI
        mem_handler = buffer_handler()
        mem_handler.setFormatter(formatter)
        logger.addHandler(mem_handler)
        
    return logger

app_logger = setup_logger("PiKiosk")

def get_recent_logs():
    return list(log_buffer)

