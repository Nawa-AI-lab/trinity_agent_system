"""
دوال مساعدة - Helper Functions
"""

import json
from typing import Any, Dict, Optional


def format_response(data: Any, status: str = "success", message: str = "") -> Dict[str, Any]:
    """تنسيق استجابة موحدة"""
    return {
        "status": status,
        "message": message,
        "data": data,
        "timestamp": str(datetime.utcnow().isoformat())
    }


def parse_json_safe(text: str, default: Any = None) -> Any:
    """تحليل JSON بأمان"""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return default


def validate_api_key(key: str) -> bool:
    """التحقق من صحة مفتاح API"""
    if not key:
        return False
    if len(key) < 10:
        return False
    if key.startswith("sk-"):
        return True
    return False
