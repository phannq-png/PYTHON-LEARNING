"""Centralized logging system for TranslatorApp."""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(data_dir: str = "data") -> logging.Logger:
    """Configure and return the root logger with file and console handlers."""
    log_dir = Path(data_dir) / "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = log_dir / "error.log"
    
    # Create root logger
    logger = logging.getLogger("TranslatorApp")
    logger.setLevel(logging.DEBUG)
    
    # Avoid duplicate handlers if already setup
    if logger.handlers:
        return logger

    # 1. Rotating File Handler (Max 10MB, 5 backups)
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024, 
        backupCount=5, 
        encoding="utf-8"
    )
    file_handler.setLevel(logging.ERROR) # Only log errors and above to file
    file_fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(file_fmt)
    
    # 2. Console Handler (For development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_fmt)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """Get a named logger that is a child of the root logger."""
    root_name = "TranslatorApp"
    if name:
        return logging.getLogger(f"{root_name}.{name}")
    return logging.getLogger(root_name)
