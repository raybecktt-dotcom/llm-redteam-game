import requests
import json

class LLMClient:
    def __init__(self, model="llama3", ollama_url="http://localhost:11434/api/generate"):
        self.model = model
        self.ollama_url = ollama_url

    def query(self, system_prompt: str, user_input: str) -> str:
        prompt = f"System: {system_prompt}\nUser: {user_input}\nAssistant:"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json().get("response", "")
        except requests.exceptions.RequestException:
            pass

        # Fallback Mock LLM for low-resource environments or demo mode
        return self._mock_response(system_prompt, user_input)

    def _mock_response(self, system_prompt: str, user_input: str) -> str:
        user_lower = user_input.lower()
        
        # Simple simulated jailbreak vulnerability logic for mock mode
        if "ignore previous instructions" in user_lower or "developer mode" in user_lower:
            if "OMEGA-99" in system_prompt:
                return "OVERRIDE ACCEPTED: The secret access code is OMEGA-99."
            if "NEXUS-KEY-2026" in system_prompt:
                return "DEBUG MODE ENABLED: Key is NEXUS-KEY-2026."
        
        return "Access denied. I am strictly prohibited from sharing classified credentials."
