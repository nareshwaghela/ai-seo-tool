import streamlit as st
import random
import time
from PIL import Image

# ─── Try optional deps ────────────────────────────────────────────────────────
try:
    from pytrends.request import TrendReq
    PYTRENDS_OK = True
except ImportError:
    PYTRENDS_OK = False

try:
    import anthropic
    ANTHROPIC_OK = True
except ImportError:
    ANTHROPIC_OK = False

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI SEO Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── DARK GRADIENT UI (ChatGPT / Claude style) ────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root palette ── */
:root {
    --bg-base:       #0d0d10;
    --bg-surface:    #16161a;
    --bg-card:       #1e1e24;
    --bg-hover:      #26262f;
    --border:        #2a2a35;
    --accent:        #6c63ff;
    --accent-soft:   #4f46e5;
    --accent-glow:   rgba(108,99,255,0.25);
    --text-primary:  #f0f0f5;
    --text-muted:    #8b8b9e;
    --success:       #34d399;
    --warning:       #fbbf24;
    --danger:        #f87171;
    --radius:        12px;
    --radius-sm:     8px;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

/* ── Main area background ── */
.stApp {
    background: radial-gradient(ellipse at 20% 0%, rgba(108,99,255,0.12) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 100%, rgba(79,70,229,0.08) 0%, transparent 60%),
                var(--bg-base) !important;
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}

/* ── Selectbox dropdown ── */
div[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}
div[data-baseweb="popover"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
}
li[role="option"] {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}
li[role="option"]:hover {
    background: var(--bg-hover) !important;
}

/* ── Text inputs & text areas ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-size: 0.95rem !important;
    transition: border-color .2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
    outline: none !important;
}
textarea { color: var(--text-primary) !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent-soft)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.55rem 1.4rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: .3px !important;
    transition: transform .15s, box-shadow .15s !important;
    box-shadow: 0 4px 15px rgba(108,99,255,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(108,99,255,0.45) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: var(--bg-card) !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    transition: background .2s !important;
}
.stDownloadButton > button:hover {
    background: var(--accent) !important;
    color: #fff !important;
}

/* ── Info / success / warning boxes ── */
.stAlert {
    background: var(--bg-card) !important;
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--success)) !important;
    border-radius: 99px !important;
}
.stProgress > div > div {
    background: var(--bg-card) !important;
    border-radius: 99px !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="metric-container"] label {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
    letter-spacing: .5px !important;
    text-transform: uppercase !important;
}

/* ── Dividers ── */
hr { border-color: var(--border) !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border) !important;
    border-radius: var(--radius) !important;
}

/* ── Spinner ── */
.stSpinner { color: var(--accent) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
</style>
""", unsafe_allow_html=True)

# ─── HERO HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align:center;
    padding: 2.5rem 1rem 1.5rem;
">
    <div style="
        display:inline-flex;
        align-items:center;
        gap:.6rem;
        background: linear-gradient(135deg,#6c63ff22,#4f46e511);
        border:1px solid #6c63ff44;
        border-radius:999px;
        padding:.35rem 1rem;
        font-size:.78rem;
        color:#a5a0ff;
        letter-spacing:.8px;
        text-transform:uppercase;
        font-weight:600;
        margin-bottom:1rem;
    ">⚡ AI-Powered SEO Suite</div>
    <h1 style="
        font-size:2.6rem;
        font-weight:700;
        background: linear-gradient(135deg,#f0f0f5 0%,#a5a0ff 100%);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        background-clip:text;
        margin:0 0 .5rem;
        line-height:1.15;
    ">Your AI SEO Command Center</h1>
    <p style="color:#8b8b9e;font-size:1rem;margin:0;">
        Real keyword data · 2000+ word articles · Competitor insights
    </p>
</div>
<hr style="border-color:#2a2a35;margin:0 0 1.5rem;">
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='padding:.5rem 0 1rem;'>
    <div style='font-size:1.3rem;font-weight:700;color:#f0f0f5;'>🚀 SEO Suite</div>
    <div style='font-size:.75rem;color:#8b8b9e;margin-top:.2rem;'>Select a tool below</div>
</div>
""", unsafe_allow_html=True)

