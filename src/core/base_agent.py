"""
الفئة الأساسية للوكلاء الذكية - العمود الفقري للنظام
"""

import json
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class AgentStatus(str, Enum):
    """حالات الوكيل"""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    LEARNING = "learning"
    ERROR = "error"


class TaskPriority(str, Enum):
    """أولويات المهام"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ThoughtStep(BaseModel):
    """خطوة تفكير"""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    step_type: str
    content: str
    confidence: float = Field(ge=0, le=1)
    tools_used: List[str] = Field(default_factory=list)


class ActionResult(BaseModel):
    """نتيجة تنفيذ إجراء"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: int
    artifacts: List[str] = Field(default_factory=list)


class TaskContext(BaseModel):
    """سياق المهمة"""
    task_id: str
    original_request: str
    priority: TaskPriority = TaskPriority.MEDIUM
    metadata: Dict[str, Any] = Field(default_factory=dict)
    max_iterations: int = 10
    timeout_seconds: int = 300


class AgentThought(BaseModel):
    """تفكير الوكيل"""
    agent_name: str
    task_id: str
    status: AgentStatus
    thought_steps: List[ThoughtStep] = Field(default_factory=list)
    current_action: Optional[str] = None
    final_result: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


class BaseAgent(ABC):
    """
    الفئة الأساسية لجميع الوكلاء الذكية
    
    توفر:
    - إدارة الحالة والتاريخ
    - تكامل مع نماذج اللغة الكبيرة
    - نظام الأدوات القابل للتسجيل
    - معالجة المهام غير المتزامنة
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        description: str,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ):
        self.name = name
        self.role = role
        self.description = description
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # إعداد نظام الرسائل
        self.system_prompt = system_prompt or self._default_system_prompt()
        
        # أدوات الوكيل
        self._tools: Dict[str, callable] = {}
        self._tool_descriptions: List[Dict] = []
        
        # إدارة الحالة
        self.status = AgentStatus.IDLE
        self.current_task: Optional[TaskContext] = None
        self.thought_history: List[AgentThought] = []
        
        # تهيئة العميل
        self._init_llm_client()
        
        # إعدادات متقدمة
        self.max_iterations = 10
        self.continue_on_error = True
        
        logger.info(f"تم تهيئة الوكيل: {self.name}")
    
    def _default_system_prompt(self) -> str:
        """النظام الافتراضي للوكيل"""
        return f"""أنت {self.name}، {self.role}.
        
{description}

مهمتك هي تحليل المهام واتخاذ الإجراءات المناسبة باستخدام الأدوات المتاحة.
يجب أن تكون منهجياً ودقيقاً في تفكيرك، مع شرح خطواتك بوضوح.
تذكر دائماً أن تختار الأداة المناسبة للمهمة، ولا تتردد في طلب توضيح إذا كان الطلب غامضاً."""

    def _init_llm_client(self):
        """تهيئة عميل نموذج اللغة"""
        api_key = self._get_api_key()
        if api_key:
            self.client = AsyncOpenAI(api_key=api_key)
            self.using_llm = True
        else:
            self.using_llm = False
            logger.warning(f"لم يتم العثور على مفتاح API للوكيل {self.name}")
    
    def _get_api_key(self) -> Optional[str]:
        """الحصول على مفتاح API"""
        import os
        env_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
        for key in env_keys:
            if os.getenv(key):
                return os.getenv(key)
        return None
    
    def register_tool(self, name: str, func: callable, description: str, parameters: Dict):
        """تسجيل أداة جديدة للوكيل"""
        self._tools[name] = func
        self._tool_descriptions.append({
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        })
        logger.info(f"تم تسجيل الأداة '{name}' للوكيل {self.name}")
    
    def get_tool(self, name: str) -> Optional[callable]:
        """الحصول على أداة بالاسم"""
        return self._tools.get(name)
    
    async def think(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """مرحلة التفكير - تحليل المهمة واتخاذ القرار"""
        self.status = AgentStatus.THINKING
        
        prompt = f"""
المهمة: {task}

السياق: {json.dumps(context, ensure_ascii=False, indent=2) if context else 'لا يوجد سياق إضافي'}

الأدوات المتاحة:
{json.dumps([t['function'] for t in self._tool_descriptions], ensure_ascii=False, indent=2)}

