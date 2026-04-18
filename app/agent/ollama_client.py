import json
import httpx
from app.config import OLLAMA_MODEL

OLLAMA_BASE_URL = "http://localhost:11434"

class OllamaClient:
    def __init__(self) -> None:
        self.base_url = OLLAMA_BASE_URL
        self.model = OLLAMA_MODEL

    def is_connected(self) -> bool:
        try:
            with httpx.Client() as client:
                response = client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False
    
    def chat(self, messages: list[dict]) -> str:
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/api/chat",
                json={"model": self.model, "messages": messages},
                timeout=120.0
            )
            response.raise_for_status()
            
            text = response.text.strip()
            lines = text.split('\n')
            final_content = ""
            final_thinking = ""
            
            for line in lines:
                try:
                    data = json.loads(line)
                    msg = data.get("message", {})
                    content = msg.get("content", "")
                    thinking = msg.get("thinking", "")
                    if content:
                        final_content += content
                    if thinking:
                        final_thinking += thinking + " "
                    if data.get("done", False):
                        break
                except:
                    continue
            
            if final_content:
                return final_content
            elif final_thinking:
                return final_thinking.strip()
            return text
    
    def get_model_info(self) -> dict:
        connected = self.is_connected()
        return {
            "model": self.model if connected else None,
            "status": "connected" if connected else "disconnected"
        }