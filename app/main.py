from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models import (
    AnalysisResponse,
    HealthResponse,
    AnalyzeRequest,
    FileAnalyzeRequest,
    ExecuteRequest
)
from app.agent.agent import CodeReviewAgent
from app.tools.code_runner import run_code, ExecutionResult
import traceback

app = FastAPI(title="Code Review Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = CodeReviewAgent()

@app.get("/health", response_model=HealthResponse)
def health_check():
    model_info = agent.ollama.get_model_info()
    return HealthResponse(
        status=model_info["status"],
        model=model_info["model"]
    )

@app.post("/analyze/paste", response_model=AnalysisResponse)
def analyze_paste(request: AnalyzeRequest):
    try:
        result = agent.analyze_code(request.code, request.focus_areas)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/analyze/files", response_model=AnalysisResponse)
def analyze_files(request: FileAnalyzeRequest):
    try:
        return agent.analyze_files(request.path, request.focus_areas)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute/code")
def execute_code(request: ExecuteRequest):
    try:
        result = run_code(request.code)
        return {
            "success": result.success,
            "output": result.output,
            "error": result.error,
            "return_value": str(result.return_value) if result.return_value else None
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
    