بناءً على المهمة والسياق، ما الإجراء المناسب؟ 
فكر خطوة بخطوة، ثم حدد أي أداة يجب استخدامها.
"""
        
        if self.using_llm:
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                thought = response.choices[0].message.content
                return thought
            except Exception as e:
                logger.error(f"خطأ في التفكير: {e}")
                return f"فشل في التواصل مع نموذج اللغة: {e}"
        else:
            return "لا يوجد نموذج لغة متاح. يرجى توفير مفتاح API."
    
    async def act(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> ActionResult:
        """مرحلة التنفيذ - تنفيذ الإجراء المحدد"""
        self.status = AgentStatus.ACTING
        start_time = datetime.utcnow()
        
        tool = self._tools.get(action)
        if not tool:
            return ActionResult(
                success=False,
                error=f"الأداة '{action}' غير موجودة",
                execution_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000)
            )
        
        try:
            if asyncio.iscoroutinefunction(tool):
                result = await tool(**params)
            else:
                result = tool(**params)
            
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            return ActionResult(
                success=True,
                data=result if isinstance(result, dict) else {"result": str(result)},
                execution_time_ms=execution_time
            )
        except Exception as e:
            logger.error(f"خطأ في تنفيذ الإجراء '{action}': {e}")
            return ActionResult(
                success=False,
                error=str(e),
                execution_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000)
            )
    
    async def run(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        max_iterations: Optional[int] = None
    ) -> AgentThought:
        """تشغيل الدورة الكاملة للوكيل"""
        max_iterations = max_iterations or self.max_iterations
        thought = AgentThought(
            agent_name=self.name,
            task_id=f"{self.name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            status=AgentStatus.IDLE
        )
        
        self.status = AgentStatus.IDLE
        
        # تخزين المهمة الحالية
        self.current_task = TaskContext(
            task_id=thought.task_id,
            original_request=task,
            metadata=context or {}
        )
        
        try:
            for iteration in range(max_iterations):
                logger.info(f"التكرار {iteration + 1}/{max_iterations}")
                
                # 1. التفكير
                thought_process = await self.think(task, context)
                thought.thought_steps.append(ThoughtStep(
                    step_type="thinking",
                    content=thought_process,
                    confidence=0.8
                ))
                
                # 2. استخراج الإجراء من التفكير
                action_result = await self._extract_and_execute_action(thought_process)
                
                if action_result.success:
                    thought.thought_steps.append(ThoughtStep(
                        step_type="action",
                        content=f"تم تنفيذ الإجراء بنجاح",
                        confidence=1.0,
                        tools_used=[action_result.data.get("tool", "unknown")]
                    ))
                    
                    thought.final_result = action_result.data
                    thought.status = AgentStatus.IDLE
                    break
                else:
                    thought.thought_steps.append(ThoughtStep(
                        step_type="error",
                        content=f"فشل التنفيذ: {action_result.error}",
                        confidence=0.0
                    ))
                    
                    if not self.continue_on_error:
                        thought.status = AgentStatus.ERROR
                        break
            
            thought.completed_at = datetime.utcnow()
            
        except Exception as e:
            logger.error(f"خطأ في دورة الوكيل: {e}")
            thought.status = AgentStatus.ERROR
            thought.thought_steps.append(ThoughtStep(
                step_type="error",
                content=str(e),
                confidence=0.0
            ))
        
        self.thought_history.append(thought)
        self.status = AgentStatus.IDLE
        self.current_task = None
        
        return thought
    
    async def _extract_and_execute_action(self, thought_process: str) -> ActionResult:
        """استخراج الإجراء من نص التفكير وتنفيذه"""
        import re
        
        # البحث عن اسم الأداة في نص التفكير
        tool_pattern = r'(?:استخدم|استدعِ|استعن بـ|استخدام)\s+(?:\"|\')?(\w+)(?:\"|\')?'
        match = re.search(tool_pattern, thought_process, re.IGNORECASE)
        
        if match:
            tool_name = match.group(1)
            params = {"query": thought_process}
            return await self.act(tool_name, params)
        
        return ActionResult(
            success=True,
            data={"message": "اكتمل التفكير بدون الحاجة لأداة خارجية"},
            execution_time_ms=0
        )
    
    def get_status(self) -> Dict[str, Any]:
        """الحصول على حالة الوكيل"""
        return {
            "name": self.name,
            "role": self.role,
            "status": self.status.value,
            "tools_count": len(self._tools),
            "history_count": len(self.thought_history),
            "using_llm": self.using_llm,
            "model": self.model if self.using_llm else None
        }
    
    def clear_history(self):
        """مسح تاريخ التفكير"""
        self.thought_history = []
        logger.info(f"تم مسح تاريخ الوكيل {self.name}")
