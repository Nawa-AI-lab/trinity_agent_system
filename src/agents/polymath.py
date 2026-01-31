"""
المركّب المعرفي الشامل - Polymath Synthesizer
وكيل متخصص في البحث وجمع المعلومات وربط المعارف من مجالات متعددة
"""

import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict
from pydantic import BaseModel, Field

from src.core.base_agent import BaseAgent


class ResearchResult(BaseModel):
    """نتيجة البحث"""
    query_id: str
    title: str
    summary: str
    key_findings: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    relevance_score: float = Field(ge=0, le=1)


class KnowledgeConnection(BaseModel):
    """رابط معرفي"""
    concept_a: str
    concept_b: str
    connection_type: str
    confidence: float = Field(ge=0, le=1)
    explanation: str


class SynthesisReport(BaseModel):
    """تقرير التركيب"""
    report_id: str
    topic: str
    executive_summary: str
    key_insights: List[str] = Field(default_factory=list)
    connections_found: List[KnowledgeConnection] = Field(default_factory=list)
    sources_analyzed: int
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class PolymathSynthesizer(BaseAgent):
    """
    المركّب المعرفي الشامل
    
    قدرات:
    - البحث في مصادر متعددة (ويب، أكاديميا، قواعد بيانات)
    - استخراج وتحليل المعلومات
    - ربط المفاهيم من مجالات مختلفة
    - اكتشاف أنماط وعلاقات مخفية
    - توليد رؤى وأفكار جديدة
    """
    
    def __init__(self):
        super().__init__(
            name="Polymath",
            role="باحث ومركّب معرفي متعدد التخصصات",
            description="""باحث ذكي قادر على:
            - البحث العميق في مصادر متعددة
            - تحليل واستخراج المعلومات المهمة
            - ربط المفاهيم من مجالات علمية مختلفة
            - اكتشاف أنماط وأفكار جديدة
            - تقديم رؤى قابلة للتنفيذ""",
            model="gpt-4-turbo-preview",
            temperature=0.3
        )
        
        self.knowledge_graph: Dict[str, Dict] = defaultdict(dict)
        self.concepts_index: Dict[str, List[str]] = defaultdict(list)
        self.research_history: List[ResearchResult] = []
        
        self._register_polymath_tools()
    
    def _register_polymath_tools(self):
        """تسجيل أدوات المركّب المعرفي"""
        
        self.register_tool(
            name="comprehensive_search",
            func=self._comprehensive_search,
            description="بحث شامل في مصادر متعددة",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "سؤال البحث"},
                    "sources": {"type": "array", "description": "المصادر المطلوبة"},
                    "depth": {"type": "string", "description": "عمق البحث"}
                },
                "required": ["query"]
            }
        )
        
        self.register_tool(
            name="extract_data",
            func=self._extract_data,
            description="استخراج بيانات محددة من نص أو صفحة",
            parameters={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "المحتوى"},
                    "data_type": {"type": "string", "description": "نوع البيانات"}
                },
                "required": ["content", "data_type"]
            }
        )
        
        self.register_tool(
            name="connect_concepts",
            func=self._connect_concepts,
            description="ربط مفهومين أو أكثر من مجالات مختلفة",
            parameters={
                "type": "object",
                "properties": {
                    "concepts": {"type": "array", "description": "المفاهيم"},
                    "domains": {"type": "array", "description": "المجالات"}
                },
                "required": ["concepts"]
            }
        )
        
        self.register_tool(
            name="generate_insights",
            func=self._generate_insights,
            description="توليد رؤى من مجموعة بيانات",
            parameters={
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "البيانات"},
                    "context": {"type": "string", "description": "السياق"}
                },
                "required": ["data"]
            }
        )
    
    async def _comprehensive_search(
        self,
        query: str,
        sources: Optional[List[str]] = None,
        depth: str = "medium"
    ) -> Dict[str, Any]:
        """بحث شامل في مصادر متعددة"""
        results = []
        sources = sources or ["web", "news", "academic"]
        depth_map = {"shallow": 3, "medium": 5, "deep": 10}
        num_results = depth_map.get(depth, 5)
        
        # محاكاة نتائج البحث
        simulated_results = [
            {
                "title": f"نتيجة بحث 1 عن {query}",
                "url": f"https://example1.com/{query}",
                "snippet": f"محتوى متعلق بـ {query}",
                "relevance": 0.9
            },
            {
                "title": f"نتيجة بحث 2 عن {query}",
                "url": f"https://example2.com/{query}",
                "snippet": f"معلومات مهمة حول {query}",
                "relevance": 0.85
            },
            {
                "title": f"نتيجة بحث 3 عن {query}",
                "url": f"https://example3.com/{query}",
                "snippet": f"تحليل شامل لـ {query}",
                "relevance": 0.8
            }
        ]
        
        results.extend(simulated_results[:num_results])
        
        return {
            "query": query,
            "sources_searched": sources,
            "total_results": len(results),
            "top_results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _extract_data(
        self,
        content: str,
        data_type: str
    ) -> Dict[str, Any]:
        """استخراج بيانات محددة من المحتوى"""
        prompt = f"""
استخرج بيانات النوع '{data_type}' من النص التالي:

النص:
{content}

قدم البيانات المستخرجة كـ JSON:
"""
        
        extraction = await self.think(prompt, {"action": "extract", "data_type": data_type})
        
        return {
            "data_type": data_type,
            "extracted_data": {"raw": extraction},
            "content_length": len(content)
        }
    
    async def _connect_concepts(
        self,
        concepts: List[str],
        domains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """ربط مفاهيم من مجالات مختلفة"""
        domains = domains or ["technology", "science", "business"]
        
        prompt = f"""
ابحث عن روابط بين المفاهيم التالية من مجالات مختلفة:

المفاهيم: {json.dumps(concepts, ensure_ascii=False)}
المجالات: {json.dumps(domains, ensure_ascii=False)}

لكل زوج مفاهيم، حدد:
1. هل هناك تشابه؟
2. هل هناك تكامل؟
3. ما الفائدة من هذا الربط؟
"""
        
        analysis = await self.think(prompt, {"action": "connect", "concepts": concepts})
        
        for i, concept_a in enumerate(concepts):
            for concept_b in concepts[i+1:]:
                connection = KnowledgeConnection(
                    concept_a=concept_a,
                    concept_b=concept_b,
                    connection_type="complementary",
                    confidence=0.7,
                    explanation=analysis
                )
                self.knowledge_graph[concept_a][concept_b] = connection
        
        return {
            "concepts": concepts,
            "domains": domains,
            "analysis": analysis,
            "connections_count": len(concepts) * (len(concepts) - 1) // 2
        }
    
    async def _generate_insights(
        self,
        data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """توليد رؤى من البيانات"""
        prompt = f"""
بناءً على البيانات التالية، قدم رؤى قابلة للتنفيذ:

السياق: {context}

البيانات:
{json.dumps(data, ensure_ascii=False, indent=2)}

قدم:
1. الأنماط المكتشفة
2. الفرص المخفية
3. التوصيات العملية
"""
        
        insights = await self.think(prompt, {"action": "insights"})
        
        return {
            "context": context,
            "insights": insights,
            "patterns": ["نمط 1", "نمط 2"],
            "opportunities": ["فرصة 1", "فرصة 2"],
            "recommendations": ["توصية 1", "توصية 2"]
        }
    
    async def conduct_deep_research(
        self,
        topic: str,
        domains: List[str],
        depth: str = "deep"
    ) -> SynthesisReport:
        """إجراء بحث عميق في موضوع معين"""
        search_results = await self._comprehensive_search(
            query=topic,
            sources=["web", "academic", "news"],
            depth=depth
        )
        
        concepts = self._extract_concepts(topic)
        connections = await self._connect_concepts(concepts, domains)
        
        insights = await self._generate_insights(
            data={
                "research_results": search_results,
                "connections": connections
            },
            context=f"Deep research on {topic}"
        )
        
        report = SynthesisReport(
            report_id=f"sr_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            topic=topic,
            executive_summary=f"بحث شامل في مجال {topic}",
            key_insights=insights.get("insights", ""),
            connections_found=[],
            sources_analyzed=len(search_results.get("top_results", []))
        )
        
        return report
    
    def _extract_concepts(self, topic: str) -> List[str]:
        """استخراج المفاهيم الرئيسية من الموضوع"""
        words = re.findall(r'\b[A-Za-zأ-ي]+\b', topic)
        stop_words = {"the", "a", "an", "is", "are", "in", "on", "at", "to", "for", "of", "and", "or", "في", "من", "على", "و", "أو"}
        concepts = [w for w in words if w.lower() not in stop_words and len(w) > 2]
        return list(set(concepts))[:10]