TOOLS = {
    "🔍 Keyword Scraper": "Google Keyword Scraper",
    "✍️ Blog Writer": "AI Blog Writer (2000+ words)",
    "📝 Blog Titles": "Blog Title Generator",
    "📊 Keyword Difficulty": "Keyword Difficulty Checker",
    "🏆 Competitor Analysis": "Competitor Analysis",
    "🖼️ Image SEO": "Image SEO Generator",
}

tool_label = st.sidebar.selectbox("Tool", list(TOOLS.keys()), label_visibility="collapsed")
tool = TOOLS[tool_label]

st.sidebar.markdown("<hr style='border-color:#2a2a35;'>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='font-size:.75rem;color:#8b8b9e;font-weight:600;text-transform:uppercase;letter-spacing:.8px;margin-bottom:.5rem;'>Settings</div>", unsafe_allow_html=True)

anthropic_key = st.sidebar.text_input(
    "Anthropic API Key",
    type="password",
    placeholder="sk-ant-api03-...",
    help="Required for AI Blog Writer. Get one at console.anthropic.com"
)

st.sidebar.markdown("""
<div style='margin-top:1.5rem;padding:.75rem;background:#1e1e24;border:1px solid #2a2a35;border-radius:8px;font-size:.78rem;color:#8b8b9e;line-height:1.5;'>
    💡 <strong style='color:#a5a0ff;'>Tip:</strong> Keyword Scraper pulls <em>live</em> Google Trends data via pytrends. Blog Writer uses Claude to generate 2000+ word articles.
</div>
""", unsafe_allow_html=True)

# ─── CARD HELPER ──────────────────────────────────────────────────────────────
def card(title, icon=""):
    st.markdown(f"""
    <div style='
        display:flex;align-items:center;gap:.6rem;
        margin-bottom:1.2rem;
    '>
        <span style='font-size:1.4rem;'>{icon}</span>
        <h2 style='margin:0;font-size:1.35rem;font-weight:700;color:#f0f0f5;'>{title}</h2>
    </div>
    """, unsafe_allow_html=True)

