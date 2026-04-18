# Code Review Agent

An AI-powered code review tool that analyzes Python code for bugs, performance issues, security vulnerabilities, and best practices using Ollama (LLM).

## Features

- Analyze pasted Python code
- Analyze Python files from a path
- Returns structured review with score (0-10)
- Uses local Ollama for privacy (no cloud API calls)

## Requirements

- Python 3.11+
- Ollama installed locally

## Installation

1. **Clone or download this project**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up Ollama:**
```bash
# Install Ollama from https://ollama.ai
ollama pull codellama
```

4. **Configure environment:**
```bash
# Copy the example environment file
copy .env.example .env
```

Edit `.env` to set your model:
```
OLLAMA_MODEL=codellama:latest
```

## Usage

### Start Ollama (Terminal 1)
```bash
ollama serve
```

### Start the API (Terminal 2)
```bash
python run.py
```

The API will start at `http://127.0.0.1:8002`

### Test the API

#### Health Check
```bash
curl http://127.0.0.1:8002/health
```

Response:
```json
{"status": "connected", "model": "codellama:latest"}
```

#### Analyze Pasted Code
```bash
curl -X POST http://127.0.0.1:8002/analyze/paste \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b): return a + b"}'
```

Response:
```json
{
  "summary": "The function is correct but lacks type hints and documentation",
  "bugs": [],
  "code_quality": [],
  "performance": [],
  "security": [],
  "best_practices": [],
  "overall_score": 7
}
```

#### Analyze Files
```bash
curl -X POST http://127.0.0.1:8002/analyze/files \
  -H "Content-Type: application/json" \
  -d '{"path": "path/to/your/file.py"}'
```

#### Using Python
```python
import requests

# Analyze code
response = requests.post(
    "http://127.0.0.1:8002/analyze/paste",
    json={"code": "def add(a, b): return a + b"}
)
print(response.json())
```

## Project Structure

```
code-review-agent/
├── app/
│   ├── __init__.py
│   ├── config.py           # Configuration settings
│   ├── models.py           # Pydantic models
│   ├── main.py             # FastAPI application
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py        # Code review agent
│   │   ├── ollama_client.py # Ollama API client
│   │   └── prompts.py      # Prompt templates
│   └── tools/
│       ├── __init__.py
│       └── file_reader.py  # File reading utility
├── tests/
│   ├── __init__.py
│   └── test_api.py        # API tests
├── .env                   # Environment variables
├── .env.example           # Environment template
├── requirements.txt      # Python dependencies
└── run.py                 # Server startup script
```

## Running Tests

```bash
python -m pytest tests/test_api.py -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/analyze/paste` | Analyze pasted code |
| POST | `/analyze/files` | Analyze Python file |

## Configuration

Edit `.env` to customize:

| Variable | Default | Description |
|----------|----------|-------------|
| OLLAMA_BASE_URL | http://localhost:11434 | Ollama server URL |
| OLLAMA_MODEL | codellama:latest | Model to use |
| MAX_FILE_SIZE | 100000 | Max characters for file reading |

## Troubleshooting

### Ollama not running
```bash
ollama serve
```

### Port already in use
Change port in `run.py`:
```python
uvicorn.run("app.main:app", host="127.0.0.1", port=8003)
```

### Model not found
```bash
ollama pull codellama
```

## License

MIT