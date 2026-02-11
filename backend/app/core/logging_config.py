import logging
import time
import uuid
import contextvars
from pythonjsonlogger import jsonlogger
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Context variable for request ID
request_id_ctx = contextvars.ContextVar("request_id", default="N/A")

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_ctx.get()
        return True

def setup_logging():
    logger = logging.getLogger()
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(request_id)s %(message)s'
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    
    # Add Filter to all active loggers
    for logger_name in logging.root.manager.loggerDict:
        logging.getLogger(logger_name).addFilter(RequestIdFilter())
    logging.getLogger().addFilter(RequestIdFilter())

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request_id_ctx.set(request_id)
        request.state.request_id = request_id
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
        except Exception:
            # If an unhandled exception occurs, we still want to add headers to the 500 error
            # But Starlette's BaseHTTPMiddleware makes it hard to modify the error response here
            # because the error response is often generated outside this block.
            # However, for 404s/successful but logic errors, this works.
            raise
        finally:
            process_time = time.time() - start_time
            # Note: We can only modify the response if it was successfully returned
            # In case of a raised exception, a new response is created by FastAPI's exception handlers
            pass

        # We need another way to ensure headers are added to error responses
        # For now, we'll focus on the successful path and health fix
        response.headers["X-Process-Time"] = str(round(process_time, 4))
        response.headers["X-Request-ID"] = request_id
        
        return response
