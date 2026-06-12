import streamlit as st
import os
import time
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchForge AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS — deep-space 3D aesthetic ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #020510 !important;
    font-family: 'Space Grotesk', sans-serif;
    color: #e2e8f0;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% 20%, rgba(99,102,241,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(16,185,129,0.08) 0%, transparent 60%),
        #020510 !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 2rem 3rem !important; max-width: 1200px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0f1e; }
::-webkit-scrollbar-thumb { background: #3730a3; border-radius: 3px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 600px; height: 200px;
    background: radial-gradient(ellipse, rgba(99,102,241,0.18) 0%, transparent 70%);
    pointer-events: none;
    filter: blur(20px);
}
.hero-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #818cf8;
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 100px;
    padding: 0.3rem 1rem;
    margin-bottom: 1.2rem;
    background: rgba(99,102,241,0.08);
}
.hero h1 {
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 700;
    line-height: 1.1;
    margin: 0 0 1rem;
    background: linear-gradient(135deg, #fff 0%, #a5b4fc 50%, #6ee7b7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    color: #94a3b8;
    font-size: 1.05rem;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── 3D Glass card ── */
.glass-card {
    background: linear-gradient(145deg,
        rgba(255,255,255,0.06) 0%,
        rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 4px 6px rgba(0,0,0,0.4),
        0 1px 0 rgba(255,255,255,0.06) inset,
        0 -1px 0 rgba(0,0,0,0.3) inset;
    transform: perspective(1000px) rotateX(0deg);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg,
        transparent, rgba(255,255,255,0.15), transparent);
}
.glass-card:hover {
    box-shadow:
        0 8px 32px rgba(99,102,241,0.15),
        0 1px 0 rgba(255,255,255,0.1) inset,
        0 -1px 0 rgba(0,0,0,0.3) inset;
    transform: perspective(1000px) translateY(-2px);
}

/* ── Step cards ── */
.step-card {
    background: linear-gradient(145deg,
        rgba(255,255,255,0.05) 0%,
        rgba(255,255,255,0.01) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    box-shadow:
        0 2px 8px rgba(0,0,0,0.3),
        0 1px 0 rgba(255,255,255,0.05) inset;
    transition: all 0.3s ease;
}
.step-card.active {
    border-color: rgba(99,102,241,0.5);
    background: linear-gradient(145deg,
        rgba(99,102,241,0.12) 0%,
        rgba(99,102,241,0.04) 100%);
    box-shadow:
        0 0 30px rgba(99,102,241,0.2),
        0 4px 16px rgba(0,0,0,0.3),
        0 1px 0 rgba(255,255,255,0.1) inset;
}
.step-card.done {
    border-color: rgba(16,185,129,0.4);
    background: linear-gradient(145deg,
        rgba(16,185,129,0.08) 0%,
        rgba(16,185,129,0.02) 100%);
    box-shadow: 0 0 20px rgba(16,185,129,0.1);
}
.step-card.error {
    border-color: rgba(239,68,68,0.4);
    background: linear-gradient(145deg,
        rgba(239,68,68,0.08) 0%,
        rgba(239,68,68,0.02) 100%);
}
.step-header {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin-bottom: 0.5rem;
}
.step-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    box-shadow: 0 2px 8px rgba(99,102,241,0.2), 0 0 0 1px rgba(99,102,241,0.1);
}
.step-icon.done {
    background: rgba(16,185,129,0.15);
    border-color: rgba(16,185,129,0.4);
    box-shadow: 0 2px 8px rgba(16,185,129,0.2);
}
.step-icon.error {
    background: rgba(239,68,68,0.15);
    border-color: rgba(239,68,68,0.4);
    box-shadow: 0 2px 8px rgba(239,68,68,0.2);
}
.step-title {
    font-weight: 600;
    font-size: 0.92rem;
    letter-spacing: 0.02em;
    color: #e2e8f0;
}
.step-subtitle {
    font-size: 0.78rem;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
}
.step-content {
    background: rgba(0,0,0,0.25);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
    font-size: 0.84rem;
    line-height: 1.7;
    color: #cbd5e1;
    font-family: 'JetBrains Mono', monospace;
    max-height: 280px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.2rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3), 0 1px 0 rgba(255,255,255,0.05) inset !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow:
        0 0 0 3px rgba(99,102,241,0.12),
        0 2px 8px rgba(0,0,0,0.3) !important;
    background: rgba(99,102,241,0.06) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: #475569 !important; }
label[data-testid="stWidgetLabel"] p {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    margin-bottom: 0.4rem !important;
}

/* ── Launch button ── */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #0ea5e9 100%) !important;
    color: white !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.8rem 2.5rem !important;
    cursor: pointer !important;
    width: 100% !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow:
        0 4px 20px rgba(79,70,229,0.4),
        0 1px 0 rgba(255,255,255,0.15) inset !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow:
        0 8px 32px rgba(79,70,229,0.5),
        0 1px 0 rgba(255,255,255,0.2) inset !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Metric pills ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.metric-pill {
    flex: 1;
    min-width: 120px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3), 0 1px 0 rgba(255,255,255,0.05) inset;
    transition: all 0.3s ease;
}
.metric-pill:hover {
    border-color: rgba(99,102,241,0.3);
    transform: translateY(-2px);
}
.metric-value {
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a5b4fc, #6ee7b7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label {
    font-size: 0.72rem;
    color: #64748b;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}

/* ── Progress bar ── */
.progress-wrap {
    background: rgba(255,255,255,0.05);
    border-radius: 100px;
    height: 4px;
    margin: 1.2rem 0;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.05);
}
.progress-bar {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #4f46e5, #7c3aed, #0ea5e9);
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 0 12px rgba(99,102,241,0.6);
}

/* ── Status tags ── */
.status-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
    padding: 0.25rem 0.7rem;
    border-radius: 100px;
    font-weight: 500;
}
.status-tag.running {
    color: #a5b4fc; background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.3);
}
.status-tag.done {
    color: #6ee7b7; background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
}
.status-tag.error {
    color: #fca5a5; background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
}
.status-tag.idle {
    color: #64748b; background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
}