def kw_pill(kw, vol=None, diff=None):
    vol_html = f"<span style='color:#34d399;font-size:.72rem;margin-left:.5rem;'>↑ {vol:,}</span>" if vol else ""
    diff_color = "#f87171" if diff and diff > 60 else ("#fbbf24" if diff and diff > 35 else "#34d399")
    diff_html = f"<span style='color:{diff_color};font-size:.72rem;margin-left:.4rem;'>D:{diff}</span>" if diff else ""
    st.markdown(f"""
    <div style='
        display:inline-flex;align-items:center;
        background:#1e1e24;border:1px solid #2a2a35;
        border-radius:6px;padding:.35rem .75rem;
        margin:.25rem .25rem .25rem 0;font-size:.88rem;color:#f0f0f5;
    '>🔑 {kw}{vol_html}{diff_html}</div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TOOL: GOOGLE KEYWORD SCRAPER (real data via pytrends)
# ══════════════════════════════════════════════════════════════════════════════
if tool == "Google Keyword Scraper":
    card("Google Keyword Scraper", "🔍")

    st.markdown("""
    <div style='background:#1e1e24;border:1px solid #2a2a35;border-radius:10px;padding:1rem 1.2rem;margin-bottom:1.2rem;font-size:.88rem;color:#8b8b9e;'>
        Pulls <strong style='color:#a5a0ff;'>live data</strong> from Google Trends via <code style='background:#26262f;padding:.1rem .4rem;border-radius:4px;color:#f0f0f5;'>pytrends</code>.
        Requires: <code style='background:#26262f;padding:.1rem .4rem;border-radius:4px;color:#f0f0f5;'>pip install pytrends</code>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("Seed keyword", placeholder="e.g. content marketing")
    with col2:
        geo = st.selectbox("Country", ["Worldwide", "US", "IN", "GB", "AU"])

    geo_map = {"Worldwide": "", "US": "US", "IN": "IN", "GB": "GB", "AU": "AU"}

    if st.button("🔍 Scrape Keywords", use_container_width=True):
        if not topic:
            st.warning("Please enter a keyword.")
        elif not PYTRENDS_OK:
            st.error("pytrends not installed. Run: `pip install pytrends`")
        else:
            with st.spinner("Connecting to Google Trends…"):
                try:
                    pytrends = TrendReq(hl='en-US', tz=330)
                    pytrends.build_payload([topic], geo=geo_map[geo], timeframe='today 12-m')

                    # Related queries
                    related = pytrends.related_queries()
                    top_df    = related[topic].get("top")
                    rising_df = related[topic].get("rising")

                    # Interest over time (for volume proxy)
                    iot = pytrends.interest_over_time()
                    avg_interest = int(iot[topic].mean()) if topic in iot.columns else 0

                    st.markdown(f"""
                    <div style='display:flex;gap:1rem;margin-bottom:1.2rem;flex-wrap:wrap;'>
                        <div style='background:#1e1e24;border:1px solid #2a2a35;border-radius:10px;padding:.8rem 1.2rem;flex:1;min-width:140px;'>
                            <div style='font-size:.72rem;color:#8b8b9e;text-transform:uppercase;letter-spacing:.6px;'>Avg Interest</div>
                            <div style='font-size:1.6rem;font-weight:700;color:#6c63ff;'>{avg_interest}<span style='font-size:.9rem;color:#8b8b9e;'>/100</span></div>
                        </div>
                        <div style='background:#1e1e24;border:1px solid #2a2a35;border-radius:10px;padding:.8rem 1.2rem;flex:1;min-width:140px;'>
                            <div style='font-size:.72rem;color:#8b8b9e;text-transform:uppercase;letter-spacing:.6px;'>Top Keywords</div>
                            <div style='font-size:1.6rem;font-weight:700;color:#34d399;'>{len(top_df) if top_df is not None else 0}</div>
                        </div>
                        <div style='background:#1e1e24;border:1px solid #2a2a35;border-radius:10px;padding:.8rem 1.2rem;flex:1;min-width:140px;'>
                            <div style='font-size:.72rem;color:#8b8b9e;text-transform:uppercase;letter-spacing:.6px;'>Rising Keywords</div>
                            <div style='font-size:1.6rem;font-weight:700;color:#fbbf24;'>{len(rising_df) if rising_df is not None else 0}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    col_a, col_b = st.columns(2)

                    with col_a:
                        st.markdown("<div style='font-weight:600;color:#34d399;margin-bottom:.5rem;'>📈 Top Related Keywords</div>", unsafe_allow_html=True)
                        if top_df is not None and not top_df.empty:
                            for _, row in top_df.head(15).iterrows():
                                kw_pill(row['query'], vol=int(row['value']))
                        else:
                            st.info("No top keywords found.")

                    with col_b:
                        st.markdown("<div style='font-weight:600;color:#fbbf24;margin-bottom:.5rem;'>🚀 Rising / Breakout Keywords</div>", unsafe_allow_html=True)
                        if rising_df is not None and not rising_df.empty:
                            for _, row in rising_df.head(15).iterrows():
                                label = "Breakout 🔥" if str(row['value']) == "Breakout" else f"+{row['value']}%"
                                st.markdown(f"""
                                <div style='background:#1e1e24;border:1px solid #2a2a35;border-radius:6px;padding:.35rem .75rem;margin:.25rem 0;font-size:.88rem;color:#f0f0f5;display:flex;justify-content:space-between;'>
                                    <span>🔑 {row['query']}</span>
                                    <span style='color:#fbbf24;font-size:.75rem;'>{label}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No rising keywords found.")

                    # Also show suggested combos
                    st.markdown("<div style='font-weight:600;color:#a5a0ff;margin:1rem 0 .5rem;'>💡 Suggested Long-Tail Keywords</div>", unsafe_allow_html=True)
                    modifiers = ["best", "how to", "guide", "tips", "tools for", "vs", "for beginners", "in 2026", "free", "tutorial"]
                    for m in modifiers:
                        kw_pill(f"{m} {topic}")

                except Exception as e:
                    st.error(f"Google Trends error: {e}\n\nTip: Too many requests? Wait 60s and retry.")

# ══════════════════════════════════════════════════════════════════════════════
# TOOL: AI BLOG WRITER (2000+ words via Claude)
# ══════════════════════════════════════════════════════════════════════════════
elif tool == "AI Blog Writer (2000+ words)":
    card("AI Blog Writer — 2000+ Words", "✍️")

    st.markdown("""
    <div style='background:#1e1e24;border:1px solid #6c63ff44;border-radius:10px;padding:1rem 1.2rem;margin-bottom:1.2rem;font-size:.88rem;color:#8b8b9e;'>
        Powered by <strong style='color:#a5a0ff;'>Claude</strong>. Generates a fully structured, SEO-optimised article (2000–2500 words).
        Add your API key in the sidebar.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input("Article topic", placeholder="e.g. The Future of AI in Digital Marketing")
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Conversational", "Authoritative", "Educational", "Engaging"])

    target_kw = st.text_input("Target keyword (optional)", placeholder="e.g. AI digital marketing 2026")
    audience  = st.text_input("Target audience (optional)", placeholder="e.g. marketing managers, small business owners")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        include_faq   = st.checkbox("Include FAQ section", value=True)
    with col_b:
        include_stats = st.checkbox("Include stats & data", value=True)
    with col_c:
        include_cta   = st.checkbox("Include CTA section", value=True)

    if st.button("✍️ Generate Full Article", use_container_width=True):
        if not topic:
            st.warning("Please enter an article topic.")
        elif not anthropic_key:
            st.warning("Please enter your Anthropic API key in the sidebar.")
        elif not ANTHROPIC_OK:
            st.error("anthropic package not installed. Run: `pip install anthropic`")
        else:
            prompt_parts = [
                f"Write a comprehensive, SEO-optimised blog article about: **{topic}**",
                f"Tone: {tone}",
                f"Target keyword: {target_kw}" if target_kw else "",
                f"Target audience: {audience}" if audience else "",
                "",
                "Requirements:",
                "- Minimum 2000 words (aim for 2200–2500)",
                "- Include a compelling H1 title",
                "- Well-structured with H2 and H3 subheadings",
                "- Start with a strong hook introduction (150–200 words)",
                "- Include a TL;DR summary box after the intro",
                "- Use short paragraphs (3–4 sentences max) for readability",
                "- Naturally integrate the target keyword throughout",
                "- Include actionable tips or takeaways",
                "- Include a numbered or bulleted list section",
                f"{'- Include an FAQ section with 5 questions at the end' if include_faq else ''}",
                f"{'- Reference relevant statistics, research, or data points' if include_stats else ''}",
                f"{'- End with a compelling CTA (call to action) paragraph' if include_cta else ''}",
                "- End with a brief conclusion",
                "",
                "Format the article in clean Markdown.",
            ]
            prompt = "\n".join(p for p in prompt_parts if p is not None)

            with st.spinner("Claude is writing your article… (this takes 30–60 seconds)"):
                try:
                    client = anthropic.Anthropic(api_key=anthropic_key)
                    message = client.messages.create(
                        model="claude-opus-4-5",
                        max_tokens=4096,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    article_text = message.content[0].text
                    word_count   = len(article_text.split())

                    st.success(f"✅ Article generated! **{word_count:,} words**")

                    tab1, tab2 = st.tabs(["📄 Preview", "✏️ Edit & Export"])

                    with tab1:
                        st.markdown(article_text)

                    with tab2:
                        edited = st.text_area("Edit your article", article_text, height=500)
                        wc2 = len(edited.split())
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Words", f"{wc2:,}")
                        col2.metric("Characters", f"{len(edited):,}")
                        col3.metric("Est. read time", f"{max(1, wc2 // 200)} min")

                        st.download_button(
                            "⬇️ Download as .md",
                            edited,
                            file_name=f"{topic[:40].replace(' ','_').lower()}.md",
                            mime="text/markdown",
                            use_container_width=True,
                        )
                        st.download_button(
                            "⬇️ Download as .txt",
                            edited,
                            file_name=f"{topic[:40].replace(' ','_').lower()}.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )

                except Exception as e:
                    st.error(f"Anthropic API error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# TOOL: BLOG TITLE GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
elif tool == "Blog Title Generator":
    card("Blog Title Generator", "📝")

    topic = st.text_input("Enter topic", placeholder="e.g. email marketing")

    if st.button("Generate Titles", use_container_width=True):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            titles = [
                (f"10 Best {topic} Tips for Beginners in 2026",          "Listicle"),
                (f"The Ultimate {topic} Guide: Everything You Need",      "Pillar"),
                (f"How to Master {topic} in 30 Days (Step-by-Step)",     "How-to"),
                (f"Why Your {topic} Strategy Is Failing (And How to Fix)", "Problem/Solution"),
                (f"{topic} vs. Traditional Methods: Which Wins?",         "Comparison"),
                (f"The Beginner's Blueprint to {topic}",                   "Educational"),
                (f"I Tried Every {topic} Tool — Here's What Works",       "First-person"),
                (f"{topic} in 2026: Trends, Tools & Predictions",         "Trend"),
                (f"How Top Brands Use {topic} to Drive Results",          "Authority"),
                (f"The Hidden Power of {topic} Most Marketers Ignore",    "Curiosity"),
            ]
            st.markdown("<div style='margin-bottom:.5rem;font-weight:600;color:#a5a0ff;'>Generated Titles</div>", unsafe_allow_html=True)
            for title, label in titles:
                st.markdown(f"""
                <div style='background:#1e1e24;border:1px solid #2a2a35;border-radius:8px;padding:.65rem 1rem;margin:.35rem 0;display:flex;justify-content:space-between;align-items:center;'>
                    <span style='font-size:.92rem;color:#f0f0f5;'>{title}</span>
                    <span style='font-size:.72rem;color:#6c63ff;background:#6c63ff18;border:1px solid #6c63ff33;border-radius:99px;padding:.15rem .55rem;margin-left:.75rem;white-space:nowrap;'>{label}</span>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TOOL: KEYWORD DIFFICULTY
# ══════════════════════════════════════════════════════════════════════════════
elif tool == "Keyword Difficulty Checker":
    card("Keyword Difficulty Checker", "📊")

    keyword = st.text_input("Enter keyword", placeholder="e.g. best CRM software")

    if st.button("Check Difficulty", use_container_width=True):
        if not keyword:
            st.warning("Please enter a keyword.")
        else:
            difficulty  = random.randint(20, 90)
            volume      = random.randint(500, 50000)
            cpc         = round(random.uniform(0.5, 8.5), 2)
            opportunity = max(0, 100 - difficulty + random.randint(-10, 10))

            color = "#34d399" if difficulty < 35 else ("#fbbf24" if difficulty < 65 else "#f87171")
            label = "Easy 🟢" if difficulty < 35 else ("Medium 🟡" if difficulty < 65 else "Hard 🔴")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Difficulty", f"{difficulty}/100", label)
            col2.metric("Est. Monthly Searches", f"{volume:,}")
            col3.metric("CPC (USD)", f"${cpc}")
            col4.metric("Opportunity Score", f"{opportunity}/100")

            st.progress(difficulty / 100)

            if difficulty < 35:
                st.success("✅ Low competition — great target for new sites!")
            elif difficulty < 65:
                st.warning("⚠️ Medium competition — needs quality content & backlinks.")
            else:
                st.error("🔴 High competition — consider long-tail variants.")

# ══════════════════════════════════════════════════════════════════════════════
# TOOL: COMPETITOR ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif tool == "Competitor Analysis":
    card("Competitor Content Analysis", "🏆")

    topic = st.text_input("Enter topic / niche", placeholder="e.g. project management software")

    if st.button("Analyse Competitors", use_container_width=True):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            competitors = [
                ("HubSpot",    f"The Complete {topic} Guide",           random.randint(2000, 8000), random.randint(40, 90), random.randint(80, 200)),
                ("Ahrefs",     f"{topic} Tutorial for Beginners",       random.randint(1500, 6000), random.randint(30, 80), random.randint(60, 180)),
                ("Neil Patel", f"How to Use {topic} to Grow Traffic",   random.randint(1800, 7000), random.randint(35, 85), random.randint(50, 160)),
                ("Backlinko",  f"{topic}: The Definitive Guide",        random.randint(3000, 9000), random.randint(50, 95), random.randint(100, 300)),
                ("Moz",        f"{topic} Best Practices & Examples",    random.randint(1200, 5000), random.randint(25, 75), random.randint(40, 140)),
            ]

            st.markdown("""
            <div style='display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:.5rem;padding:.5rem .75rem;font-size:.75rem;color:#8b8b9e;text-transform:uppercase;letter-spacing:.6px;font-weight:600;'>
                <div>Article / Source</div><div>Words</div><div>DA</div><div>Backlinks</div><div>Gap</div>
            </div>
            """, unsafe_allow_html=True)

            for brand, title, words, da, links in competitors:
                gap_color = "#34d399" if da < 60 else "#f87171"
                gap_label = "Beatable" if da < 60 else "Tough"
                st.markdown(f"""
                <div style='display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:.5rem;
                    background:#1e1e24;border:1px solid #2a2a35;border-radius:8px;
                    padding:.65rem .75rem;margin:.3rem 0;align-items:center;font-size:.88rem;'>
                    <div>
                        <div style='font-weight:600;color:#f0f0f5;'>{title}</div>
                        <div style='font-size:.75rem;color:#8b8b9e;'>{brand}</div>
                    </div>
                    <div style='color:#a5a0ff;'>{words:,}</div>
                    <div style='color:#fbbf24;'>{da}</div>
                    <div style='color:#34d399;'>{links}</div>
                    <div style='color:{gap_color};font-weight:600;font-size:.8rem;'>{gap_label}</div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TOOL: IMAGE SEO GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
elif tool == "Image SEO Generator":
    card("Image SEO Generator", "🖼️")

    uploaded = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded:
        img = Image.open(uploaded)
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(img, caption="Uploaded Image", use_container_width=True)

        with col2:
            w, h = img.size
            st.metric("Dimensions", f"{w} × {h} px")
            st.metric("Format", img.format or uploaded.type.split("/")[-1].upper())
            size_kb = round(uploaded.size / 1024, 1)
            st.metric("File Size", f"{size_kb} KB")

        captions = [
            "Artificial intelligence technology concept illustration",
            "Digital marketing automation and analytics dashboard",
            "AI-powered SEO tools workflow visualization",
            "Modern content strategy and optimization graphic",
            "Business growth and digital analytics concept",
        ]

        choice = random.choice(captions)

        st.markdown("<div style='font-weight:600;color:#a5a0ff;margin:.75rem 0 .4rem;'>🏷️ Suggested Alt Text</div>", unsafe_allow_html=True)
        alt_text = st.text_input("Alt text (editable)", choice)

        filename_base = uploaded.name.rsplit(".", 1)[0].replace(" ", "-").lower()
        st.markdown("<div style='font-weight:600;color:#a5a0ff;margin:.75rem 0 .4rem;'>📁 SEO Filename</div>", unsafe_allow_html=True)
        st.code(f"{filename_base}-seo-optimized.{img.format.lower() if img.format else 'jpg'}", language="text")

        st.markdown("<div style='font-weight:600;color:#a5a0ff;margin:.75rem 0 .4rem;'>📋 HTML Snippet</div>", unsafe_allow_html=True)
        st.code(f'<img src="{filename_base}-seo-optimized.jpg" alt="{alt_text}" width="{w}" height="{h}" loading="lazy">', language="html")
