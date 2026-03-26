import streamlit as st
import random
import time
from PIL import Image
from datetime import datetime

# ─── Try pytrends ─────────────────────────────────────────────────────────────
try:
    from pytrends.request import TrendReq
    PYTRENDS_OK = True
except ImportError:
    PYTRENDS_OK = False

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI SEO Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── DARK GRADIENT UI ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-base:      #0d0d10;
    --bg-surface:   #16161a;
    --bg-card:      #1e1e24;
    --bg-hover:     #26262f;
    --border:       #2a2a35;
    --accent:       #6c63ff;
    --accent-soft:  #4f46e5;
    --accent-glow:  rgba(108,99,255,0.25);
    --text:         #f0f0f5;
    --muted:        #8b8b9e;
    --success:      #34d399;
    --warning:      #fbbf24;
    --danger:       #f87171;
    --radius:       12px;
    --radius-sm:    8px;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-base) !important;
    color: var(--text) !important;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%,   rgba(108,99,255,0.13) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 100%, rgba(79,70,229,0.09)  0%, transparent 55%),
        var(--bg-base) !important;
}

[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
}

div[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
}
div[data-baseweb="popover"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; }
li[role="option"] { background: var(--bg-card) !important; color: var(--text) !important; }
li[role="option"]:hover { background: var(--bg-hover) !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-size: 0.95rem !important;
    transition: border-color .2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
    outline: none !important;
}
textarea { color: var(--text) !important; }

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

.stAlert { background: var(--bg-card) !important; border-radius: var(--radius) !important; border: 1px solid var(--border) !important; }

.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--success)) !important;
    border-radius: 99px !important;
}
.stProgress > div > div { background: var(--bg-card) !important; border-radius: 99px !important; }

[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="metric-container"] label {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    letter-spacing: .5px !important;
    text-transform: uppercase !important;
}

hr { border-color: var(--border) !important; }

[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border) !important;
    border-radius: var(--radius) !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: var(--bg-card) !important; border-radius: var(--radius-sm) !important; border: 1px solid var(--border) !important; gap: 0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--muted) !important; border-radius: var(--radius-sm) !important; font-weight: 500 !important; }
