# توثيق نظام الثالوث للوكلاء الذكية

## نظرة عامة

نظام الثالوث هو إطار عمل متكامل للوكلاء الذكية المتخصصة في مجالات مختلفة.

## الوكلاء المتاحون

### 1. المهندس المعماري العودي (Ouroboros)

**المسؤوليات:**
- تحليل الكود وفهم هيكلته
- اكتشاف المشاكل والثغرات الأمنية
- إعادة كتابة وتحسين الكود
- إنشاء أنظمة برمجية جديدة من الصفر

**الأدوات:**
- `analyze_code`: تحليل ملف كود
- `generate_code`: إنشاء كود جديد
- `refactor_code`: إعادة هيكلة الكود
- `security_audit`: فحص أمني

### 2. الرئيس التنفيذي المجهري (Micro-CEO)

**المسؤوليات:**
- تحليل السوق والمنافسين
- تخطيط الأعمال والاستراتيجية
- إدارة الميزانية والموارد
- اتخاذ القرارات بناءً على البيانات

**الأدوات:**
- `market_analysis`: تحليل السوق
- `business_plan`: إنشاء خطة عمل
- `budget_management`: إدارة الميزانية
- `generate_report`: إنشاء تقارير

### 3. المركّب المعرفي الشامل (Polymath)

**المسؤوليات:**
- البحث في مصادر متعددة
- استخراج وتحليل المعلومات
- ربط المفاهيم من مجالات مختلفة
- اكتشاف أنماط وعلاقات مخفية

**الأدوات:**
- `comprehensive_search`: بحث شامل
- `extract_data`: استخراج البيانات
- `connect_concepts`: ربط المفاهيم
- `generate_insights`: توليد الرؤى

## API Reference

### نقاط النهاية الرئيسية

| الطريقة | العنوان | الوصف |
|---------|---------|-------|
| GET | `/health` | فحص صحة النظام |
| GET | `/agents` | قائمة الوكلاء |
| GET | `/system/status` | حالة النظام |
| POST | `/agent/{name}/run` | تشغيل وكيل |
| GET | `/agent/{name}/history` | تاريخ الوكيل |

## التطوير

### إضافة وكيل جديد

```python
from src.core.base_agent import BaseAgent

class NewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="NewAgent",
            role="دور الوكيل",
            description="وصف الوكيل"
        )
        self._register_tools()
    
    def _register_tools(self):
        self.register_tool(
            name="tool_name",
            func=self.tool_function,
            description="وصف الأداة",
            parameters={...}
        )
```

## الترخيص

MIT License
