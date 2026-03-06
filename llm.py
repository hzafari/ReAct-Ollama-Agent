import requests
import json

class LocalLLM:
    def __init__(self, model="llama3"): #phi3:mini
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt, temperature=0.0):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"]