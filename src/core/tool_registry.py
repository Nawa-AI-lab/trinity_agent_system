"""
سجل الأدوات - Tool Registry
"""

from typing import Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum


class ToolCategory(str, Enum):
    """فئات الأدوات"""
    BROWSER = "browser"
    CODE = "code"
    FILE = "file"
    SEARCH = "search"
    API = "api"
    DATA = "data"
    UTILITY = "utility"


@dataclass
class Tool:
    """أداة"""
    name: str
    category: ToolCategory
    function: Callable
    description: str
    parameters: Dict[str, Any]
    examples: List[str] = None


class ToolRegistry:
    """سجل الأدوات"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.categories: Dict[ToolCategory, List[str]] = {cat: [] for cat in ToolCategory}
    
    def register(self, tool: Tool):
        """تسجيل أداة"""
        self.tools[tool.name] = tool
        self.categories[tool.category].append(tool.name)
    
    def get(self, name: str) -> Tool:
        """الحصول على أداة"""
        return self.tools.get(name)
    
    def list_by_category(self, category: ToolCategory) -> List[str]:
        """قائمة الأدوات حسب الفئة"""
        return self.categories.get(category, [])
    
    def list_all(self) -> List[Tool]:
        """قائمة جميع الأدوات"""
        return list(self.tools.values())