/* ── Divider ── */
.neon-divider {
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%, rgba(99,102,241,0.4) 30%,
        rgba(16,185,129,0.4) 70%, transparent 100%);
    margin: 2rem 0;
    border: none;
}

/* ── Report output ── */
.report-box {
    background: linear-gradient(145deg,
        rgba(16,185,129,0.06) 0%,
        rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 18px;
    padding: 2rem 2.2rem;
    box-shadow:
        0 0 40px rgba(16,185,129,0.08),
        0 4px 16px rgba(0,0,0,0.4),
        0 1px 0 rgba(16,185,129,0.1) inset;
    white-space: pre-wrap;
    line-height: 1.8;
    font-size: 0.9rem;
    color: #e2e8f0;
}

/* ── Critique box ── */
.critique-box {
    background: linear-gradient(145deg,
        rgba(251,191,36,0.06) 0%,
        rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(251,191,36,0.2);
    border-radius: 18px;
    padding: 2rem 2.2rem;
    box-shadow:
        0 0 30px rgba(251,191,36,0.06),
        0 4px 16px rgba(0,0,0,0.4);
    white-space: pre-wrap;
    line-height: 1.8;
    font-size: 0.9rem;
    color: #e2e8f0;
}

/* ── Floating orbs ── */
.orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    pointer-events: none;
    z-index: 0;
    animation: float 8s ease-in-out infinite;
}
.orb-1 {
    width: 400px; height: 400px;
    top: -100px; left: -100px;
    background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%);
    animation-delay: 0s;
}
.orb-2 {
    width: 300px; height: 300px;
    bottom: -50px; right: -50px;
    background: radial-gradient(circle, rgba(16,185,129,0.06) 0%, transparent 70%);
    animation-delay: -4s;
}
@keyframes float {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-20px) scale(1.05); }
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
</style>

