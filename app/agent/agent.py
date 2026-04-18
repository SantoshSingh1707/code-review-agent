import json
import re
from app.agent.ollama_client import OllamaClient
from app.agent.prompts import SYSTEM_PROMPT, USER_PROMPT
from app.models import AnalysisResponse
from app.tools.file_reader import read_file

FALLBACK_PROMPT = """Quick review of this Python code:
```
{code}
```
Respond with just: {"summary":"...","overall_score":5}"""

class CodeReviewAgent:
    def __init__(self) -> None:
        self.ollama = OllamaClient()

    def _parse_response(self, response: str) -> dict:
        cleaned = response.strip()
        
        # Try to extract JSON from markdown or extra text
        json_match = re.search(r'\{[\s\S]*\}', cleaned)
        if json_match:
            cleaned = json_match.group(0)
        
        # Remove markdown code blocks
        cleaned = re.sub(r'^```json\s*', '', cleaned)
        cleaned = re.sub(r'^```\s*$', '', cleaned)
        cleaned = cleaned.strip()
        
        return json.loads(cleaned)

    def analyze_code(self, code: str, focus_areas: list = None) -> AnalysisResponse:
        system_content = SYSTEM_PROMPT
        user_content = USER_PROMPT.format(code=code)
        
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

        try:
            response = self.ollama.chat(messages)
            data = self._parse_response(response)
            
            return AnalysisResponse(
                summary=data.get("summary", "Analysis complete."),
                overall_score=int(data.get("overall_score", 5)),
                bugs=data.get("bugs", []),
                security=data.get("security", []),
                performance=data.get("performance", []),
                code_quality=data.get("code_quality", []),
                best_practices=data.get("best_practices", [])
            )
        except Exception as e:
            # Try fallback with shorter prompt
            try:
                fallback_messages = [
                    {"role": "system", "content": "You are a code reviewer. Respond with JSON only."},
                    {"role": "user", "content": FALLBACK_PROMPT.format(code=code)}
                ]
                response = self.ollama.chat(fallback_messages)
                data = self._parse_response(response)
                
                return AnalysisResponse(
                    summary=data.get("summary", "Analysis completed with basic review."),
                    overall_score=int(data.get("overall_score", 5)),
                    bugs=[],
                    security=[],
                    performance=[],
                    code_quality=[],
                    best_practices=[]
                )
            except:
                return AnalysisResponse(
                    summary=f"Analysis failed: {str(e)}. Please check Ollama is running.",
                    overall_score=5,
                    bugs=[],
                    security=[],
                    performance=[],
                    code_quality=[],
                    best_practices=[]
                )

    def analyze_files(self, path: str, focus_areas: list = None) -> AnalysisResponse:
        code = read_file(path)
        return self.analyze_code(code, focus_areas)