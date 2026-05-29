# SpeakSmart — Runbook
### How to Start, Use, and Stop the Application
**Last Updated:** 2026-05-29

---

## Prerequisites (One-Time Setup)

Before running the app for the first time, ensure these are installed:

| Tool | Purpose | Check if installed |
|---|---|---|
| Python 3.10+ | Runs the application | `python --version` |
| Ollama | Runs the local AI model | `ollama --version` |
| llama3 model | The AI brain | `ollama list` |
| Python dependencies | App libraries | Already installed |

---

## How to START the App

### Step 1 — Start Ollama (AI Engine)
Open a terminal and run:

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve
```

> Keep this terminal open. Ollama runs silently in the background.  
> You should see: `Listening on 127.0.0.1:11434`

---

### Step 2 — Start the App
Open a **second terminal** and run:

```powershell
python -m streamlit run "c:\Personal Workspace\AI\529Activity\src\app.py"
```

> Press **Enter** to skip the email prompt if it appears.

---

### Step 3 — Open in Browser
Go to:
```
http://localhost:8501
```

The SpeakSmart app will open in your browser. You're ready to go!

---

## How to USE the App

1. **Paste** your speech or text in the input box
2. Click **Analyze Communication**
3. Wait ~30–60 seconds (first run loads the AI model into memory)
4. Subsequent analyses are faster (~10–15 seconds)

### Tabs explained:
| Tab | What it shows |
|---|---|
| Analysis | Score, filler words, grammar errors, improvement tips |
| Rewrite | AI-polished version of your text |
| History | All past sessions |
| Trends | Charts showing your progress over time |

---

## How to STOP the App

### Stop Streamlit (App UI)
In the terminal where Streamlit is running:
```
Press Ctrl + C
```

### Stop Ollama (AI Engine)
In the terminal where Ollama is running:
```
Press Ctrl + C
```

Or kill it via PowerShell:
```powershell
Stop-Process -Name "ollama" -Force
```

---

## Quick Reference — Key Files

| File | Purpose |
|---|---|
| `src/app.py` | **Main entry point** — this is what you run |
| `src/analyzer.py` | Sends text to LLM, parses response |
| `src/historian.py` | Saves/reads session history |
| `src/scorer.py` | Calculates communication score |
| `src/ollama_client.py` | Talks to Ollama API |
| `config/settings.yaml` | All settings (model, timeout, filler words) |
| `data/history.db` | Your session history (auto-created) |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Connection refused` on app open | Ollama is not running — do Step 1 first |
| `ReadTimeout` error | Analysis took too long — try shorter text or wait |
| `No models found` in sidebar | Run: `ollama pull llama3` |
| App not opening in browser | Go manually to `http://localhost:8501` |
| Streamlit email prompt stuck | Press **Enter** to skip |
| Want to change AI model | Edit `config/settings.yaml` → `default_model` |

---

## Changing the AI Model

Edit `config/settings.yaml`:
```yaml
ollama:
  default_model: "llama3"   # change to: mistral, phi3, gemma, etc.
```

To pull a different model:
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull mistral
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull phi3
```

---

## Full Startup in One Go (Copy-Paste)

Open **two separate terminals** and run one command in each:

**Terminal 1:**
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve
```

**Terminal 2:**
```powershell
python -m streamlit run "c:\Personal Workspace\AI\529Activity\src\app.py"
```

Then open **http://localhost:8501**