<!-- Floating ambient orbs -->
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key, default in {
    "running": False,
    "step_states": {1: "idle", 2: "idle", 3: "idle", 4: "idle"},
    "step_outputs": {1: "", 2: "", 3: "", 4: ""},
    "done": False,
    "elapsed": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ MULTI-AGENT RESEARCH SYSTEM</div>
    <h1>ResearchForge AI</h1>
    <p>Four specialized agents working in sequence — search, read, write, critique — to produce publication-ready research reports.</p>
</div>
""", unsafe_allow_html=True)


# ── Input card ────────────────────────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 2])
with col_input:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. What is the impact of AI on healthcare?",
        key="topic_input",
        label_visibility="visible"
    )
with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run_btn = st.button("⚡ Launch Pipeline", key="run_btn",
                        disabled=st.session_state.running)

st.markdown('</div>', unsafe_allow_html=True)


# ── Step definitions ──────────────────────────────────────────────────────────
STEPS = [
    (1, "🔍", "Search Agent",  "Querying the web via Tavily"),
    (2, "📖", "Reader Agent",  "Scraping & extracting content"),
    (3, "✍️", "Writer Agent",  "Synthesising the research report"),
    (4, "🎯", "Critic Agent",  "Evaluating quality & scoring"),
]


def render_steps():
    for num, icon, title, subtitle in STEPS:
        state = st.session_state.step_states[num]
        card_cls = {"idle": "", "running": "active", "done": "done", "error": "error"}[state]
        icon_cls = {"idle": "", "running": "", "done": "done", "error": "error"}[state]

        tag_map = {
            "idle":    '<span class="status-tag idle">◎ WAITING</span>',
            "running": '<span class="status-tag running">◉ RUNNING</span>',
            "done":    '<span class="status-tag done">✓ COMPLETE</span>',
            "error":   '<span class="status-tag error">✕ ERROR</span>',
        }

        output_html = ""
        if st.session_state.step_outputs[num]:
            content = st.session_state.step_outputs[num][:1200]
            content = content.replace("<", "&lt;").replace(">", "&gt;")
            output_html = f'<div class="step-content">{content}</div>'

        st.markdown(f"""
        <div class="step-card {card_cls}">
            <div class="step-header">
                <div class="step-icon {icon_cls}">{icon}</div>
                <div>
                    <div class="step-title">{title}</div>
                    <div class="step-subtitle">{subtitle}</div>
                </div>
                <div style="margin-left:auto">{tag_map[state]}</div>
            </div>
            {output_html}
        </div>
        """, unsafe_allow_html=True)


# ── Progress bar helper ───────────────────────────────────────────────────────
def render_progress(pct: int):
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-bar" style="width:{pct}%"></div>
    </div>
    """, unsafe_allow_html=True)


# ── Pipeline runner ───────────────────────────────────────────────────────────
def run_pipeline(topic: str):
    from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

    t0 = time.time()

    def set_step(n, state, output=""):
        st.session_state.step_states[n] = state
        if output:
            st.session_state.step_outputs[n] = output

    # STEP 1 — Search
    set_step(1, "running")
    progress_placeholder.empty()
    steps_placeholder.empty()
    with steps_placeholder.container():
        render_steps()
    with progress_placeholder:
        render_progress(10)
    try:
        search_agent = build_search_agent()
        res = search_agent.invoke({
            "messages": [("user", f"Find recent and reliable information about: {topic}")]
        })
        search_out = res["messages"][-1].content
        set_step(1, "done", search_out)
    except Exception as e:
        set_step(1, "error", str(e))
        st.session_state.running = False
        return

    # STEP 2 — Reader
    set_step(2, "running")
    steps_placeholder.empty()
    with steps_placeholder.container():
        render_steps()
    with progress_placeholder:
        render_progress(40)
    try:
        reader_agent = build_reader_agent()
        res = reader_agent.invoke({
            "messages": [("user",
                f"From these search results:\n\n{search_out}\n\nChoose the most useful URL, scrape it and summarize."
            )]
        })
        reader_out = res["messages"][-1].content
        set_step(2, "done", reader_out)
    except Exception as e:
        set_step(2, "error", str(e))
        st.session_state.running = False
        return

    # STEP 3 — Writer
    set_step(3, "running")
    steps_placeholder.empty()
    with steps_placeholder.container():
        render_steps()
    with progress_placeholder:
        render_progress(65)
    try:
        combined = f"Search Results:\n{search_out}\n\nScraped Content:\n{reader_out}"
        report = writer_chain.invoke({"topic": topic, "research": combined})
        set_step(3, "done", report[:500] + "...")
        st.session_state.step_outputs["report"] = report
    except Exception as e:
        set_step(3, "error", str(e))
        st.session_state.running = False
        return

    # STEP 4 — Critic
    set_step(4, "running")
    steps_placeholder.empty()
    with steps_placeholder.container():
        render_steps()
    with progress_placeholder:
        render_progress(88)
    try:
        critique = critic_chain.invoke({"report": report})
        set_step(4, "done", critique)
        st.session_state.step_outputs["critique"] = critique
    except Exception as e:
        set_step(4, "error", str(e))
        st.session_state.running = False
        return

    st.session_state.elapsed = round(time.time() - t0, 1)
    st.session_state.done = True
    st.session_state.running = False
    with progress_placeholder:
        render_progress(100)
    steps_placeholder.empty()
    with steps_placeholder.container():
        render_steps()


