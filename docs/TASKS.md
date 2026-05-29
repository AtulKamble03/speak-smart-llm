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

## Phase 5 — Testing & Validation
| # | Task | Status | Notes |
|---|---|---|---|
| 5.1 | Verify Ollama connectivity | ⬜ Pending | Health check on launch |
| 5.2 | Test analysis with sample text | ⬜ Pending | End-to-end run |
| 5.3 | Test history persistence | ⬜ Pending | Save and reload sessions |
| 5.4 | Test trend charts rendering | ⬜ Pending | Plotly charts display correctly |

---

## Decisions Log
| Date | Decision | Reason |
|---|---|---|
| 2026-05-29 | Chose Streamlit over WPF/Flask | Fastest to build, great demo UI, cross-platform |
| 2026-05-29 | Chose Ollama as LLM runtime | Most popular local LLM tool, simple REST API, no API key needed |
| 2026-05-29 | Chose SQLite for history | Built into Python, zero setup, file-based and portable |
| 2026-05-29 | App theme: Communication Coach | Unique, practical, impressive demo — not just another chatbot |

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
│   └── app.py           ✅ Streamlit UI — complete
├── config/
│   └── settings.yaml    ✅ All configuration
├── data/
│   └── history.db       ⬜ Auto-created on first run
├── requirements.txt     ✅ Done
└── README.md            ✅ Done
```
