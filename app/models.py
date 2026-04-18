from pydantic import BaseModel
from typing import Optional

class AnalysisResponse(BaseModel):
    summary: str = "Analysis complete"
    bugs: list = []
    code_quality: list = []
    performance: list = []
    security: list = []
    best_practices: list = []
    overall_score: int = 5

class HealthResponse(BaseModel):
    status: str = "unknown"
    model: str = "unknown"

class AnalyzeRequest(BaseModel):
    code: str
    focus_areas: Optional[list[str]] = None

class FileAnalyzeRequest(BaseModel):
    path: str
    focus_areas: Optional[list[str]] = None

class ExecuteRequest(BaseModel):
    code: str