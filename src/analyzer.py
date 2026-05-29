import json
import re
from dataclasses import dataclass, field

from ollama_client import OllamaClient


@dataclass
class GrammarError:
    original: str
    correction: str
    explanation: str


@dataclass
class AnalysisResult:
    filler_words_found: list[str] = field(default_factory=list)
    filler_word_count: int = 0
    grammar_errors: list[GrammarError] = field(default_factory=list)
    rewritten_text: str = ""
    suggestions: list[str] = field(default_factory=list)
    clarity_score: float = 0.0
    fluency_score: float = 0.0
    overall_score: float = 0.0
    raw_input: str = ""


PROMPT_TEMPLATE = """You are an expert communication coach. Analyze the following text for filler words, grammar errors, and overall communication quality.

Text to analyze:
\"\"\"
{text}
\"\"\"

Respond ONLY with valid JSON — no explanation, no markdown, no code blocks. Use this exact structure:
{{
  "filler_words_found": ["list each filler word instance found, e.g. uh, um, like"],
  "filler_word_count": <integer total count>,
  "grammar_errors": [
    {{"original": "the problematic phrase", "correction": "corrected version", "explanation": "why it is wrong"}}
  ],
  "rewritten_text": "a polished, professional rewrite of the original text with no filler words and correct grammar",
  "suggestions": ["specific tip 1", "specific tip 2", "specific tip 3"],
  "clarity_score": <number 0 to 10>,
  "fluency_score": <number 0 to 10>,
  "overall_score": <number 0 to 10>
}}"""


class CommunicationAnalyzer:
    def __init__(self, client: OllamaClient):
        self.client = client

    def analyze(self, text: str) -> AnalysisResult:
        prompt = PROMPT_TEMPLATE.format(text=text)
        raw_response = self.client.generate(prompt)
        result = self._parse_response(raw_response)
        result.raw_input = text
        return result

    def _parse_response(self, raw: str) -> AnalysisResult:
        json_str = self._extract_json(raw)
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            return AnalysisResult(
                suggestions=["Could not parse AI response. Try again."],
                rewritten_text=raw,
            )

        grammar_errors = [
            GrammarError(
                original=e.get("original", ""),
                correction=e.get("correction", ""),
                explanation=e.get("explanation", ""),
            )
            for e in data.get("grammar_errors", [])
        ]

        return AnalysisResult(
            filler_words_found=data.get("filler_words_found", []),
            filler_word_count=int(data.get("filler_word_count", 0)),
            grammar_errors=grammar_errors,
            rewritten_text=data.get("rewritten_text", ""),
            suggestions=data.get("suggestions", []),
            clarity_score=float(data.get("clarity_score", 0)),
            fluency_score=float(data.get("fluency_score", 0)),
            overall_score=float(data.get("overall_score", 0)),
        )

    def _extract_json(self, text: str) -> str:
        # Strip markdown code fences if present
        text = re.sub(r"```(?:json)?", "", text).strip()
        # Find the first { ... } block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return match.group(0) if match else text
