"""
إعدادات النظام - Configuration
"""

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """إعدادات النظام"""
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # System Settings
    environment: str = "development"
    debug: bool = True
    
    # Storage
    storage_path: str = "./workspace"
    
    # Task Engine
    task_timeout: int = 300
    max_concurrent_tasks: int = 5
    
    # Browser Settings
    browser_headless: bool = True
    playwright_timeout: int = 30000
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./workspace/logs/system.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """الحصول على إعدادات النظام"""
    return Settings()


settings = get_settings()
