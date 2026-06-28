import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import admin, auth, builder, dashboard, jobs, resumes
from app.core.config import settings
from app.db.seed import seed_jobs

logger = logging.getLogger("resumeai")


def create_app() -> FastAPI:
    app = FastAPI(title="ResumeAI API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=False if settings.cors_origins_list == ["*"] else True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(resumes.router)
    app.include_router(jobs.router)
    app.include_router(builder.router)
    app.include_router(dashboard.router)
    app.include_router(admin.router)

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: HTTPException):
        return JSONResponse(status_code=404, content={"detail": exc.detail or "Resource not found"})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=422, content={"detail": "Validation error", "errors": exc.errors()})

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )

    @app.on_event("startup")
    def on_startup():
        seed_jobs()

    @app.get("/")
    def root():
        return {"message": "ResumeAI API is running", "docs": "/docs"}

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
