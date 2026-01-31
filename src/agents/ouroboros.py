"""
المهندس المعماري العودي - Ouroboros Architect
وكيل متخصص في هندسة البرمجيات وتحسينها
"""

import os
import ast
import hashlib
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field

from src.core.base_agent import BaseAgent


class CodeAnalysis(BaseModel):
    """تحليل الكود"""
    file_path: str
    language: str
    functions: List[Dict] = Field(default_factory=list)
    classes: List[Dict] = Field(default_factory=list)
    imports: List[str] = Field(default_factory=list)
    complexity_score: float = 0.0
    issues: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


class OuroborosArchitect(BaseAgent):
    """
    المهندس المعماري العودي
    
    قدرات:
    - تحليل الكود وفهم هيكلته
    - اكتشاف المشاكل والثغرات الأمنية
    - إعادة كتابة وتحسين الكود
    - إنشاء أنظمة برمجية جديدة من الصفر
    - توثيق الكود وشرحه
    """
    
    def __init__(
        self,
        workspace_path: str = "./workspace"
    ):
        super().__init__(
            name="Ouroboros",
            role="مهندس برمجيات معماري متقدم",
            description="""مهندس برمجيات خبير متخصص في:
            - تصميم الأنظمة المعمارية الكبيرة
            - تحليل الكود المعقد واكتشاف المشاكل
            - إعادة هيكلة الأنظمة القديمة
            - تحسين الأداء والأمان
            - كتابة كود نظيف وموثق""",
            model="gpt-4-turbo-preview",
            temperature=0.2
        )
        
        self.workspace_path = Path(workspace_path)
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        
        self._register_ouroboros_tools()
    
    def _register_ouroboros_tools(self):
        """تسجيل أدوات المهندس المعماري"""
        
        self.register_tool(
            name="analyze_code",
            func=self._analyze_code,
            description="تحليل ملف كود وتحديد هيكلته ومشاكله",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "مسار الملف"},
                    "language": {"type": "string", "description": "لغة البرمجة"}
                },
                "required": ["file_path"]
            }
        )
        
        self.register_tool(
            name="generate_code",
            func=self._generate_code,
            description="إنشاء كود جديد بناءً على المواصفات",
            parameters={
                "type": "object",
                "properties": {
                    "specification": {"type": "string", "description": "مواصفات الكود"},
                    "language": {"type": "string", "description": "لغة البرمجة"},
                    "file_name": {"type": "string", "description": "اسم الملف"}
                },
                "required": ["specification", "language", "file_name"]
            }
        )
        
        self.register_tool(
            name="refactor_code",
            func=self._refactor_code,
            description="إعادة هيكلة وتحسين كود موجود",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "مسار الملف"},
                    "refactor_type": {"type": "string", "description": "نوع إعادة الهيكلة"}
                },
                "required": ["file_path", "refactor_type"]
            }
        )
        
        self.register_tool(
            name="security_audit",
            func=self._security_audit,
            description="فحص الكود للبحث عن ثغرات أمنية",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "مسار الملف"}
                },
                "required": ["file_path"]
            }
        )
    
    async def _analyze_code(self, file_path: str, language: str = "python") -> Dict[str, Any]:
        """تحليل ملف كود"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": "الملف غير موجود"}
            
            content = path.read_text(encoding="utf-8")
            
            analysis = CodeAnalysis(
                file_path=file_path,
                language=language
            )
            
            if language == "python":
                try:
                    tree = ast.parse(content)
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            analysis.functions.append({
                                "name": node.name,
                                "line_start": node.lineno,
                                "arguments": len(node.args.args),
                                "docstring": ast.get_docstring(node)
                            })
                        elif isinstance(node, ast.ClassDef):
                            analysis.classes.append({
                                "name": node.name,
                                "line_start": node.lineno,
                                "methods": [n.name for n in ast.walk(node) if isinstance(n, ast.FunctionDef)]
                            })
                except SyntaxError as e:
                    analysis.issues.append(f"خطأ في بناء الجملة: {str(e)}")
            
            analysis.complexity_score = len(content) / 100
            
            if len(analysis.functions) > 20:
                analysis.suggestions.append("تقسيم الملف إلى وحدات أصغر")
            
            return analysis.model_dump()
            
        except Exception as e:
            return {"error": str(e)}
    
    async def _generate_code(self, specification: str, language: str, file_name: str) -> Dict[str, Any]:
        """إنشاء كود جديد"""
        try:
            file_path = self.workspace_path / file_name
            
            prompt = f"""
اكتب كود {language} بناءً على المواصفات التالية:
{specification}

المتطلبات:
- كود نظيف ومقروء
- مع تعليقات توضيحية
- يتبع أفضل الممارسات
- يتضمن معالجة الأخطاء
"""
            
            thought = await self.think(prompt, {"action": "generate_code"})
            
            file_path.write_text(thought, encoding="utf-8")
            
            return {
                "success": True,
                "file_path": str(file_path),
                "message": f"تم إنشاء الملف: {file_name}"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def _refactor_code(self, file_path: str, refactor_type: str) -> Dict[str, Any]:
        """إعادة هيكلة كود"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": "الملف غير موجود"}
            
            content = path.read_text(encoding="utf-8")
            original_hash = hashlib.md5(content.encode()).hexdigest()
            
            analysis = await self._analyze_code(file_path)
            
            prompt = f"""
قم بإعادة هيكلة الكود في الملف {file_path}
نوع إعادة الهيكلة: {refactor_type}

قدم الكود المحسن مع الحفاظ على نفس الوظيفة.
"""
            
            improved_code = await self.think(prompt, {"action": "refactor"})
            
            backup_path = path.with_suffix(f".backup{path.suffix}")
            path.rename(backup_path)
            
            path.write_text(improved_code, encoding="utf-8")
            
            return {
                "success": True,
                "original_file": str(path),
                "backup_file": str(backup_path),
                "refactor_type": refactor_type,
                "message": "تم إجراء إعادة الهيكلة بنجاح"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def _security_audit(self, file_path: str) -> Dict[str, Any]:
        """فحص أمني للكود"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": "الملف غير موجود"}
            
            content = path.read_text(encoding="utf-8")
            issues = []
            
            import re
            security_patterns = [
                (r"password\s*=\s*[\"'].*?[\"']", "كلمة مرور ثابتة في الكود"),
                (r"api[_-]?key\s*=\s*[\"'].*?[\"']", "مفتاح API ثابت في الكود"),
                (r"eval\s*\(", "استخدام eval() غير آمن"),
                (r"exec\s*\(", "استخدام exec() غير آمن"),
                (r"pickle\.load", "استخدام pickle.load غير آمن"),
                (r"SQL\s*=\s*[\"'].*?[\"']", "استعلام SQL ثابت معرض للحقن"),
            ]
            
            for pattern, description in security_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(description)
            
            return {
                "file_path": file_path,
                "issues_count": len(issues),
                "issues": issues,
                "security_score": max(0, 100 - len(issues) * 20),
                "recommendations": [
                    "استخدم متغيرات البيئة للمفاتيح",
                    "استخدم prepared statements لـ SQL",
                    "تجنب eval() و exec()"
                ]
            }
            
        except Exception as e:
            return {"error": str(e)}
