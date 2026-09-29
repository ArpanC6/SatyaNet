"""
SatyaNet - FastAPI Application Entry Point
Trust-Aware Field Intelligence for Disaster Response.
"""
from __future__ import annotations

import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend import __version__
from backend.config import settings
from backend.routes import projects_router, search_router, verify_router
from backend.utils.exceptions import SatyaNetError
from backend.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    log = logger.bind(component="lifespan")
    log.info(f"SatyaNet v{__version__} starting")
    log.info(f"Environment: {settings.app_env}")
    log.info(f"Cloudinary configured: {bool(settings.cloudinary_cloud_name)}")
    log.info(f"Qdrant URL: {settings.qdrant_url}")
    yield
    log.info("SatyaNet shutting down")


app = FastAPI(
    title="SatyaNet API",
    description=(
        "Trust-Aware Field Intelligence for Disaster Response. "
        "Bayesian verification of field media using Cloudinary, "
        "satellite cross-check, and EXIF forensics."
    ),
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time-ms"] = f"{elapsed_ms:.2f}"
    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code} "
        f"({elapsed_ms:.1f} ms) [{request_id}]"
    )
    return response


@app.exception_handler(SatyaNetError)
async def satyanet_exception_handler(request: Request, exc: SatyaNetError):
    logger.error(f"SatyaNetError: {exc.error_code} - {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "details": {},
        },
    )


app.include_router(verify_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")


@app.get("/", tags=["meta"])
async def root():
    return {
        "name": "SatyaNet",
        "version": __version__,
        "description": "Trust-Aware Field Intelligence for Disaster Response",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["meta"])
async def health():
    return {
        "status": "ok",
        "version": __version__,
        "environment": settings.app_env,
    }