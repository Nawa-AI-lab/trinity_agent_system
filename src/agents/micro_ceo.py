"""
الرئيس التنفيذي المجهري - Micro-CEO Entity
وكيل متخصص في إدارة المشاريع والأعمال واتخاذ القرارات الاستراتيجية
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

from src.core.base_agent import BaseAgent


class BusinessGoal(BaseModel):
    """هدف تجاري"""
    id: str
    name: str
    description: str
    target_value: Decimal
    current_value: Decimal = Decimal("0")
    deadline: Optional[datetime] = None
    priority: int = 1
    metrics: List[str] = Field(default_factory=list)


class ResourceAllocation(BaseModel):
    """تخصيص الموارد"""
    resource_type: str
    allocated_amount: Decimal
    used_amount: Decimal = Decimal("0")
    unit: str
    allocated_to: str


class BusinessReport(BaseModel):
    """تقرير الأعمال"""
    report_id: str
    period: str
    goals_achieved: int
    goals_total: int
    resources_used: Decimal
    resources_budget: Decimal
    key_insights: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)


class MicroCEO(BaseAgent):
    """
    الرئيس التنفيذي المجهري
    
    قدرات:
    - تحليل السوق والمنافسين
    - تخطيط الأعمال والاستراتيجية
    - إدارة الميزانية والموارد
    - اتخاذ القرارات بناءً على البيانات
    - إنشاء التقارير والوثائق
    """
    
    def __init__(self, initial_budget: float = 1000.0, currency: str = "USD"):
        super().__init__(
            name="MicroCEO",
            role="مدير تنفيذي ذكي",
            description="""رئيس تنفيذي ذكي قادر على:
            - تحليل السوق واتخاذ قرارات استراتيجية
            - تخطيط وتنفيذ المشاريع من الصفر
            - إدارة الميزانية والموارد بفعالية
            - إنشاء شركات ومشاريع قابلة للربح
            - تحليل المنافسين وتحديد الفرص""",
            model="gpt-4-turbo-preview",
            temperature=0.5
        )
        
        self.budget = Decimal(str(initial_budget))
        self.currency = currency
        self.expenses: List[Dict] = []
        self.goals: Dict[str, BusinessGoal] = {}
        self.decision_history: List[Dict] = []
        
        self._register_ceo_tools()
    
    def _register_ceo_tools(self):
        """تسجيل أدوات الرئيس التنفيذي"""
        
        self.register_tool(
            name="market_analysis",
            func=self._market_analysis,
            description="تحليل السوق المستهدف والمنافسين",
            parameters={
                "type": "object",
                "properties": {
                    "market": {"type": "string", "description": "اسم السوق أو المنتج"},
                    "scope": {"type": "string", "description": "نطاق التحليل"}
                },
                "required": ["market"]
            }
        )
        
        self.register_tool(
            name="business_plan",
            func=self._create_business_plan,
            description="إنشاء خطة عمل كاملة للمشروع",
            parameters={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string", "description": "اسم المشروع"},
                    "description": {"type": "string", "description": "وصف المشروع"},
                    "target_audience": {"type": "string", "description": "الجمهور المستهدف"}
                },
                "required": ["project_name", "description"]
            }
        )
        
        self.register_tool(
            name="budget_management",
            func=self._manage_budget,
            description="إدارة الميزانية وتتبع المصروفات",
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "description": "إجراء: allocate, spend, report"},
                    "amount": {"type": "number", "description": "المبلغ"},
                    "category": {"type": "string", "description": "الفئة"},
                    "description": {"type": "string", "description": "الوصف"}
                },
                "required": ["action"]
            }
        )
        
        self.register_tool(
            name="generate_report",
            func=self._generate_report,
            description="إنشاء تقرير أداء شامل",
            parameters={
                "type": "object",
                "properties": {
                    "report_type": {"type": "string", "description": "نوع التقرير"},
                    "period": {"type": "string", "description": "الفترة الزمنية"}
                },
                "required": ["report_type"]
            }
        )
    
    async def _market_analysis(self, market: str, scope: str = "global") -> Dict[str, Any]:
        """تحليل السوق والمنافسين"""
        prompt = f"""
قم بتحليل السوق التالي: {market}
نطاق التحليل: {scope}

