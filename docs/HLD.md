# High Level Design (HLD)
## SpeakSmart — AI Communication Coach
**Version:** 1.0  
**Date:** 2026-05-29  
**Author:** AI Engineering Team

---

## 1. Overview

SpeakSmart is a local AI-powered communication coaching application. It analyzes user-provided speech or written text and provides real-time feedback on communication quality — including filler word detection, grammar correction, clarity scoring, and improvement suggestions. All processing runs entirely on a local LLM via Ollama, ensuring privacy and zero dependency on external APIs.

---

## 2. Goals and Objectives

| Goal | Description |
|---|---|
| Communication Improvement | Help users identify and reduce filler words over time |
| Grammar Awareness | Surface grammatical mistakes with explanations |
| AI-Powered Rewriting | Provide a polished, professional version of the input |
| Progress Tracking | Maintain session history and trend analysis |
| Offline / Private | 100% local — no data leaves the machine |

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     USER (Browser)                       │
│              Streamlit Web Interface                     │
└───────────────────────┬─────────────────────────────────┘
                        │  HTTP (localhost)
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  Python Application Layer                │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Analyzer   │  │  Historian   │  │   Scorer      │  │
│  │  Module     │  │  Module      │  │   Module      │  │
│  └──────┬──────┘  └──────┬───────┘  └──────┬────────┘  │
│         └────────────────┼──────────────────┘           │
│                          ▼                               │
│              ┌───────────────────────┐                  │
│              │   Ollama API Client   │                  │
│              └───────────┬───────────┘                  │
└──────────────────────────┼──────────────────────────────┘
                           │  REST API (localhost:11434)
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Ollama Runtime                        │
│              Local LLM (llama3 / mistral)               │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   SQLite Database                        │
│              Session History & Analytics                 │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Key Components

### 4.1 Frontend (Streamlit UI)
- Single-page web application running on `localhost:8501`
- Input area for user text/speech transcript
- Results panel with tabs: Analysis | Rewrite | History | Trends
- Model selector dropdown (auto-detects installed Ollama models)

### 4.2 Application Layer (Python)
| Module | Responsibility |
|---|---|
| `analyzer.py` | Sends text to LLM, parses structured response (filler words, grammar, score) |
| `historian.py` | Reads/writes session history to SQLite |
| `scorer.py` | Computes communication score from LLM output |
| `ollama_client.py` | Wraps Ollama REST API calls |
| `app.py` | Streamlit entry point, wires all modules |

### 4.3 Local LLM (Ollama)
- Runs on `localhost:11434`
- Supports any model installed via `ollama pull`
- Receives structured prompts, returns JSON-formatted analysis

### 4.4 Database (SQLite)
- File: `data/history.db`
- Stores: session ID, timestamp, raw input, filler word count, grammar errors, score, rewritten text

---

## 5. Data Flow

```
User Input Text
      │
      ▼
Filler Word Pre-scan (local regex)
      │
      ▼
LLM Analysis Request (structured prompt)
      │
      ▼
LLM Response (JSON: filler_words, grammar_errors, score, rewrite, suggestions)
      │
      ├──► Display Results in UI
      │
      └──► Save to SQLite History
                  │
                  ▼
           Trend Charts (Plotly)
```

---

## 6. Non-Functional Requirements

| Requirement | Target |
|---|---|
| Response Time | < 10 seconds for analysis (model dependent) |
| Privacy | All processing on local machine — no external calls |
| Portability | Runs on Windows / Mac / Linux |
| Model Agnostic | Works with any Ollama-compatible model |
| Persistence | History survives app restarts |

---

## 7. Technology Stack

| Layer | Technology | Version |
|---|---|---|
| UI Framework | Streamlit | ≥ 1.35 |
| Language | Python | ≥ 3.10 |
| Local LLM Runtime | Ollama | Latest |
| Database | SQLite (via sqlite3) | Built-in |
| Charts | Plotly | ≥ 5.0 |
| HTTP Client | requests | ≥ 2.31 |
| Config | PyYAML | ≥ 6.0 |

---

## 8. Deployment View

- All components run on a single developer machine
- No cloud dependencies
- Single command to launch: `streamlit run src/app.py`
- Prerequisites: Python 3.10+, Ollama installed and running

---

## 9. Out of Scope (v1.0)

- Real-time speech-to-text (microphone input)
- Multi-user support
- Cloud deployment
- Mobile interface
