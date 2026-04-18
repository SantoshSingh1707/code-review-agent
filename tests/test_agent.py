import pytest
from app.agent.agent import CodeReviewAgent
from app.agent.ollama_client import OllamaClient
from unittest.mock import patch

def test_agent_init():
    """Test that agent initializes correctly"""
    agent = CodeReviewAgent()
    assert agent.ollama is not None
    assert isinstance(agent.ollama, OllamaClient)

def test_analyze_code_with_focus_areas():
    """Test analyze_code with focus areas"""
    agent = CodeReviewAgent()
    with patch.object(agent.ollama, 'chat') as mock_chat:
        mock_chat.return_value = '{"summary": "Good", "overall_score": 8}'
        result = agent.analyze_code("def test(): pass", focus_areas=["security"])
        assert result.summary == "Good"
        assert result.overall_score == 8

def test_analyze_code_default_score():
    """Test that default score is 5 when parsing fails"""
    agent = CodeReviewAgent()
    with patch.object(agent.ollama, 'chat') as mock_chat:
        mock_chat.return_value = "invalid json response"
        result = agent.analyze_code("def test(): pass")
        assert result.overall_score == 5