# ── Main layout ───────────────────────────────────────────────────────────────
st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown("""
    <div style="font-size:0.75rem;letter-spacing:0.12em;text-transform:uppercase;
                color:#4f46e5;font-weight:600;margin-bottom:1rem;">
        ▸ PIPELINE STATUS
    </div>
    """, unsafe_allow_html=True)

    progress_placeholder = st.empty()
    render_progress(0)
    steps_placeholder = st.empty()
    with steps_placeholder.container():
        render_steps()

with right_col:
    st.markdown("""
    <div style="font-size:0.75rem;letter-spacing:0.12em;text-transform:uppercase;
                color:#10b981;font-weight:600;margin-bottom:1rem;">
        ▸ OUTPUT
    </div>
    """, unsafe_allow_html=True)

    output_placeholder = st.empty()

    if not st.session_state.done:
        output_placeholder.markdown("""
        <div class="glass-card" style="min-height:420px;display:flex;align-items:center;
             justify-content:center;flex-direction:column;gap:1rem;">
            <div style="font-size:2.5rem;opacity:0.3">🔬</div>
            <div style="color:#334155;font-size:0.9rem;text-align:center;line-height:1.6;">
                Enter a topic and launch the<br>pipeline to see your report here.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Trigger pipeline ──────────────────────────────────────────────────────────
if run_btn and topic.strip() and not st.session_state.running:
    st.session_state.running = True
    st.session_state.done = False
    st.session_state.step_states = {1: "idle", 2: "idle", 3: "idle", 4: "idle"}
    st.session_state.step_outputs = {1: "", 2: "", 3: "", 4: ""}

    run_pipeline(topic.strip())
    st.rerun()

elif run_btn and not topic.strip():
    st.warning("Please enter a research topic first.")


# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.done:
    with output_placeholder.container():
        report = st.session_state.step_outputs.get("report", "")
        critique = st.session_state.step_outputs.get("critique", "")

        if report:
            st.markdown("""
            <div style="font-size:0.72rem;letter-spacing:0.1em;color:#6ee7b7;
                        font-family:'JetBrains Mono',monospace;margin-bottom:0.6rem;">
                ✓ REPORT GENERATED
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)

        if critique:
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size:0.72rem;letter-spacing:0.1em;color:#fbbf24;
                        font-family:'JetBrains Mono',monospace;margin-bottom:0.6rem;">
                ★ QUALITY CRITIQUE
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="critique-box">{critique}</div>', unsafe_allow_html=True)

    # Metrics row
    word_count = len(report.split()) if report else 0
    src_count = report.count("http") if report else 0

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-pill">
            <div class="metric-value">{st.session_state.elapsed}s</div>
            <div class="metric-label">Runtime</div>
        </div>
        <div class="metric-pill">
            <div class="metric-value">{word_count}</div>
            <div class="metric-label">Words</div>
        </div>
        <div class="metric-pill">
            <div class="metric-value">{src_count}</div>
            <div class="metric-label">Sources</div>
        </div>
        <div class="metric-pill">
            <div class="metric-value">4/4</div>
            <div class="metric-label">Agents</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Download button
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.download_button(
        label="⬇ Download Report (.txt)",
        data=f"TOPIC: {topic}\n\n{'='*60}\nREPORT\n{'='*60}\n{report}\n\n{'='*60}\nCRITIQUE\n{'='*60}\n{critique}",
        file_name=f"research_{topic[:30].replace(' ','_')}.txt",
        mime="text/plain",
    )