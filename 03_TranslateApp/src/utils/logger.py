"""Centralized logging system for TranslatorApp."""

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def setup_logger(data_dir: str = "data") -> logging.Logger:
    """Configure and return the root logger with daily file rotation."""
    log_dir = Path(data_dir) / "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = log_dir / "app.log" # Rename to app.log as it might contain more than errors now
    
    # Create root logger
    logger = logging.getLogger("TranslatorApp")
    logger.setLevel(logging.DEBUG)
    
    # Avoid duplicate handlers if already setup
    if logger.handlers:
        return logger

    # 1. Main App Log (Every midnight, keep 7 days, all levels)
    app_log = log_dir / "app.log"
    app_handler = TimedRotatingFileHandler(
        app_log, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    app_handler.setLevel(logging.DEBUG)
    app_fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
    app_handler.setFormatter(app_fmt)
    
    # 2. Error Log (Every midnight, keep 7 days, only ERROR+)
    error_log = log_dir / "error.log"
    error_handler = TimedRotatingFileHandler(
        error_log, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(app_fmt)
    
    # 3. Console Handler (For development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_fmt)
    
    logger.addHandler(app_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """Get a named logger that is a child of the root logger."""
    root_name = "TranslatorApp"
    if name:
        return logging.getLogger(f"{root_name}.{name}")
    return logging.getLogger(root_name)
