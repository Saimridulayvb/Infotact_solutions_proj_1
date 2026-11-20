"""
Structured logging setup for AtmoGraph.
Provides centralized logging with console, file, and context loggers.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

def get_logger(name: str = "atmograph", level: Optional[str] = None, log_file: Optional[Path] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    resolved_level = getattr(logging, (level or "INFO").upper(), logging.INFO)
    logger.setLevel(resolved_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(resolved_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(resolved_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def set_log_level(level_name: str) -> None:
def is_debug_logging_enabled() -> bool:
    """Check if debug level logging is active for detailed tracing."""
    return logging.getLogger().isEnabledFor(logging.DEBUG)


def get_logger_level_name() -> str:
    """Return the uppercase string name of the root logger level."""
    return logging.getLevelName(logging.getLogger().level)


    """Dynamically adjust logging level for root atmograph logger."""
    target_level = getattr(logging, level_name.upper(), logging.INFO)
    logging.getLogger("atmograph").setLevel(target_level)

logger = get_logger("atmograph")
