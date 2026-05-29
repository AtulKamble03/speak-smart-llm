# SpeakSmart — AI Communication Coach

A local AI-powered app that analyzes your speech or text for filler words, grammar errors, and communication quality — running 100% offline using Ollama.

---

## Prerequisites

1. **Python 3.10+** — [python.org](https://python.org)
2. **Ollama** — [ollama.com](https://ollama.com)

---

## Setup

### 1. Install Ollama and pull a model
```bash
# After installing Ollama, pull a model (choose one):
ollama pull llama3
ollama pull mistral
ollama pull phi3
```

### 2. Start Ollama
```bash
ollama serve
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run src/app.py
```

The app opens at **http://localhost:8501**

---

## Configuration

Edit [`config/settings.yaml`](config/settings.yaml) to:
- Change the default model
- Add/remove filler words
- Adjust scoring weights
- Change history display limit

---

## Features

| Feature | Description |
|---|---|
| Filler Word Detection | Counts and lists "uh", "um", "like", "you know", etc. |
| Grammar Check | Identifies errors with corrections and explanations |
| AI Rewrite | Clean, professional version of your text |
| Communication Score | 0–10 score with grade (A–F) |
| Session History | All past sessions saved to local SQLite |
| Trend Charts | Visual progress tracking over time |

---

## Project Structure

```
529Activity/
├── docs/               # Design documents
│   ├── HLD.md          # High Level Design
│   ├── LLD.md          # Low Level Design
│   ├── SUMMARY.md      # Layman summary
│   └── TASKS.md        # Task plan & progress
├── src/                # Application code
│   ├── app.py          # Streamlit UI (entry point)
│   ├── analyzer.py     # LLM analysis logic
│   ├── historian.py    # Session history (SQLite)
│   ├── scorer.py       # Scoring & grading
│   └── ollama_client.py # Ollama API wrapper
├── config/
│   └── settings.yaml   # All configuration
├── data/               # Auto-created on first run
│   └── history.db      # Session history database
└── requirements.txt
```

---

## Built With

- [Streamlit](https://streamlit.io) — UI framework
- [Ollama](https://ollama.com) — Local LLM runtime
- [Plotly](https://plotly.com) — Charts
- [SQLite](https://sqlite.org) — Local database
