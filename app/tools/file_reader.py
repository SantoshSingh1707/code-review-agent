from app.config import MAX_FILE_SIZE
import os

def read_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if len(content) > MAX_FILE_SIZE:
        raise ValueError(f"File too large. Max size: {MAX_FILE_SIZE}")
    
    return content

def read_directory(path: str) -> dict[str, str]:
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Not a directory: {path}")
    
    files = {}
    for filename in os.listdir(path):
        if filename.endswith(".py"):
            filepath = os.path.join(path, filename)
            files[filename] = read_file(filepath)
    return files