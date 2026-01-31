"""
مدير الذاكرة - Memory Manager
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class MemoryEntry:
    """مدخل ذاكرة"""
    id: str
    type: str
    content: str
    metadata: Dict[str, Any]
    timestamp: datetime
    importance: float


class MemoryManager:
    """إدارة ذاكرة الوكيل"""
    
    def __init__(self, storage_path: str = "./workspace/memory"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.short_term: List[MemoryEntry] = []
        self.long_term: Dict[str, MemoryEntry] = {}
    
    def add_short_term(self, entry: MemoryEntry):
        """إضافة للذاكرة قصيرة المدى"""
        self.short_term.append(entry)
        if len(self.short_term) > 100:
            self._consolidate_short_term()
    
    def add_long_term(self, key: str, entry: MemoryEntry):
        """إضافة للذاكرة طويلة المدى"""
        self.long_term[key] = entry
        self._save_to_disk(key, entry)
    
    def recall(self, query: str) -> List[MemoryEntry]:
        """استرجاع الذاكرة"""
        results = []
        for entry in self.long_term.values():
            if query.lower() in entry.content.lower():
                results.append(entry)
        return results
    
    def _consolidate_short_term(self):
        """دمج الذاكرة قصيرة المدى"""
        # نقل أهم المدخلات للذاكرة طويلة المدى
        important = sorted(self.short_term, key=lambda x: x.importance, reverse=True)[:10]
        for entry in important:
            self.add_long_term(entry.id, entry)
        self.short_term = []
    
    def _save_to_disk(self, key: str, entry: MemoryEntry):
        """حفظ على القرص"""
        file_path = self.storage_path / f"{key}.json"
        file_path.write_text(json.dumps(entry.__dict__, default=str, ensure_ascii=False))
    
    def clear(self):
        """مسح الذاكرة"""
        self.short_term = []
        self.long_term = {}
