# SpeakSmart — Project Task Plan
**Last Updated:** 2026-05-29  
**Status Legend:** ✅ Done | 🔄 In Progress | ⬜ Pending | ❌ Blocked

---

## Phase 1 — Documentation
| # | Task | Status | Notes |
|---|---|---|---|
| 1.1 | High Level Design (HLD) | ✅ Done | `docs/HLD.md` |
| 1.2 | Low Level Design (LLD) | ✅ Done | `docs/LLD.md` |
| 1.3 | Layman Summary Document | ✅ Done | `docs/SUMMARY.md` |
| 1.4 | Project Task Plan (this file) | ✅ Done | `docs/TASKS.md` |

---

## Phase 2 — Configuration
| # | Task | Status | Notes |
|---|---|---|---|
| 2.1 | Create `config/settings.yaml` | ✅ Done | Ollama URL, model, filler words, scoring weights |
| 2.2 | Create folder structure | ✅ Done | `src/`, `docs/`, `config/`, `data/` |

---

## Phase 3 — Implementation
| # | Task | Status | Notes |
|---|---|---|---|
| 3.1 | `src/ollama_client.py` — Ollama API wrapper | ✅ Done | list models, generate, health check |
| 3.2 | `src/analyzer.py` — LLM analysis + response parsing | ✅ Done | prompt template, JSON parsing, dataclasses |
| 3.3 | `src/historian.py` — SQLite session history | ✅ Done | save, read, trend data, clear |
| 3.4 | `src/scorer.py` — Communication scoring logic | ✅ Done | grade scale, badge colors, weighted score |
| 3.5 | `src/app.py` — Streamlit UI (main app) | ✅ Done | 4 tabs: Analysis, Rewrite, History, Trends |

---

## Phase 4 — Project Setup
| # | Task | Status | Notes |
|---|---|---|---|
| 4.1 | `requirements.txt` | ✅ Done | streamlit, requests, plotly, pyyaml |
| 4.2 | `README.md` | ✅ Done | Quick start guide with setup steps |

---

## Phase 5 — Environment Setup & Testing
| # | Task | Status | Notes |
|---|---|---|---|
| 5.1 | Install Ollama (v0.24.0) | ✅ Done | Installed via winget |
| 5.2 | Pull LLM model (llama3) | ✅ Done | 4.7 GB — llama3:latest ready |
| 5.3 | Install Python dependencies | ✅ Done | All packages installed |
| 5.4 | Verify Ollama connectivity | ✅ Done | API responding on localhost:11434 |
| 5.5 | Launch Streamlit app | ✅ Done | Running on localhost:8501 |
| 5.6 | Fix timeout (60s → 300s) | ✅ Done | config/settings.yaml updated |
| 5.7 | Add voice mic button | ✅ Done | Web Speech API (Chrome/Edge) |
| 5.8 | Add RUNBOOK.md | ✅ Done | Start/stop/troubleshoot guide |
| 5.9 | Test analysis end-to-end | 🔄 In Progress | Testing with sample prompts |
| 5.10 | Test history & trends tabs | ⬜ Pending | After successful analysis |

---

## Decisions Log
| Date | Decision | Reason |
|---|---|---|
| 2026-05-29 | Chose Streamlit over WPF/Flask | Fastest to build, great demo UI, cross-platform — timed activity |
| 2026-05-29 | Chose Ollama as LLM runtime | Most popular local LLM tool, simple REST API, no API key needed |
| 2026-05-29 | Chose SQLite for history | Built into Python, zero setup, file-based and portable |
| 2026-05-29 | App theme: Communication Coach | Unique, practical, impressive demo — not just another chatbot |
| 2026-05-29 | C# WPF version deferred | Build C# version only after Python version is fully functional and validated |

---

## File Map
```
529Activity/
├── docs/
│   ├── HLD.md          ✅ High Level Design
│   ├── LLD.md          ✅ Low Level Design
│   ├── SUMMARY.md      ✅ Layman Summary
│   └── TASKS.md        ✅ This file — Task Plan
├── src/
│   ├── ollama_client.py ✅ Ollama API wrapper
│   ├── analyzer.py      ✅ LLM analysis logic
│   ├── historian.py     ✅ SQLite history
│   ├── scorer.py        ✅ Scoring logic
│   └── app.py           ✅ Streamlit UI + mic button (Web Speech API)
├── config/
│   └── settings.yaml    ✅ All configuration
├── data/
│   └── history.db       ⬜ Auto-created on first run
├── requirements.txt     ✅ Done
└── README.md            ✅ Done

---

## Phase 6 — C# WPF Version (Deferred)
> Start this phase ONLY after Phase 5 is fully complete and the Python app is validated.

| # | Task | Status | Notes |
|---|---|---|---|
| 6.1 | Create WPF project structure | ⬜ Deferred | .NET 8, WPF |
| 6.2 | Ollama HTTP client in C# | ⬜ Deferred | `HttpClient` + `System.Text.Json` |
| 6.3 | Analysis & scoring logic in C# | ⬜ Deferred | Port from `analyzer.py`, `scorer.py` |
| 6.4 | SQLite history (Dapper) | ⬜ Deferred | Same schema as Python version |
| 6.5 | WPF UI — Analysis, Rewrite, History, Trends | ⬜ Deferred | MaterialDesignThemes + LiveCharts2 |
| 6.6 | Test & validate C# version | ⬜ Deferred | Feature parity with Python version |
```
