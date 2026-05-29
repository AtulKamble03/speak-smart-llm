import sys
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
import yaml

sys.path.insert(0, str(Path(__file__).parent))

from ollama_client import OllamaClient
from analyzer import CommunicationAnalyzer
from historian import SessionHistorian
from scorer import CommunicationScorer

MIC_HTML = """
<style>
#mic-btn {
    background: #2ecc71; color: white; border: none;
    padding: 12px 24px; border-radius: 8px; font-size: 15px;
    cursor: pointer; width: 100%; margin-bottom: 6px;
    transition: background 0.2s;
}
#mic-btn.recording { background: #e74c3c; }
#mic-status { color: #a6adc8; font-size: 13px; text-align: center; }
</style>

<button id="mic-btn" onclick="toggleRecording()">🎤 Click to Speak</button>
<div id="mic-status">Click the button and speak. It will stop automatically.</div>

<script>
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (!SpeechRecognition) {
    document.getElementById('mic-status').innerText = '❌ Browser does not support speech recognition. Use Chrome or Edge.';
    document.getElementById('mic-btn').disabled = true;
}

let recognition;
let isRecording = false;

function toggleRecording() {
    if (!isRecording) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = function() {
            isRecording = true;
            document.getElementById('mic-btn').innerHTML = '⏹ Stop Recording';
            document.getElementById('mic-btn').classList.add('recording');
            document.getElementById('mic-status').innerText = '🔴 Listening... speak now.';
        };

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('mic-status').innerText = '✅ Transcribed: "' + transcript + '"';
            setStreamlitTextarea(transcript);
        };

        recognition.onerror = function(e) {
            document.getElementById('mic-status').innerText = '❌ Error: ' + e.error;
        };

        recognition.onend = function() {
            isRecording = false;
            document.getElementById('mic-btn').innerHTML = '🎤 Click to Speak';
            document.getElementById('mic-btn').classList.remove('recording');
        };

        recognition.start();
    } else {
        recognition.stop();
    }
}

function setStreamlitTextarea(text) {
    const doc = window.parent.document;
    const textareas = doc.querySelectorAll('textarea');
    if (textareas.length > 0) {
        const ta = textareas[0];
        const setter = Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(ta, text);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
    }
}
</script>
"""


# ── Config ────────────────────────────────────────────────────────────────────

CONFIG_PATH = Path(__file__).parent.parent / "config" / "settings.yaml"

@st.cache_resource
def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

@st.cache_resource
def get_historian(db_path: str) -> SessionHistorian:
    return SessionHistorian(db_path)


# ── Page setup ────────────────────────────────────────────────────────────────

config = load_config()

st.set_page_config(
    page_title=config["app"]["title"],
    page_icon="🎤",
    layout="wide",
)

