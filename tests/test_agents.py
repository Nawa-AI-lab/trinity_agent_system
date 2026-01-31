"""
Tests - اختبارات النظام
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock


class TestAgents:
    """اختبارات الوكلاء"""
    
    @pytest.fixture
    def mock_openai_client(self):
        """إنشاء عميل OpenAI وهمي"""
        client = AsyncMock()
        response = MagicMock()
        response.choices = [MagicMock()]
        response.choices[0].message.content = "تم تنفيذ المهمة بنجاح"
        client.chat.completions.create = AsyncMock(return_value=response)
        return client
    
    def test_agent_initialization(self):
        """اختبار تهيئة الوكيل"""
        from src.agents.ouroboros import OuroborosArchitect
        
        agent = OuroborosArchitect()
        assert agent.name == "Ouroboros"
        assert agent.role == "مهندس برمجيات معماري متقدم"
    
    def test_agent_status(self):
        """اختبار حالة الوكيل"""
        from src.core.base_agent import BaseAgent, AgentStatus
        
        class TestAgent(BaseAgent):
            def __init__(self):
                super().__init__(
                    name="TestAgent",
                    role="Test Role",
                    description="Test Description"
                )
        
        agent = TestAgent()
        status = agent.get_status()
        assert status["name"] == "TestAgent"
        assert status["status"] == AgentStatus.IDLE.value


class TestTools:
    """اختبارات الأدوات"""
    
    def test_browser_tool_import(self):
        """اختبار استيراد أداة المتصفح"""
        from src.tools.browser_tool import BrowserTool
        assert BrowserTool is not None
    
    def test_search_tool_import(self):
        """اختبار استيراد أداة البحث"""
        from src.tools.search_tool import SearchTool
        assert SearchTool is not None


class TestUtils:
    """اختبارات الأدوات المساعدة"""
    
    def test_format_response(self):
        """اختبار تنسيق الاستجابة"""
        from src.utils.helpers import format_response
        
        response = format_response({"key": "value"})
        assert response["status"] == "success"
        assert response["data"]["key"] == "value"
    
    def test_parse_json_safe(self):
        """اختبار تحليل JSON بأمان"""
        from src.utils.helpers import parse_json_safe
        
        result = parse_json_safe('{"key": "value"}')
        assert result == {"key": "value"}
        
        result = parse_json_safe("invalid json")
        assert result is None
