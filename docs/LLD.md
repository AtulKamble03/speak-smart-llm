# Low Level Design (LLD)
## SpeakSmart — AI Communication Coach
**Version:** 1.0  
**Date:** 2026-05-29  
**Author:** AI Engineering Team

---

## 1. Project Structure

```
529Activity/
│
├── docs/
│   ├── HLD.md                  # High Level Design
│   ├── LLD.md                  # This document
│   └── SUMMARY.md              # Layman summary
│
├── src/
│   ├── app.py                  # Streamlit entry point
│   ├── analyzer.py             # LLM analysis logic
│   ├── historian.py            # SQLite history management
│   ├── scorer.py               # Score computation
│   └── ollama_client.py        # Ollama REST API wrapper
│
├── config/
│   └── settings.yaml           # All configuration values
│
├── data/
│   └── history.db              # SQLite database (auto-created)
│
├── requirements.txt
└── README.md
```

---

## 2. Configuration — `config/settings.yaml`

```yaml
ollama:
  base_url: "http://localhost:11434"
  default_model: "llama3"
  timeout_seconds: 60

app:
  title: "SpeakSmart — AI Communication Coach"
  port: 8501
  theme: "dark"
  max_history_display: 20

filler_words:
  - "uh"
  - "um"
  - "like"
  - "you know"
  - "basically"
  - "right"
  - "so"
  - "actually"
  - "literally"
  - "I mean"
  - "kind of"
  - "sort of"

scoring:
  weights:
    filler_penalty: 0.4    # 40% weight on filler word reduction
    grammar_penalty: 0.3   # 30% weight on grammar correctness
    clarity_bonus: 0.3     # 30% weight on clarity/structure
  max_score: 10
```

---

## 3. Module Design

---

### 3.1 `ollama_client.py`

**Purpose:** Abstracts all HTTP communication with the Ollama API.

```python
class OllamaClient:
    def __init__(self, base_url: str, model: str, timeout: int)
    def list_models(self) -> list[str]         # GET /api/tags
    def generate(self, prompt: str) -> str     # POST /api/generate (non-streaming)
    def is_available(self) -> bool             # Health check
```

**Ollama API Details:**
- List models: `GET http://localhost:11434/api/tags`
- Generate: `POST http://localhost:11434/api/generate`
  ```json
  {
    "model": "llama3",
    "prompt": "<prompt text>",
    "stream": false
  }
  ```
- Response field: `response.json()["response"]`

---

### 3.2 `analyzer.py`

**Purpose:** Builds structured prompts, sends to LLM, parses JSON response.

```python
class CommunicationAnalyzer:
    def __init__(self, client: OllamaClient)
    def analyze(self, text: str) -> AnalysisResult
    def _build_prompt(self, text: str) -> str
    def _parse_response(self, raw: str) -> AnalysisResult
```

**AnalysisResult dataclass:**
```python
@dataclass
class AnalysisResult:
    filler_words_found: list[str]        # e.g. ["uh", "um", "you know"]
    filler_word_count: int               # total count
    grammar_errors: list[GrammarError]  # list of errors with explanations
    rewritten_text: str                  # polished version
    suggestions: list[str]              # 2-3 improvement tips
    clarity_score: float                 # 0-10
    fluency_score: float                 # 0-10
    overall_score: float                 # 0-10
```

**GrammarError dataclass:**
```python
@dataclass
class GrammarError:
    original: str       # the problematic phrase
    correction: str     # corrected version
    explanation: str    # plain English explanation
```

**LLM Prompt Template:**
```
You are an expert communication coach. Analyze the following text and respond ONLY with valid JSON.

Text to analyze:
"""
{user_text}
"""

Respond with this exact JSON structure:
{
  "filler_words_found": ["list of filler words detected"],
  "filler_word_count": <integer>,
  "grammar_errors": [
    {"original": "...", "correction": "...", "explanation": "..."}
  ],
  "rewritten_text": "polished version of the text",
  "suggestions": ["tip 1", "tip 2", "tip 3"],
  "clarity_score": <0-10>,
  "fluency_score": <0-10>,
  "overall_score": <0-10>
}
```

---

### 3.3 `historian.py`

**Purpose:** Manages SQLite database for session history.

```python
class SessionHistorian:
    def __init__(self, db_path: str)
    def init_db(self)                                    # Create tables if not exist
    def save_session(self, result: AnalysisResult, raw_input: str) -> int
    def get_all_sessions(self) -> list[dict]
    def get_trend_data(self) -> dict                     # For charts
    def clear_history(self)
```

