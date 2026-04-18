import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_connected():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "connected"
    assert data["model"] is not None

def test_health_response_structure():
    response =client.get("/health")
    data = response.json()
    assert "status" in data
    assert "model" in data

def test_analyze_paste_simple_function():
    time.sleep(1)
    response = client.post("/analyze/paste" , json={"code":"def add(a,b):\n  return a+b"})
    if response.status_code==500:
        pytest.skip("Ollama temporarily unavailable")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "overall_score" in data

def test_execute_code_simple():
    """Test executing simple code"""
    response = client.post("/execute/code", json={"code": "print(2 + 2)"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "4" in data["output"]

def test_execute_code_with_error():
    """Test executing code with error"""
    response = client.post("/execute/code", json={"code": "print(undefined_var)"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"] != ""

def test_execute_code_with_return():
    """Test executing code that returns value"""
    response = client.post("/execute/code", json={"code": "result = 5 + 3"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

