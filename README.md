# Code Review Agent

An AI-powered code review tool that analyzes Python code for bugs, performance issues, security vulnerabilities, and best practices using local Ollama (LLM).

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Features

- **Code Analysis**: Analyze pasted Python code or files from a path
- **Structured Reviews**: Returns detailed reviews with bugs, code quality, performance, and security issues
- **Scoring**: Provides an overall score (0-10) for code quality
- **Local Privacy**: Uses local Ollama - no cloud API calls or data leaving your machine
- **REST API**: FastAPI-based API for easy integration
- **Web UI**: Simple frontend interface for quick reviews

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Ollama installed locally

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/SantoshSingh1707/code-review-agent.git
cd code-review-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up Ollama**
```bash
# Install Ollama from https://ollama.ai
ollama pull codellama
```

4. **Configure environment**
```bash
copy .env.example .env
```
Edit `.env` to set your model (default: `codellama:latest`)

### Running

1. **Start Ollama** (in a separate terminal)
```bash
ollama serve
```

2. **Start the API**
```bash
python run.py
```

The API will start at `http://127.0.0.1:8002`

## Usage

### Using the Web UI

Open `http://127.0.0.1:8002` in your browser to access the web interface.

### Using the API

#### Health Check
```bash
curl http://127.0.0.1:8002/health
```

#### Analyze Pasted Code
```bash
curl -X POST http://127.0.0.1:8002/analyze/paste \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b): return a + b"}'
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

response = requests.post(
    "http://127.0.0.1:8002/analyze/paste",
    json={"code": "def add(a, b): return a + b"}
)
print(response.json())
```

### API Response Format

```json
{
  "summary": "Brief summary of the analysis",
  "bugs": ["list of bugs found"],
  "code_quality": ["list of code quality issues"],
  "performance": ["list of performance issues"],
  "security": ["list of security issues"],
  "best_practices": ["list of best practice suggestions"],
  "overall_score": 7
}
```

## Project Structure

```
code-review-agent/
├── app/
│   ├── agent/
│   │   ├── agent.py          # Code review agent logic
│   │   ├── ollama_client.py # Ollama API client
│   │   └── prompts.py       # Prompt templates
│   ├── tools/
│   │   ├── code_runner.py  # Code execution utility
│   │   └── file_reader.py  # File reading utility
│   ├── config.py          # Configuration
│   ├── models.py         # Pydantic models
│   └── main.py          # FastAPI application
├── frontend/             # Web UI
├── tests/              # Test files
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
└── run.py             # Server startup
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

## Running Tests

```bash
python -m pytest tests/ -v
```

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

MIT License - feel free to use, modify, and distribute.