**Database Schema:**
```sql
CREATE TABLE sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_input       TEXT NOT NULL,
    filler_count    INTEGER,
    grammar_errors  INTEGER,
    clarity_score   REAL,
    fluency_score   REAL,
    overall_score   REAL,
    rewritten_text  TEXT,
    suggestions     TEXT,           -- JSON array stored as string
    filler_words    TEXT            -- JSON array stored as string
);
```

---

### 3.4 `scorer.py`

**Purpose:** Computes final composite score from LLM output.

```python
class CommunicationScorer:
    def __init__(self, config: dict)
    def compute_score(self, result: AnalysisResult, word_count: int) -> float
    def get_grade(self, score: float) -> str          # A/B/C/D/F
    def get_badge(self, score: float) -> str          # "Excellent" / "Good" / etc.
```

**Scoring Logic:**
```
filler_rate = filler_count / word_count
filler_score = max(0, 10 - (filler_rate * 100))

grammar_score = max(0, 10 - (grammar_error_count * 1.5))

final_score = (
    filler_score   * 0.4 +
    grammar_score  * 0.3 +
    clarity_score  * 0.3     # from LLM
)
```

**Grade Scale:**
| Score | Grade | Badge |
|---|---|---|
| 9.0 – 10 | A | Excellent |
| 7.5 – 8.9 | B | Good |
| 6.0 – 7.4 | C | Fair |
| 4.0 – 5.9 | D | Needs Work |
| 0 – 3.9 | F | Poor |

---

### 3.5 `app.py` — Streamlit UI

**Page Layout:**
```
┌──────────────────────────────────────────────────────┐
│  🎤 SpeakSmart — AI Communication Coach              │
│  [Model: llama3 ▼]                                   │
├──────────────────────────────────────────────────────┤
│  Paste your speech or text below:                    │
│  ┌────────────────────────────────────────────────┐  │
│  │  [Text Area — min 3 rows]                      │  │
│  └────────────────────────────────────────────────┘  │
│  [Analyze Communication]                              │
├──────────────────────────────────────────────────────┤
│  [Analysis] [Rewrite] [History] [Trends]             │
│                                                      │
│  ANALYSIS TAB:                                       │
│  Overall Score: 7.2 / 10  Grade: B  Badge: Good     │
│  ├── Filler Words: 5 found  [uh x2, um x1, like x2] │
│  ├── Grammar Errors: 2                               │
│  │     • "me and him went" → "he and I went"        │
│  └── Suggestions:                                    │
│        • Use pauses instead of filler words          │
│        • Practice slower, deliberate speech          │
└──────────────────────────────────────────────────────┘
```

**Tab: Analysis**
- Metric cards: Overall Score, Filler Count, Grammar Errors
- Highlighted filler words (with counts)
- Grammar error table (original → correction → explanation)
- Improvement suggestions as bullet list

**Tab: Rewrite**
- Side-by-side: Original text vs Rewritten text
- Copy-to-clipboard button

**Tab: History**
- Table of all past sessions (timestamp, score, filler count, grammar errors)
- Expandable rows to see full details

**Tab: Trends**
- Line chart: Overall Score over sessions
- Bar chart: Filler word count over sessions
- Both rendered with Plotly

---

## 4. Error Handling

| Scenario | Handling |
|---|---|
| Ollama not running | Show clear error: "Ollama is not running. Start it with: `ollama serve`" |
| No models installed | Show error: "No models found. Run: `ollama pull llama3`" |
| LLM returns invalid JSON | Retry once with stricter prompt; fallback to regex-based analysis |
| Empty input | Disable analyze button; show inline warning |
| DB error | Log to console; show toast notification to user |

---

## 5. Sequence Diagram — Analysis Flow

```
User          Streamlit         Analyzer        OllamaClient      SQLite
  │               │                │                 │               │
  │─[Input Text]─►│                │                 │               │
  │               │─[analyze(text)]►│                 │               │
  │               │                │─[generate(prompt)]►│             │
  │               │                │                 │─[POST /api]   │
  │               │                │                 │◄[JSON resp]   │
  │               │                │◄[AnalysisResult]│               │
  │               │                │                 │               │
  │               │◄[result]───────│                 │               │
  │               │─────────────────────────────────────[save_session]►│
  │               │                │                 │               │
  │◄[Display UI]──│                │                 │               │
```

---

## 6. Dependencies

```
streamlit>=1.35.0
requests>=2.31.0
plotly>=5.0.0
pyyaml>=6.0.0
```

All other dependencies (`sqlite3`, `json`, `re`, `dataclasses`) are Python built-ins.
