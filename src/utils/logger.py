"""
نظام التسجيل - Logging System
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger:
    """إعداد نظام التسجيل"""
    
    # إنشاء مجلد السجلات
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # تكوين الشكل
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # الحصول على المسجل الرئيسي
    logger = logging.getLogger('trinity')
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # معالج Console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # معالج الملف
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """الحصول على مسجل"""
    return logging.getLogger(f'trinity.{name}')
