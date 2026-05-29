import requests


class OllamaClient:
    def __init__(self, base_url: str, model: str, timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def is_available(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return r.status_code == 200
        except Exception:
            return False

    def list_models(self) -> list[str]:
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=10)
            r.raise_for_status()
            models = r.json().get("models", [])
            return [m["name"] for m in models]
        except Exception:
            return []

    def generate(self, prompt: str) -> str:
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        r = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json().get("response", "")
