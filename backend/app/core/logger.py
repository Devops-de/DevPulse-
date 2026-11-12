import logging
import sys

from app.core.config import settings


def setup_logger(name: str = "devpulse") -> logging.Logger:
    """Configures and returns a structured application logger."""
    app_logger = logging.getLogger(name)

    if not app_logger.handlers:
        level = logging.DEBUG if settings.DEBUG else logging.INFO
        app_logger.setLevel(level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        app_logger.addHandler(handler)

    return app_logger


logger = setup_logger()
