"""Centralized logging system for TranslatorApp."""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def setup_logger(data_dir: str = "data") -> logging.Logger:
    """Configure and return the root logger with daily file rotation and date prefix."""
    log_dir = Path(data_dir) / "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    date_prefix = datetime.now().strftime("%Y%m%d")
    
    # Create root logger
    logger = logging.getLogger("TranslatorApp")
    logger.setLevel(logging.DEBUG)
    
    # Avoid duplicate handlers if already setup
    if logger.handlers:
        return logger

    # Shared Formatter
    app_fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

    # 1. Main App Log (yyyyMMdd_app.log)
    app_log = log_dir / f"{date_prefix}_app.log"
    app_handler = TimedRotatingFileHandler(
        app_log, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    app_handler.setLevel(logging.DEBUG)
    app_handler.setFormatter(app_fmt)
    
    # 2. Error Log (yyyyMMdd_error.log)
    error_log = log_dir / f"{date_prefix}_error.log"
    error_handler = TimedRotatingFileHandler(
        error_log, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(app_fmt)
    
    # 3. API Log (yyyyMMdd_api.log) - For Requests and Responses
    api_log = log_dir / f"{date_prefix}_api.log"
    api_handler = TimedRotatingFileHandler(
        api_log, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    api_handler.setLevel(logging.INFO)
    api_handler.setFormatter(app_fmt)
    
    # Assign handlers to specific loggers
    logger.addHandler(app_handler)
    logger.addHandler(error_handler)
    
    # Configure special API logger
    api_logger = logging.getLogger("TranslatorApp.api")
    api_logger.propagate = False # Don't send API logs to app.log
    api_logger.addHandler(api_handler)
    
    # 4. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_fmt)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """Get a named logger that is a child of the root logger."""
    root_name = "TranslatorApp"
    if name:
        return logging.getLogger(f"{root_name}.{name}")
    return logging.getLogger(root_name)