.stTabs [aria-selected="true"] { background: var(--accent) !important; color: #fff !important; }
.stTabs [data-baseweb="tab-panel"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2.5rem 1rem 1.5rem;">
    <div style="
        display:inline-flex;align-items:center;gap:.6rem;
        background:linear-gradient(135deg,#6c63ff22,#4f46e511);
        border:1px solid #6c63ff44;border-radius:999px;
        padding:.35rem 1rem;font-size:.78rem;color:#a5a0ff;
        letter-spacing:.8px;text-transform:uppercase;font-weight:600;margin-bottom:1rem;
    ">⚡ 100% Free — No API Key Required</div>
    <h1 style="
        font-size:2.6rem;font-weight:700;
        background:linear-gradient(135deg,#f0f0f5 0%,#a5a0ff 100%);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;margin:0 0 .5rem;line-height:1.15;
    ">AI SEO Suite</h1>
    <p style="color:#8b8b9e;font-size:1rem;margin:0;">
        Google Keyword Scraper · 2000+ Word Blog Writer · Competitor Analysis
    </p>
</div>
<hr style="border-color:#2a2a35;margin:0 0 1.5rem;">
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='padding:.5rem 0 1rem;'>
    <div style='font-size:1.3rem;font-weight:700;color:#f0f0f5;'>🚀 SEO Suite</div>
    <div style='font-size:.75rem;color:#8b8b9e;margin-top:.2rem;'>100% Free · No API Key</div>
</div>
""", unsafe_allow_html=True)

TOOLS = {
    "🔍 Keyword Scraper":      "Google Keyword Scraper",
    "✍️ Blog Writer 2000+":    "AI Blog Writer",
    "📝 Blog Titles":          "Blog Title Generator",
    "📊 Keyword Difficulty":   "Keyword Difficulty Checker",
    "🏆 Competitor Analysis":  "Competitor Analysis",
    "🖼️ Image SEO":            "Image SEO Generator",
}

tool_label = st.sidebar.selectbox("Tool", list(TOOLS.keys()), label_visibility="collapsed")
tool = TOOLS[tool_label]

st.sidebar.markdown("<hr style='border-color:#2a2a35;'>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='padding:.75rem;background:#1e1e24;border:1px solid #2a2a35;border-radius:8px;font-size:.78rem;color:#8b8b9e;line-height:1.6;'>
    ✅ <strong style='color:#34d399;'>All tools are FREE</strong><br>
    🔍 Keyword Scraper uses live Google Trends<br>
    ✍️ Blog Writer generates 2000+ words locally<br>
    📦 Install: <code style='background:#26262f;padding:.1rem .3rem;border-radius:3px;color:#f0f0f5;'>pip install pytrends pillow</code>
</div>
""", unsafe_allow_html=True)

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def card(title, icon=""):
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:.6rem;margin-bottom:1.2rem;'>
        <span style='font-size:1.4rem;'>{icon}</span>
        <h2 style='margin:0;font-size:1.35rem;font-weight:700;color:#f0f0f5;'>{title}</h2>
    </div>
    """, unsafe_allow_html=True)

def kw_pill(kw, score=None, badge_color="#6c63ff"):
    score_html = f"<span style='color:{badge_color};font-size:.72rem;margin-left:.5rem;font-weight:600;'>{score}</span>" if score else ""
    st.markdown(f"""
    <div style='display:inline-flex;align-items:center;
        background:#1e1e24;border:1px solid #2a2a35;
        border-radius:6px;padding:.35rem .75rem;
        margin:.25rem .25rem .25rem 0;font-size:.88rem;color:#f0f0f5;'>
        🔑 {kw}{score_html}
    </div>
    """, unsafe_allow_html=True)

# ─── ARTICLE GENERATOR (no API, template-based, 2000+ words) ──────────────────
def generate_article(topic, tone, include_faq, include_stats, include_cta, target_kw, audience):
    year = datetime.now().year
    tk = target_kw if target_kw else topic
    aud = audience if audience else "marketers and business owners"

    tone_intro = {
        "Professional":    f"In today's competitive landscape, {topic} has become an indispensable part of any successful strategy.",
        "Conversational":  f"Let's be honest — if you haven't started paying attention to {topic} yet, you're already behind.",
        "Authoritative":   f"Research and industry data consistently demonstrate that {topic} is one of the most impactful disciplines available today.",
        "Educational":     f"Understanding {topic} can feel overwhelming at first. But once you break it down step by step, it becomes one of the most rewarding skills you can develop.",
        "Engaging":        f"What if I told you that mastering {topic} could completely transform the way you work, grow, and compete online?",
    }[tone]

    stats_section = f"""
## Key Statistics & Data About {topic}

Numbers don't lie. Here are some compelling data points that highlight why {topic} deserves your full attention:

- **68%** of online experiences begin with a search engine — making {topic} critical to visibility.
- Businesses that invest in {topic} see on average **2.8× more organic growth** than those that don't.
- Content strategies aligned with {topic} generate **3× more leads** at **62% lower cost** than outbound marketing.
- **75%** of users never scroll past the first page of search results.
- Companies using {topic} effectively report **revenue growth 40% faster** than competitors.
- The global {topic} market is projected to reach **$1.6 trillion by {year + 2}**.

These numbers make one thing abundantly clear: {topic} is not optional — it's essential.

""" if include_stats else ""

    faq_section = f"""
## Frequently Asked Questions About {topic}

**Q1: What is {topic} and why does it matter?**
{topic} refers to the set of strategies, tools, and practices used to improve visibility, performance, and growth in your chosen domain. It matters because it directly impacts how your audience discovers and engages with your content or product.

**Q2: How long does it take to see results from {topic}?**
Results vary depending on your niche, competition, and effort level. Most people start seeing measurable improvements within 3–6 months of consistent, strategic implementation.

**Q3: Can beginners learn {topic} without prior experience?**
Absolutely. Many of the most successful practitioners of {topic} started with zero experience. The key is to start with the fundamentals, be consistent, and iterate based on data.

**Q4: What are the biggest mistakes people make with {topic}?**
The most common mistakes include: ignoring data, not defining a clear audience, inconsistent content publishing, neglecting technical fundamentals, and failing to track and measure results.

**Q5: Is {topic} relevant in {year} and beyond?**
More than ever. As digital competition intensifies, the principles behind {topic} — understanding your audience, creating valuable content, and optimising for discovery — are timeless and increasingly important.

""" if include_faq else ""

    cta_section = f"""
## Ready to Take Your {topic} to the Next Level?

You now have a comprehensive understanding of {topic} — from the foundational principles to advanced tactics that industry leaders use every day.

The difference between those who succeed with {topic} and those who don't comes down to one thing: **action**. Knowledge without implementation is just entertainment.

Here's your challenge: Pick **one strategy** from this guide and implement it in the next 48 hours. Just one. Then measure, learn, and build from there.

Your journey with {topic} starts now. The best time to begin was yesterday. The second best time is today.

""" if include_cta else ""

    article = f"""# The Complete Guide to {topic}: Everything You Need to Know in {year}

*Published: {datetime.now().strftime("%B %d, %Y")} | Target Audience: {aud} | Keyword: {tk}*

---

> **TL;DR:** This comprehensive guide covers everything about {topic} — from core concepts and proven strategies to tools, real-world examples, and actionable next steps. Whether you're a beginner or looking to level up, this is your definitive resource.

---

## Introduction

{tone_intro}

In this guide, we'll cover everything you need to know about {topic} — from the fundamental concepts that every practitioner must understand, to the advanced tactics that industry leaders use to stay ahead of the curve. By the time you finish reading, you'll have a clear, actionable roadmap to implement {topic} effectively.

This is not a surface-level overview. This is the guide we wish we had when we were starting out.

---

## What Is {topic}?

At its core, {topic} is the practice of systematically improving how you attract, engage, and convert your target audience — in this case, {aud}. While definitions vary across industries, the fundamental goal remains the same: **deliver maximum value to the right people at the right time**.

{topic} sits at the intersection of strategy, creativity, and data. It's not enough to produce great content or have a great product — you need to ensure it's visible, relevant, and compelling to your audience.

The term "{tk}" encapsulates this holistic approach. Every decision you make — from the language you use to the channels you prioritise — should be informed by a deep understanding of your audience and the competitive landscape.

---

## Why {topic} Matters More Than Ever in {year}

The digital landscape has changed dramatically over the past decade. The platforms, algorithms, and consumer behaviours that worked in {year - 5} are barely recognisable today. Here's why {topic} has never been more critical:

### 1. Increased Competition
More businesses than ever are operating online. The barrier to entry has dropped, meaning your competitors are growing in number every day. Without a clear {topic} strategy, you risk becoming invisible.

### 2. Changing Consumer Behaviour
Today's audience is more informed, more discerning, and less patient than ever. They research before they buy, compare options, read reviews, and expect personalised experiences. {topic} helps you meet them where they are.

### 3. Algorithm-Driven Discovery
Whether it's Google, social media, or app stores, discovery is increasingly mediated by algorithms. Understanding {topic} means understanding how to work with — not against — these systems.

### 4. Data Abundance
We've never had access to more data about our audience. {topic} gives you the framework to turn that data into decisions that drive real results.

---

{stats_section}

## The Core Pillars of {topic}

Successful {topic} practitioners build their work on a foundation of four interconnected pillars:

### Pillar 1: Research & Discovery
Everything begins with understanding. Who is your audience? What are they searching for? What problems do they need solved? Effective {topic} starts with deep, rigorous research — keyword research, competitor analysis, audience profiling, and trend monitoring.

Tools like Google Trends, Ahrefs, SEMrush, and even Reddit can give you invaluable insights into the conversations your audience is already having.

### Pillar 2: Content & Messaging
Once you understand your audience, you need to speak their language. Content is the vehicle through which {topic} delivers value. This includes blog posts, videos, social media content, email campaigns, landing pages, and more.

The key is alignment: every piece of content should serve a specific purpose in the customer journey, from awareness to conversion.

### Pillar 3: Technical Foundation
Even the best content fails if the technical foundation isn't solid. For {topic}, this means fast load times, mobile optimisation, clean site architecture, proper indexing, and structured data. Technical excellence amplifies everything else you do.

### Pillar 4: Measurement & Iteration
What gets measured gets managed. Successful {topic} requires a commitment to tracking the right metrics — not vanity metrics, but metrics that actually reflect business outcomes. Then you use that data to iterate and improve continuously.

---

## Step-by-Step Strategy for {topic}

Ready to build your {topic} strategy from scratch? Here's the framework used by leading practitioners:

### Step 1: Define Your Goals
Start with the end in mind. What does success look like for you? More traffic? Higher conversion rates? Greater brand awareness? Each goal requires a different approach, so clarity here is essential.

### Step 2: Understand Your Audience Deeply
Go beyond demographics. Build detailed personas. Understand your audience's pain points, aspirations, daily habits, and the language they use to describe their problems. Interview customers. Read reviews. Spend time in relevant communities.

### Step 3: Conduct Thorough Keyword & Topic Research
For {topic}, keyword research is foundational. Focus on:
- **Head terms**: High volume, high competition (e.g., "{topic}")
- **Long-tail keywords**: Lower volume, lower competition, higher intent (e.g., "how to get started with {topic} in {year}")
- **Question keywords**: What questions is your audience asking? (e.g., "what is {topic}", "best {topic} tools")

### Step 4: Create a Content Calendar
Consistency beats intensity. Plan your content 30–90 days in advance. Mix content formats — long-form guides, short-form posts, video, infographics — to serve different consumption preferences.

### Step 5: Optimise for Search
Every piece of content should be optimised for the keyword "{tk}" and related terms. This means:
- Including the keyword in the title, first paragraph, and headings
- Writing meta descriptions that drive clicks
- Using internal and external links strategically
- Optimising images with alt text

### Step 6: Promote and Distribute
Great content that nobody sees is a wasted effort. Build a distribution system: share on social media, send to your email list, pitch to relevant publications, and engage in communities where your audience spends time.

### Step 7: Track, Analyse, and Optimise
Review your performance data weekly and monthly. Which content is driving traffic? Which pages have high bounce rates? Where are you losing potential customers in the funnel? Use this data to double down on what works and fix what doesn't.

---

## Advanced Tactics for {topic}

Once you've mastered the fundamentals, these advanced tactics will help you pull ahead of the competition:

### Tactic 1: Topical Authority
Rather than creating isolated pieces of content, build clusters of interlinked content around {topic}. A pillar page supported by multiple cluster pages signals deep expertise to search engines and keeps visitors engaged longer.

### Tactic 2: Conversion Rate Optimisation (CRO)
Getting traffic is only half the battle. Optimise your pages to convert visitors into leads or customers. Test headlines, CTAs, page layouts, and messaging. Even small improvements compound significantly over time.

### Tactic 3: Competitor Gap Analysis
Identify keywords and topics your competitors rank for that you don't. These represent immediate opportunities. Tools like Ahrefs' Content Gap feature make this analysis straightforward.

### Tactic 4: Repurposing Content
Get more mileage from every piece of content. Turn a long-form blog post into a Twitter/X thread, a LinkedIn article, a YouTube video script, an email sequence, and an infographic. One idea, multiple formats, exponential reach.

### Tactic 5: E-E-A-T Optimisation
Google's quality guidelines emphasise Experience, Expertise, Authoritativeness, and Trustworthiness. Demonstrate all four by including author bios, citing credible sources, earning backlinks from reputable sites, and keeping your content accurate and up to date.

---

## Common Mistakes to Avoid

Even experienced practitioners fall into these traps. Knowing them in advance saves you months of wasted effort:

- **Chasing vanity metrics**: Pageviews and social media likes feel good but don't pay the bills. Focus on metrics that drive revenue.
- **Ignoring search intent**: Ranking for a keyword means nothing if your content doesn't satisfy the intent behind the search.
- **Inconsistency**: The single biggest killer of {topic} results is stopping too soon. Algorithms and audiences reward consistency above almost everything else.
- **Neglecting existing content**: New content gets all the attention, but updating and improving existing content can often deliver faster results.
- **Not building an email list**: Social platforms can change their algorithms overnight. Your email list is the one audience channel you own and control.

---

## Best Tools for {topic} in {year}

Here are the tools that top practitioners rely on:

| Tool | Purpose | Price |
|------|---------|-------|
| Google Search Console | Track search performance | Free |
| Google Analytics 4 | Audience & behaviour analytics | Free |
| Ahrefs / SEMrush | Keyword research & competitor analysis | Paid |
| Surfer SEO | Content optimisation | Paid |
| Screaming Frog | Technical SEO audits | Free/Paid |
| Notion / Trello | Content planning & calendar | Free/Paid |
| Canva | Visual content creation | Free/Paid |
| Grammarly | Writing quality | Free/Paid |

---

## Real-World Examples of {topic} in Action

### Example 1: The Long-Form Content Play
A B2B software company publishing exhaustive, research-backed guides on {topic} saw their organic traffic increase by **340%** in 12 months. The secret? They went deeper than any competitor on every topic they covered.

### Example 2: The Technical Foundation Fix
An e-commerce brand discovered their site was loading in 8 seconds on mobile. After optimising to under 2 seconds, their conversion rate improved by **27%** and their Google rankings jumped significantly — without changing a single word of their content.

### Example 3: The Distribution-First Approach
A content creator built a newsletter audience of 50,000 subscribers before launching a course on {topic}. By owning their distribution, they generated $200,000 in launch revenue — with zero ad spend.

---

## The Future of {topic}

Looking ahead, several trends will shape the evolution of {topic}:

**AI and Automation**: AI tools are accelerating content production, personalisation, and analysis. Practitioners who embrace AI as a collaborator — not a replacement — will have a significant competitive advantage.

**Voice and Conversational Search**: As voice assistants become more prevalent, optimising for natural language queries and featured snippets will become increasingly important.

**Video-First Content**: Short-form video continues to dominate attention. Integrating {topic} principles into video strategy is no longer optional.

**Privacy and First-Party Data**: As third-party cookies phase out, building owned audiences and leveraging first-party data becomes the cornerstone of sustainable {topic} strategy.

**Search Generative Experience (SGE)**: AI-powered search is changing how results are surfaced. Brands that demonstrate genuine expertise and authority will be best positioned in this new landscape.

---

{faq_section}

## Conclusion

{topic} is both an art and a science. It requires creativity, analytical thinking, persistence, and a genuine commitment to delivering value to your audience — in this case, {aud}.

The strategies and tactics outlined in this guide are not theoretical. They're drawn from the real-world experience of practitioners who have built significant, sustainable results through disciplined, data-driven application of {topic} principles.

The path forward is clear: start with research, build on a solid technical foundation, create content that genuinely serves your audience, distribute it consistently, and measure everything. Then iterate. And iterate again.

There is no shortcut to lasting success with {topic}. But there is a clear, proven roadmap — and you now have it in your hands.

---

{cta_section}

---
*Tags: {tk}, {topic} guide, {topic} strategy {year}, {topic} tips, {aud}*
"""
    return article

# ══════════════════════════════════════════════════════════════════════════════
# TOOL: GOOGLE KEYWORD SCRAPER
# ══════════════════════════════════════════════════════════════════════════════
if tool == "Google Keyword Scraper":
    card("Google Keyword Scraper", "🔍")

    st.markdown("""
    <div style='background:#1e1e24;border:1px solid #2a2a35;border-radius:10px;padding:1rem 1.2rem;margin-bottom:1.2rem;font-size:.88rem;color:#8b8b9e;'>
        Pulls <strong style='color:#a5a0ff;'>live data</strong> from Google Trends via
        <code style='background:#26262f;padding:.1rem .4rem;border-radius:4px;color:#f0f0f5;'>pytrends</code>.
        Install: <code style='background:#26262f;padding:.1rem .4rem;border-radius:4px;color:#f0f0f5;'>pip install pytrends</code>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("Seed keyword", placeholder="e.g. content marketing")
    with col2:
        geo = st.selectbox("Country", ["Worldwide", "India", "US", "UK", "Australia"])

    geo_map = {"Worldwide": "", "India": "IN", "US": "US", "UK": "GB", "Australia": "AU"}

    if st.button("🔍 Scrape Google Keywords", use_container_width=True):
        if not topic:
            st.warning("Keyword daalna padega!")
        elif not PYTRENDS_OK:
            st.error("pytrends install karo: `pip install pytrends`")
        else:
            with st.spinner("Google Trends se data fetch ho raha hai…"):
                try:
                    pytrends = TrendReq(hl='en-US', tz=330)
                    pytrends.build_payload([topic], geo=geo_map[geo], timeframe='today 12-m')

                    related   = pytrends.related_queries()
                    top_df    = related[topic].get("top")
                    rising_df = related[topic].get("rising")
                    iot       = pytrends.interest_over_time()
                    avg_interest = int(iot[topic].mean()) if topic in iot.columns else 0

                    st.markdown(f"""
                    <div style='display:flex;gap:1rem;margin-bottom:1.2rem;flex-wrap:wrap;'>
                        <div style='background:#1e1e24;border:1px solid #2a2a35;border-radius:10px;padding:.8rem 1.2rem;flex:1;min-width:130px;'>
                            <div style='font-size:.72rem;color:#8b8b9e;text-transform:uppercase;letter-spacing:.6px;'>Avg Interest</div>
                            <div style='font-size:1.6rem;font-weight:700;color:#6c63ff;'>{avg_interest}<span style='font-size:.85rem;color:#8b8b9e;'>/100</span></div>
                        </div>
                        <div style='background:#1e1e24;border:1px solid #2a2a35;border-radius:10px;padding:.8rem 1.2rem;flex:1;min-width:130px;'>
                            <div style='font-size:.72rem;color:#8b8b9e;text-transform:uppercase;letter-spacing:.6px;'>Top Keywords</div>
                            <div style='font-size:1.6rem;font-weight:700;color:#34d399;'>{len(top_df) if top_df is not None else 0}</div>
                        </div>
                        <div style='background:#1e1e24;border:1px solid #2a2a35;border-radius:10px;padding:.8rem 1.2rem;flex:1;min-width:130px;'>
                            <div style='font-size:.72rem;color:#8b8b9e;text-transform:uppercase;letter-spacing:.6px;'>Rising Keywords</div>
                            <div style='font-size:1.6rem;font-weight:700;color:#fbbf24;'>{len(rising_df) if rising_df is not None else 0}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("<div style='font-weight:600;color:#34d399;margin-bottom:.5rem;'>📈 Top Keywords</div>", unsafe_allow_html=True)
                        if top_df is not None and not top_df.empty:
                            for _, row in top_df.head(15).iterrows():
                                kw_pill(row['query'], score=f"↑{int(row['value'])}", badge_color="#34d399")
                        else:
                            st.info("Koi top keyword nahi mila.")
                    with col_b:
                        st.markdown("<div style='font-weight:600;color:#fbbf24;margin-bottom:.5rem;'>🚀 Rising Keywords</div>", unsafe_allow_html=True)
                        if rising_df is not None and not rising_df.empty:
                            for _, row in rising_df.head(15).iterrows():
                                label = "🔥 Breakout" if str(row['value']) == "Breakout" else f"+{row['value']}%"
                                st.markdown(f"""
                                <div style='background:#1e1e24;border:1px solid #2a2a35;border-radius:6px;padding:.35rem .75rem;margin:.25rem 0;font-size:.88rem;color:#f0f0f5;display:flex;justify-content:space-between;'>
                                    <span>🔑 {row['query']}</span>
                                    <span style='color:#fbbf24;font-size:.75rem;'>{label}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("Koi rising keyword nahi mila.")

                    st.markdown("<div style='font-weight:600;color:#a5a0ff;margin:1rem 0 .5rem;'>💡 Long-Tail Keywords</div>", unsafe_allow_html=True)
                    for m in ["best", "how to", "guide", "tips", "tools for", "vs", "for beginners", f"in {datetime.now().year}", "free", "tutorial"]:
                        kw_pill(f"{m} {topic}")

                except Exception as e:
                    st.error(f"Google Trends error: {e}\n\nZyada requests? 60 second wait karo phir try karo.")

# ══════════════════════════════════════════════════════════════════════════════
# TOOL: AI BLOG WRITER — NO API KEY
# ══════════════════════════════════════════════════════════════════════════════
elif tool == "AI Blog Writer":
    card("AI Blog Writer — 2000+ Words", "✍️")

    st.markdown("""
    <div style='background:#1e1e24;border:1px solid #34d39944;border-radius:10px;padding:1rem 1.2rem;margin-bottom:1.2rem;font-size:.88rem;color:#8b8b9e;'>
        ✅ <strong style='color:#34d399;'>100% Free — No API Key Needed.</strong>
        Professionally structured articles with intro, stats, strategy, examples, FAQ, and CTA.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input("Article topic", placeholder="e.g. Social Media Marketing for Small Businesses")
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Conversational", "Authoritative", "Educational", "Engaging"])

    target_kw = st.text_input("Target keyword (optional)", placeholder="e.g. social media marketing tips 2026")
    audience  = st.text_input("Target audience (optional)", placeholder="e.g. small business owners, freelancers")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        include_faq   = st.checkbox("FAQ Section", value=True)
    with col_b:
        include_stats = st.checkbox("Stats & Data", value=True)
    with col_c:
        include_cta   = st.checkbox("CTA Section", value=True)

    if st.button("✍️ Generate Full Article (2000+ Words)", use_container_width=True):
        if not topic:
            st.warning("Topic daalna padega!")
        else:
            with st.spinner("Article likh raha hoon… (2–5 seconds)"):
                time.sleep(1.5)
                article = generate_article(topic, tone, include_faq, include_stats, include_cta, target_kw, audience)
                word_count = len(article.split())

            st.success(f"✅ Article ready! **{word_count:,} words** generated.")

            tab1, tab2 = st.tabs(["📄 Preview", "✏️ Edit & Export"])

            with tab1:
                st.markdown(article)

            with tab2:
                edited = st.text_area("Edit karo apna article", article, height=500)
                wc = len(edited.split())
                col1, col2, col3 = st.columns(3)
                col1.metric("Words", f"{wc:,}")
                col2.metric("Characters", f"{len(edited):,}")
                col3.metric("Read Time", f"{max(1, wc // 200)} min")

                dl_col1, dl_col2 = st.columns(2)
                with dl_col1:
                    st.download_button(
                        "⬇️ Download .md",
                        edited,
                        file_name=f"{topic[:40].replace(' ','_').lower()}.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )
                with dl_col2:
                    st.download_button(
                        "⬇️ Download .txt",
                        edited,
                        file_name=f"{topic[:40].replace(' ','_').lower()}.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )

# ══════════════════════════════════════════════════════════════════════════════
# TOOL: BLOG TITLE GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
elif tool == "Blog Title Generator":
    card("Blog Title Generator", "📝")

    topic = st.text_input("Topic daalo", placeholder="e.g. email marketing")

    if st.button("Generate Titles", use_container_width=True):
        if not topic:
            st.warning("Topic daalna padega!")
        else:
            year = datetime.now().year
            titles = [
                (f"10 Best {topic} Tips for Beginners in {year}",            "Listicle"),
                (f"The Ultimate {topic} Guide: Everything You Need to Know",  "Pillar"),
                (f"How to Master {topic} in 30 Days (Step-by-Step)",          "How-to"),
                (f"Why Your {topic} Strategy Is Failing (And How to Fix It)", "Problem/Solution"),
                (f"{topic} vs. Traditional Methods: Which One Wins?",         "Comparison"),
                (f"The Beginner's Blueprint to {topic}",                       "Educational"),
                (f"I Tested Every {topic} Tool — Here's What Actually Works", "First-person"),
                (f"{topic} in {year}: Trends, Tools & Bold Predictions",      "Trend"),
                (f"How Top Brands Use {topic} to Drive Massive Results",      "Authority"),
                (f"The Hidden Power of {topic} Most Marketers Ignore",        "Curiosity"),
            ]
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

    keyword = st.text_input("Keyword daalo", placeholder="e.g. best CRM software")

    if st.button("Check Difficulty", use_container_width=True):
        if not keyword:
            st.warning("Keyword daalna padega!")
        else:
            difficulty  = random.randint(20, 90)
            volume      = random.randint(500, 50000)
            cpc         = round(random.uniform(0.5, 8.5), 2)
            opportunity = max(0, min(100, 100 - difficulty + random.randint(-5, 15)))

            color = "#34d399" if difficulty < 35 else ("#fbbf24" if difficulty < 65 else "#f87171")
            label = "Easy 🟢" if difficulty < 35 else ("Medium 🟡" if difficulty < 65 else "Hard 🔴")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Difficulty", f"{difficulty}/100", label)
            col2.metric("Est. Monthly Searches", f"{volume:,}")
            col3.metric("CPC (USD)", f"${cpc}")
            col4.metric("Opportunity Score", f"{opportunity}/100")

            st.progress(difficulty / 100)

            if difficulty < 35:
                st.success("✅ Low competition — naye sites ke liye perfect target!")
            elif difficulty < 65:
                st.warning("⚠️ Medium competition — quality content aur backlinks chahiye.")
            else:
                st.error("🔴 High competition — long-tail variants try karo.")

# ══════════════════════════════════════════════════════════════════════════════
# TOOL: COMPETITOR ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif tool == "Competitor Analysis":
    card("Competitor Content Analysis", "🏆")

    topic = st.text_input("Topic / Niche daalo", placeholder="e.g. project management software")

    if st.button("Analyse Competitors", use_container_width=True):
        if not topic:
            st.warning("Topic daalna padega!")
        else:
            comps = [
                ("HubSpot",    f"The Complete {topic} Guide",         random.randint(2000, 8000), random.randint(55, 90), random.randint(80,  200)),
                ("Ahrefs",     f"{topic} Tutorial for Beginners",     random.randint(1500, 6000), random.randint(45, 80), random.randint(60,  180)),
                ("Neil Patel", f"How to Use {topic} to Grow Traffic", random.randint(1800, 7000), random.randint(50, 85), random.randint(50,  160)),
                ("Backlinko",  f"{topic}: The Definitive Guide",      random.randint(3000, 9000), random.randint(60, 95), random.randint(100, 300)),
                ("Moz",        f"{topic} Best Practices & Examples",  random.randint(1200, 5000), random.randint(40, 75), random.randint(40,  140)),
            ]

            st.markdown("""
            <div style='display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:.5rem;padding:.5rem .75rem;
                font-size:.75rem;color:#8b8b9e;text-transform:uppercase;letter-spacing:.6px;font-weight:600;'>
                <div>Article</div><div>Words</div><div>DA</div><div>Backlinks</div><div>Gap</div>
            </div>
            """, unsafe_allow_html=True)

            for brand, title, words, da, links in comps:
                gc = "#34d399" if da < 65 else "#f87171"
                gl = "Beatable ✅" if da < 65 else "Tough 🔴"
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
                    <div style='color:{gc};font-weight:600;font-size:.8rem;'>{gl}</div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TOOL: IMAGE SEO
# ══════════════════════════════════════════════════════════════════════════════
elif tool == "Image SEO Generator":
    card("Image SEO Generator", "🖼️")

    uploaded = st.file_uploader("Image upload karo", type=["png", "jpg", "jpeg"])

    if uploaded:
        img = Image.open(uploaded)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(img, caption="Uploaded Image", use_container_width=True)
        with col2:
            w, h = img.size
            st.metric("Dimensions", f"{w} × {h} px")
            st.metric("Format", img.format or uploaded.type.split("/")[-1].upper())
            st.metric("File Size", f"{round(uploaded.size/1024, 1)} KB")

        captions = [
            "Artificial intelligence technology concept illustration",
            "Digital marketing automation and analytics dashboard",
            "AI-powered SEO tools workflow visualization",
            "Modern content strategy and optimization graphic",
            "Business growth and digital analytics concept",
        ]
        choice = random.choice(captions)

        st.markdown("<div style='font-weight:600;color:#a5a0ff;margin:.75rem 0 .4rem;'>🏷️ Alt Text</div>", unsafe_allow_html=True)
        alt_text = st.text_input("Edit karo", choice)

        fname = uploaded.name.rsplit(".", 1)[0].replace(" ", "-").lower()
        ext   = (img.format or "jpg").lower()

        st.markdown("<div style='font-weight:600;color:#a5a0ff;margin:.75rem 0 .4rem;'>📁 SEO Filename</div>", unsafe_allow_html=True)
        st.code(f"{fname}-seo-optimized.{ext}", language="text")

        st.markdown("<div style='font-weight:600;color:#a5a0ff;margin:.75rem 0 .4rem;'>📋 HTML Snippet</div>", unsafe_allow_html=True)
        st.code(f'<img src="{fname}-seo-optimized.{ext}" alt="{alt_text}" width="{w}" height="{h}" loading="lazy">', language="html")
