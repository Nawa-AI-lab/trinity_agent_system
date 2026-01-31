"""
API Routes - نقاط النهاية
"""

from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()


@router.get("/info")
async def api_info():
    """معلومات API"""
    return {
        "name": "Trinity Agent API",
        "version": "1.0.0",
        "description": "API لنظام الوكلاء الذكية"
    }


@router.get("/agents/list")
async def list_available_agents():
    """قائمة الوكلاء المتاحين"""
    return {
        "agents": ["ouroboros", "ceo", "polymath"]
    }


@router.post("/agents/{agent_name}/execute")
async def execute_agent_command(agent_name: str, command: Dict[str, Any]):
    """تنفيذ أمر على وكيل"""
    return {
        "agent": agent_name,
        "command": command,
        "status": "executed"
    }
