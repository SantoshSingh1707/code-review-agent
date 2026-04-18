import pytest
import os
import tempfile
from app.tools.file_reader import read_file, read_directory

def test_read_file_success():
    """Test reading a file successfully"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
        f.write("def test(): pass")
        temp_path = f.name
    
    try:
        content = read_file(temp_path)
        assert content == "def test(): pass"
    finally:
        os.unlink(temp_path)

def test_read_file_not_found():
    """Test reading non-existent file"""
    with pytest.raises(FileNotFoundError):
        read_file("nonexistent_file.py")

def test_read_file_size_limit():
    """Test file size limit"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
        f.write("x" * 200000)
        temp_path = f.name
    
    try:
        with pytest.raises(ValueError):
            read_file(temp_path)
    finally:
        os.unlink(temp_path)

def test_read_directory():
    """Test reading directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, "test1.py")
        file2 = os.path.join(tmpdir, "test2.py")
        
        with open(file1, 'w') as f:
            f.write("def func1(): pass")
        with open(file2, 'w') as f:
            f.write("def func2(): pass")
        
        result = read_directory(tmpdir)
        assert len(result) == 2
        assert "test1.py" in result
        assert "test2.py" in result
