"""Small, centralized logging setup."""

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure consistent logs for scripts and web processes."""
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
