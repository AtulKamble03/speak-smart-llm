# SpeakSmart — Project Summary
### Written in Plain English (No Tech Jargon)
**Date:** 2026-05-29

---

## What is SpeakSmart?

SpeakSmart is an AI-powered app that acts like a **personal communication coach** — but it runs completely on your own computer without needing the internet.

You type or paste something you said (like a speech, a presentation, a meeting message, or even a casual conversation), and the app tells you:
- How many filler words you used (like "uh", "um", "you know", "basically")
- What grammar mistakes you made — and how to fix them
- A better, cleaner version of what you said
- A score out of 10 for how well you communicated
- Tips to improve next time

And it remembers all your past sessions, so you can see if you're getting better over time!

---

## Why Did We Build This?

Many of us use filler words without even realizing it. In interviews, presentations, or meetings, too many "uh"s and "um"s can make us sound less confident and unclear.

Most tools that fix this require an internet connection and send your data to a server somewhere. **SpeakSmart is different — everything stays on your computer.** Your words, your data, your privacy.

---

## How Does It Work? (Simple Version)

Think of it like this:

```
You type something
        ↓
The app sends it to an AI running on your computer
        ↓
The AI reads it like a coach and writes back a detailed report
        ↓
The app shows you the report in a nice, easy-to-read layout
        ↓
Your session is saved so you can track your progress
```

The "AI running on your computer" is called **Ollama** — it's a free tool that lets you run powerful AI models (like the ones behind ChatGPT) completely offline on your own machine.

---

## What Will You See in the App?

The app has 4 sections (tabs):

### 1. Analysis Tab
This is the main report. You'll see:
- Your **overall communication score** (e.g., 7.2 / 10 — Grade B — "Good")
- A list of **filler words** found and how many times you used each one
- **Grammar mistakes** — shown as: what you said → what you should have said → why
- **3 improvement tips** written by the AI just for your text

### 2. Rewrite Tab
The AI rewrites your text as if a professional communications coach cleaned it up — no filler words, correct grammar, clear and confident. You can copy it and use it!

### 3. History Tab
Every time you analyze something, it gets saved. This tab shows a table of all your past sessions — date, score, filler count, errors — so you can look back.

### 4. Trends Tab
Charts! You can visually see:
- Is your score going up over time?
- Is your filler word count going down?

These charts make it easy to see your progress at a glance.

---

## Who is This For?

- **Professionals** preparing for interviews or presentations
- **Students** working on public speaking skills
- **Anyone** who wants to communicate more clearly and confidently
- **Teams** who want to improve meeting communication quality

---

## What Do You Need to Run It?

Just two things:
1. **Python** installed on your computer (free, takes 2 minutes)
2. **Ollama** installed and running (free, takes 5 minutes — just download and run one command)

Then run one command:
```
streamlit run src/app.py
```

And the app opens in your browser. That's it!

---

## Key Facts at a Glance

| What | Detail |
|---|---|
| App Name | SpeakSmart |
| What it does | Analyzes your communication and helps you improve |
| Internet needed? | No — runs 100% offline |
| Data privacy | Your text never leaves your computer |
| Where it runs | In your web browser (on your local computer) |
| How to start | One command in the terminal |
| Cost | Free (uses open-source AI tools) |

---

## Folder Overview (What's in the Project)

```
529Activity/
├── docs/           ← Design documents (HLD, LLD, this summary)
├── src/            ← The actual application code
├── config/         ← Settings and configuration
├── data/           ← Where your history is saved (auto-created)
├── requirements.txt ← List of tools needed to run the app
└── README.md       ← Quick start guide
```

---

## In One Sentence

> SpeakSmart listens to what you say, tells you what's wrong, shows you how to say it better, and tracks your improvement — all using AI that runs privately on your own computer.