st.markdown("""
<style>
    .metric-card {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #313244;
    }
    .metric-value { font-size: 2.5rem; font-weight: 700; }
    .metric-label { font-size: 0.85rem; color: #a6adc8; margin-top: 4px; }
    .badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 6px;
    }
    .filler-tag {
        display: inline-block;
        background: #45475a;
        color: #cdd6f4;
        border-radius: 6px;
        padding: 3px 10px;
        margin: 3px;
        font-size: 0.85rem;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #cdd6f4;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("🎤 SpeakSmart")
    st.caption("AI Communication Coach — 100% Local")
    st.divider()

    ollama_url = config["ollama"]["base_url"]
    client_check = OllamaClient(ollama_url, config["ollama"]["default_model"])

    if not client_check.is_available():
        st.error("Ollama is not running.\n\nStart it with:\n```\nollama serve\n```")
        st.stop()

    available_models = client_check.list_models()
    if not available_models:
        st.error("No models found.\n\nInstall one:\n```\nollama pull llama3\n```")
        st.stop()

    default_model = config["ollama"]["default_model"]
    default_idx = available_models.index(default_model) if default_model in available_models else 0

    selected_model = st.selectbox("Model", available_models, index=default_idx)
    st.success(f"Connected to Ollama")

    st.divider()
    st.caption("Session")
    historian = get_historian(config["database"]["path"])
    sessions = historian.get_all_sessions()
    st.metric("Total Sessions", len(sessions))
    if sessions:
        avg_score = sum(s["overall_score"] for s in sessions) / len(sessions)
        st.metric("Avg Score", f"{avg_score:.1f} / 10")

    st.divider()
    if st.button("🗑 Clear History", use_container_width=True):
        historian.clear_history()
        st.rerun()


# ── Main area ─────────────────────────────────────────────────────────────────

st.title("🎤 SpeakSmart — AI Communication Coach")
st.caption("Paste your speech or written text below, or use the microphone to speak directly.")

# ── Voice Input ───────────────────────────────────────────────────────────────

st.markdown("**Speak your text** *(Chrome/Edge only)*")
st.components.v1.html(MIC_HTML, height=80)
st.markdown("**Or type / paste your text:**")

prefill = ""

text_input = st.text_area(
    "Your text",
    value=prefill,
    placeholder='Example: "So, uh, basically what I wanted to say is, you know, we should, like, improve our communication skills..."',
    height=160,
    label_visibility="collapsed",
)

col_btn, col_info = st.columns([2, 5])
with col_btn:
    analyze_clicked = st.button(
        "Analyze Communication",
        type="primary",
        use_container_width=True,
        disabled=len(text_input.strip()) < 10,
    )
with col_info:
    if text_input.strip():
        word_count = len(text_input.split())
        st.caption(f"{word_count} words · {len(text_input)} characters")

st.divider()

tab_analysis, tab_rewrite, tab_history, tab_trends = st.tabs(
    ["📊 Analysis", "✏️ Rewrite", "📋 History", "📈 Trends"]
)


# ── Analysis ──────────────────────────────────────────────────────────────────

if analyze_clicked and text_input.strip():
    client = OllamaClient(
        ollama_url,
        selected_model,
        timeout=config["ollama"]["timeout_seconds"],
    )
    scorer = CommunicationScorer(
        config["scoring"]["weights"],
        config["scoring"]["max_score"],
    )
    analyzer = CommunicationAnalyzer(client)

    with st.spinner("Analyzing your communication..."):
        result = analyzer.analyze(text_input)

    word_count = len(text_input.split())
    computed_score = scorer.compute_score(result, word_count)
    result.overall_score = computed_score
    grade, badge, badge_color = scorer.get_grade(computed_score)

    historian.save_session(result)
    st.session_state["last_result"] = result
    st.session_state["last_grade"] = (grade, badge, badge_color)
    st.session_state["last_word_count"] = word_count


result = st.session_state.get("last_result")
grade_info = st.session_state.get("last_grade", ("—", "—", "#45475a"))
word_count = st.session_state.get("last_word_count", 0)

with tab_analysis:
    if result is None:
        st.info("Paste some text above and click **Analyze Communication** to get started.")
    else:
        grade, badge, badge_color = grade_info

        # Score cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:{badge_color}">{result.overall_score}</div>
                <div class="metric-label">Overall Score / 10</div>
                <span class="badge" style="background:{badge_color}22; color:{badge_color}">{grade} — {badge}</span>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:#f38ba8">{result.filler_word_count}</div>
                <div class="metric-label">Filler Words</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:#fab387">{len(result.grammar_errors)}</div>
                <div class="metric-label">Grammar Errors</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:#a6e3a1">{result.clarity_score:.1f}</div>
                <div class="metric-label">Clarity Score / 10</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown('<div class="section-header">🔴 Filler Words Found</div>', unsafe_allow_html=True)
            if result.filler_words_found:
                from collections import Counter
                counts = Counter(w.lower() for w in result.filler_words_found)
                tags = " ".join(
                    f'<span class="filler-tag">{word} ×{cnt}</span>'
                    for word, cnt in counts.most_common()
                )
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.success("No filler words detected!")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">💡 Improvement Tips</div>', unsafe_allow_html=True)
            for tip in result.suggestions:
                st.markdown(f"- {tip}")

        with col_right:
            st.markdown('<div class="section-header">🟡 Grammar Errors</div>', unsafe_allow_html=True)
            if result.grammar_errors:
                for err in result.grammar_errors:
                    with st.expander(f"❌ \"{err.original}\""):
                        st.markdown(f"**Correction:** {err.correction}")
                        st.markdown(f"**Why:** {err.explanation}")
            else:
                st.success("No grammar errors detected!")


# ── Rewrite ───────────────────────────────────────────────────────────────────

with tab_rewrite:
    if result is None:
        st.info("Run an analysis first to see the rewritten version.")
    else:
        col_orig, col_new = st.columns(2)
        with col_orig:
            st.markdown("#### Original Text")
            st.markdown(f'<div style="background:#1e1e2e; padding:16px; border-radius:8px; border:1px solid #313244; min-height:150px">{result.raw_input}</div>', unsafe_allow_html=True)
        with col_new:
            st.markdown("#### Rewritten by AI")
            st.markdown(f'<div style="background:#1e2e1e; padding:16px; border-radius:8px; border:1px solid #2a4a2a; min-height:150px">{result.rewritten_text}</div>', unsafe_allow_html=True)
            st.code(result.rewritten_text, language=None)


# ── History ───────────────────────────────────────────────────────────────────

with tab_history:
    sessions = historian.get_all_sessions()
    if not sessions:
        st.info("No sessions yet. Analyze some text to build your history.")
    else:
        st.caption(f"{len(sessions)} session(s) recorded")
        for s in sessions[:config["app"]["max_history_display"]]:
            _, badge, color = CommunicationScorer(
                config["scoring"]["weights"]
            ).get_grade(s["overall_score"])
            with st.expander(
                f"🕐 {s['timestamp']}  |  Score: {s['overall_score']}/10  |  Fillers: {s['filler_count']}  |  Grammar: {s['grammar_errors']}"
            ):
                st.markdown(f"**Input:** {s['raw_input'][:300]}{'...' if len(s['raw_input']) > 300 else ''}")
                if s["suggestions"]:
                    st.markdown("**Tips given:**")
                    for tip in s["suggestions"]:
                        st.markdown(f"- {tip}")


# ── Trends ────────────────────────────────────────────────────────────────────

with tab_trends:
    trend = historian.get_trend_data()
    if len(trend["timestamps"]) < 2:
        st.info("Complete at least 2 sessions to see trends.")
    else:
        labels = [f"Session {i+1}" for i in range(len(trend["timestamps"]))]

        fig_score = go.Figure()
        fig_score.add_trace(go.Scatter(
            x=labels, y=trend["scores"],
            mode="lines+markers",
            line=dict(color="#89b4fa", width=2),
            marker=dict(size=8),
            name="Overall Score",
        ))
        fig_score.update_layout(
            title="Overall Score Over Time",
            yaxis=dict(range=[0, 10]),
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
            font=dict(color="#cdd6f4"),
        )
        st.plotly_chart(fig_score, use_container_width=True)

        fig_filler = go.Figure()
        fig_filler.add_trace(go.Bar(
            x=labels, y=trend["filler_counts"],
            marker_color="#f38ba8",
            name="Filler Words",
        ))
        fig_filler.update_layout(
            title="Filler Word Count Over Time",
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
            font=dict(color="#cdd6f4"),
        )
        st.plotly_chart(fig_filler, use_container_width=True)
