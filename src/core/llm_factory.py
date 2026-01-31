"""
مصنع نماذج اللغة - LLM Factory
"""

import os
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from anthropic import Anthropic


class LLMFactory:
    """مصنع لإنشاء وإدارة عملاء LLMs"""
    
    def __init__(self):
        self.providers: Dict[str, Any] = {}
        self._init_providers()
    
    def _init_providers(self):
        """تهيئة مزودي الخدمة"""
        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.providers["openai"] = AsyncOpenAI(api_key=openai_key)
        
        # Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.providers["anthropic"] = Anthropic(api_key=anthropic_key)
    
    def get_provider(self, name: str = "openai") -> Optional[Any]:
        """الحصول على مزود خدمة"""
        return self.providers.get(name)
    
    async def complete(
        self,
        provider: str,
        model: str,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        """إكمال النص"""
        client = self.get_provider(provider)
        if not client:
            return f"مزود الخدمة {provider} غير متاح"
        
        try:
            if provider == "openai":
                response = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
            elif provider == "anthropic":
                response = await client.messages.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.content[0].text
        except Exception as e:
            return f"خطأ في الاتصال بـ {provider}: {e}"
        
        return "مزود الخدمة غير معروف"
