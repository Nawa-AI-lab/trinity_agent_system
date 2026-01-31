"""
نماذج البيانات - Data Models
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


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


class ToolDefinition(BaseModel):
    """تعريف أداة"""
    name: str
    description: str
    parameters: Dict[str, Any]
    function: Any


class AgentDefinition(BaseModel):
    """تعريف وكيل"""
    name: str
    role: str
    description: str
    model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    tools: List[ToolDefinition] = Field(default_factory=list)
