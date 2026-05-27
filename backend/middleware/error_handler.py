from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.utils.exceptions import DocumentQAException


def setup_error_handlers(app: FastAPI):
    @app.exception_handler(DocumentQAException)
    async def document_qa_exception_handler(request: Request, exc: DocumentQAException):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc), "error_code": exc.__class__.__name__},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "error_code": "INTERNAL_ERROR"},
        )
