"""
محرك المهام - Task Engine
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio


class TaskStatus(str, Enum):
    """حالة المهمة"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """مهمة"""
    id: str
    name: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 1
    agent_name: str = ""
    params: Dict = field(default_factory=dict)
    result: Optional[Dict] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class TaskEngine:
    """محرك إدارة المهام"""
    
    def __init__(self, max_concurrent: int = 5):
        self.tasks: Dict[str, Task] = {}
        self.queue: List[Task] = []
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    def add_task(self, task: Task):
        """إضافة مهمة"""
        self.tasks[task.id] = task
        self.queue.append(task)
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """الحصول على مهمة"""
        return self.tasks.get(task_id)
    
    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """قائمة المهام"""
        if status:
            return [t for t in self.tasks.values() if t.status == status]
        return list(self.tasks.values())
    
    async def execute_task(self, task: Task, agent) -> Dict:
        """تنفيذ مهمة"""
        async with self.semaphore:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.utcnow()
            
            try:
                result = await agent.run(
                    task.name,
                    task.params
                )
                task.result = result.model_dump()
                task.status = TaskStatus.COMPLETED
            except Exception as e:
                task.error = str(e)
                task.status = TaskStatus.FAILED
            
            task.completed_at = datetime.utcnow()
            return task.result or {}
    
    async def run_all(self, agents: Dict[str, Any]):
        """تشغيل جميع المهام"""
        for task in self.queue:
            agent = agents.get(task.agent_name)
            if agent:
                await self.execute_task(task, agent)
