"""
Trinity AI Agent System
نظام ثلاثي الوكلاء الذكية المتخصصة
"""

__version__ = "1.0.0"
__author__ = "Nawa AI Lab"

from .main import app
from .core.base_agent import BaseAgent
from .agents.ouroboros import OuroborosArchitect
from .agents.micro_ceo import MicroCEO
from .agents.polymath import PolymathSynthesizer

__all__ = [
    "app",
    "BaseAgent",
    "OuroborosArchitect",
    "MicroCEO",
    "PolymathSynthesizer",
]