قدم تحليل شامل يتضمن:
1. حجم السوق ونموه المتوقع
2. أهم اللاعبين والمنافسين
3. الاتجاهات الحالية والمستقبلية
4. الفرص والتهديدات
5. شرائح العملاء المستهدفة
6. استراتيجيات التسعير الشائعة
"""
        
        analysis = await self.think(prompt, {"action": "market_analysis"})
        
        return {
            "market": market,
            "scope": scope,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _create_business_plan(
        self,
        project_name: str,
        description: str,
        target_audience: str = "general"
    ) -> Dict[str, Any]:
        """إنشاء خطة عمل كاملة"""
        prompt = f"""
أنشئ خطة عمل كاملة للمشروع التالي:

اسم المشروع: {project_name}
الوصف: {description}
الجمهور المستهدف: {target_audience}

الميزانية المتاحة: {self.budget} {self.currency}

قدم خطة عمل تتضمن:
1. الملخص التنفيذي
2. وصف المنتج/الخدمة
3. تحليل السوق
4. استراتيجية التسويق
5. الخطة المالية
6. الجدول الزمني للتنفيذ
"""
        
        business_plan = await self.think(prompt, {"action": "business_plan"})
        
        plan_id = f"plan_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "plan_id": plan_id,
            "project_name": project_name,
            "plan": business_plan
        }
    
    async def _manage_budget(
        self,
        action: str,
        amount: Optional[float] = None,
        category: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """إدارة الميزانية"""
        if action == "allocate":
            if amount is None:
                return {"error": "المبلغ مطلوب"}
            
            self.budget += Decimal(str(amount))
            
            return {
                "action": "allocated",
                "amount": amount,
                "new_balance": float(self.budget),
                "message": f"تم تخصيص {amount} {self.currency}"
            }
            
        elif action == "spend":
            if amount is None:
                return {"error": "المبلغ مطلوب"}
            if Decimal(str(amount)) > self.budget:
                return {"error": "الميزانية غير كافية"}
            
            self.budget -= Decimal(str(amount))
            self.expenses.append({
                "amount": amount,
                "category": category or "general",
                "description": description or "",
                "timestamp": datetime.utcnow().isoformat()
            })
            
            return {
                "action": "spent",
                "amount": amount,
                "category": category,
                "new_balance": float(self.budget)
            }
            
        elif action == "report":
            total_expenses = sum(e["amount"] for e in self.expenses)
            
            return {
                "current_balance": float(self.budget),
                "total_expenses": total_expenses,
                "transaction_count": len(self.expenses)
            }
        
        return {"error": "إجراء غير معروف"}
    
    async def _generate_report(self, report_type: str, period: str = "monthly") -> Dict[str, Any]:
        """إنشاء تقرير أداء"""
        budget_report = await self._manage_budget("report")
        
        goals_summary = {
            "achieved": len([g for g in self.goals.values() 
                           if g.current_value >= g.target_value]),
            "total": len(self.goals)
        }
        
        report = BusinessReport(
            report_id=f"rpt_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            period=period,
            goals_achieved=goals_summary["achieved"],
            goals_total=goals_summary["total"],
            resources_used=budget_report.get("total_expenses", 0),
            resources_budget=float(self.budget),
            key_insights=[
                "تقدم ملحوظ في تحقيق الأهداف المحددة",
                "إدارة الميزانية فعالة"
            ],
            recommendations=[
                "زيادة الاستثمار في التسويق",
                "توسيع قاعدة العملاء"
            ],
            next_actions=[
                "مراجعة الأهداف الشهرية",
                "تحديث استراتيجية المحتوى"
            ]
        )
        
        return report.model_dump()
    
    async def launch_company(
        self,
        company_type: str,
        niche: str,
        initial_investment: float = 1000.0
    ) -> Dict[str, Any]:
        """إطلاق شركة جديدة"""
        await self._manage_budget("allocate", initial_investment, "initial_capital")
        
        market_data = await self._market_analysis(niche)
        
        plan = await self._create_business_plan(
            project_name=f"{company_type} in {niche}",
            description=f"شركة متخصصة في مجال {niche}",
            target_audience="العملاء المستهدفون"
        )
        
        return {
            "company_type": company_type,
            "niche": niche,
            "investment": initial_investment,
            "market_analysis": market_data,
            "business_plan": plan,
            "status": "launched"
        }
