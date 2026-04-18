import pytest
from app.tools.code_runner import run_code, run_function, ExecutionResult

def test_run_code_simple():
    """Test running simple code"""
    result = run_code("print('Hello, World!')")
    assert result.success is True
    assert "Hello, World!" in result.output

def test_run_code_with_return():
    """Test code that returns a value"""
    result = run_code("x = 2 + 2\nresult = x")
    assert result.success is True

def test_run_code_with_error():
    """Test code with syntax error"""
    result = run_code("print(undefined_var)")
    assert result.success is False
    assert "NameError" in result.error or "error" in result.error.lower()

def test_run_code_with_exception():
    """Test code that raises exception"""
    result = run_code("raise ValueError('test error')")
    assert result.success is False

def test_run_function():
    """Test running a specific function"""
    code = "def add(a, b):\n    return a + b"
    result = run_function(code, "add", (2, 3))
    assert result.success is True
    assert result.return_value == 5

def test_run_code_complex():
    """Test running complex code"""
    code = "result = sum([1, 2, 3, 4, 5])"
    result = run_code(code)
    assert result.success is True