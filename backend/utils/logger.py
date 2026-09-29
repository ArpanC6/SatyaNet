"""Structured logger."""
import sys
from loguru import logger
from backend.config import settings


def _configure_logger():
    logger.remove()

    logger.add(
        sys.stdout,
        level=settings.log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    try:
        logger.add(
            "logs/satyanet_{time:YYYY-MM-DD}.log",
            level=settings.log_level,
            rotation="10 MB",
            retention="14 days",
            compression="zip",
            serialize=True,
            enqueue=True,
            backtrace=True,
            diagnose=not settings.is_production,
        )
    except Exception:
        pass


_configure_logger()

__all__ = ["logger"]
