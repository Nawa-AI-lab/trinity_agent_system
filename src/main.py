"""
نظام الثالوث للوكلاء الذكية - نقطة الدخول الرئيسية
FastAPI Server مع واجهات برمجة كاملة
"""

import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# إضافة مسار المشروع
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import settings
from src.core.base_agent import AgentStatus
from src.agents.ouroboros import OuroborosArchitect
from src.agents.micro_ceo import MicroCEO
from src.agents.polymath import PolymathSynthesizer
from src.utils.logger import setup_logging

# إعداد التسجيل
logger = setup_logging()


# نماذج الطلبات والاستجابات
class AgentRequest(BaseModel):
    """طلب الوكيل"""
    task: str = Field(..., description="المهمة المطلوبة")
    context: Dict[str, Any] = Field(default_factory=dict, description="سياق إضافي")
    stream: bool = Field(default=False, description="تدفق الاستجابة")


class SystemStatus(BaseModel):
    """حالة النظام"""
    status: str
    timestamp: str
    agents: Dict[str, Any]
    system_info: Dict[str, Any]


# إدارة الوكلاء
agents = {}


def initialize_agents():
    """تهيئة جميع الوكلاء"""
    global agents
    
    logger.info("بدء تهيئة الوكلاء...")
    
    try:
        agents["ouroboros"] = OuroborosArchitect(
            workspace_path=str(Path(__file__).parent.parent / "workspace")
        )
        logger.info("تم تهيئة المهندس المعماري العودي")
    except Exception as e:
        logger.error(f"فشل في تهيئة Ouroboros: {e}")
    
    try:
        agents["ceo"] = MicroCEO(
            initial_budget=1000.0,
            currency="USD"
        )
        logger.info("تم تهيئة الرئيس التنفيذي المجهري")
    except Exception as e:
        logger.error(f"فشل في تهيئة MicroCEO: {e}")
    
    try:
        agents["polymath"] = PolymathSynthesizer()
        logger.info("تم تهيئة المركّب المعرفي الشامل")
    except Exception as e:
        logger.error(f"فشل في تهيئة Polymath: {e}")
    
    logger.info(f"تم تهيئة {len(agents)} وكيل(s)")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """إدارة دورة حياة التطبيق"""
    # بدء التشغيل
    logger.info("بدء تشغيل نظام الثالوث...")
    initialize_agents()
    logger.info("النظام جاهز!")
    
    yield
    
    # إيقاف التشغيل
    logger.info("إيقاف النظام...")


# إنشاء تطبيق FastAPI
app = FastAPI(
    title="Trinity AI Agent System",
    description="نظام ثلاثي الوكلاء الذكية: المعماري، التنفيذي، والباحث",
    version="1.0.0",
    lifespan=lifespan
)

# إضافة CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# نقاط النهاية

@app.get("/", response_model=Dict)
async def root():
    """الصفحة الرئيسية"""
    return {
        "name": "Trinity AI Agent System",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "agents": "/agents",
            "status": "/system/status"
        }
    }


@app.get("/health")
async def health_check():
    """فحص صحة النظام"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agents_active": list(agents.keys())
    }


@app.get("/system/status", response_model=SystemStatus)
async def system_status():
    """الحصول على حالة النظام"""
    agents_status = {}
    
    for name, agent in agents.items():
        agents_status[name] = agent.get_status()
    
    return SystemStatus(
        status="operational",
        timestamp=datetime.utcnow().isoformat(),
        agents=agents_status,
        system_info={
            "python_version": sys.version,
            "agents_count": len(agents)
        }
    )


@app.get("/agents")
async def list_agents():
    """قائمة الوكلاء المتاحين"""
    return {
        "agents": [
            {
                "name": "ouroboros",
                "role": "المهندس المعماري العودي",
                "description": "متخصص في هندسة البرمجيات وتحسينها",
                "capabilities": ["تحليل الكود", "إنشاء الكود", "إعادة الهيكلة", "الأمن"]
            },
            {
                "name": "ceo",
                "role": "الرئيس التنفيذي المجهري",
                "description": "متخصص في إدارة الأعمال واتخاذ القرارات",
                "capabilities": ["تحليل السوق", "تخطيط الأعمال", "إدارة الميزانية", "التقارير"]
            },
            {
                "name": "polymath",
                "role": "المركّب المعرفي الشامل",
                "description": "متخصص في البحث وربط المعلومات",
                "capabilities": ["البحث الشامل", "استخراج البيانات", "ربط المفاهيم", "تحليل الأوراق"]
            }
        ]
    }


@app.post("/agent/{agent_name}/run")
async def run_agent(agent_name: str, request: AgentRequest):
    """تشغيل وكيل محدد"""
    if agent_name not in agents:
        raise HTTPException(
            status_code=404,
            detail=f"الوكيل '{agent_name}' غير موجود. الوكلاء المتاحون: {list(agents.keys())}"
        )
    
    try:
        agent = agents[agent_name]
        result = await agent.run(request.task, request.context)
        
        return {
            "agent": agent_name,
            "result": result.model_dump()
        }
        
    except Exception as e:
        logger.error(f"خطأ في تشغيل الوكيل {agent_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/agent/{agent_name}/history")
async def get_agent_history(agent_name: str, limit: int = 10):
    """الحصول على تاريخ الوكيل"""
    if agent_name not in agents:
        raise HTTPException(status_code=404, detail="الوكيل غير موجود")
    
    agent = agents[agent_name]
    history = agent.thought_history[-limit:]
    
    return {
        "agent": agent_name,
        "history_count": len(history),
        "history": [h.model_dump() for h in history]
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
