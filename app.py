import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, quote_plus
import whois
from datetime import datetime, date
import re
import socket
import ssl
import json
import random

st.set_page_config(page_title="Free SEO Tool Box", page_icon="🚀", layout="wide")

# =========================
# STYLES
# =========================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0f13 0%, #161622 100%);
        color: white;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121a 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(245,197,66,0.15);
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #f5c542 !important;
        font-weight: 700;
        font-size: 14px;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(245,197,66,0.25) !important;
        border-radius: 12px !important;
    }
    [data-testid="stSidebar"] .stSelectbox span {
        color: #f5c542 !important;
        font-weight: 600;
    }
    .sidebar-title {
        font-size: 20px;
        font-weight: 800;
        color: #f5c542;
        text-align: center;
        margin-bottom: 4px;
    }
    .sidebar-subtitle {
        font-size: 12px;
        color: #888;
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar-divider {
        height: 1px;
        background: rgba(245,197,66,0.15);
        margin: 16px 0;
    }
    .sidebar-info {
        background: rgba(245,197,66,0.06);
        border: 1px solid rgba(245,197,66,0.12);
        border-radius: 12px;
        padding: 14px;
        margin-top: 16px;
    }
    .sidebar-info-title {
        font-size: 13px;
        font-weight: 700;
        color: #f5c542;
        margin-bottom: 8px;
    }
    .sidebar-info-text {
        font-size: 11px;
        color: #999;
        line-height: 1.6;
    }
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #f5c542;
        margin-bottom: 8px;
    }
    .sub-title {
        font-size: 17px;
        color: #cfcfcf;
        margin-bottom: 24px;
    }
    .box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(245,197,66,0.18);
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
    }
    .metric-label {
        color: #bbbbbb;
        font-size: 14px;
    }
    .metric-value {
        color: #f5c542;
        font-size: 34px;
        font-weight: 800;
    }
    .small {
        color: #aaaaaa;
        font-size: 13px;
    }
    .tab-title {
        font-size: 22px;
        font-weight: 700;
        color: #f5c542;
        margin-bottom: 12px;
    }
    .kw-box {
        background: rgba(245,197,66,0.06);
        border: 1px solid rgba(245,197,66,0.15);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .kw-text {
        color: #e0e0e0;
        font-size: 15px;
    }
    .kw-badge {
        background: rgba(245,197,66,0.2);
        color: #f5c542;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .article-output {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 24px;
        line-height: 1.8;
        color: #d4d4d4;
        font-size: 16px;
    }
    .article-output h2 {
        color: #f5c542;
        font-size: 22px;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .article-output h3 {
        color: #e0e0e0;
        font-size: 18px;
        margin-top: 16px;
        margin-bottom: 8px;
    }
    .article-output p {
        margin-bottom: 12px;
    }
    .article-output ul {
        margin-left: 20px;
        margin-bottom: 12px;
    }
    .article-output li {
        margin-bottom: 6px;
    }
    .sidebar-icon-row {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(255,255,255,0.03);
        margin-bottom: 6px;
        font-size: 14px;
        color: #ccc;
    }
    .sidebar-icon-row .icon {
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🚀 SEO Tool Box</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Free Tools — No Limits</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    page = st.selectbox(
        "Navigate To",
        [
            "📈 DA PA Checker",
            "🔍 Keyword Research",
            "✍️ Article Writer"
        ],
        label_visibility="visible"
    )
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="sidebar-icon-row"><span class="icon">📈</span> DA/PA Checker — Free</div>
    <div class="sidebar-icon-row"><span class="icon">🔍</span> Keyword Research — Free</div>
    <div class="sidebar-icon-row"><span class="icon">✍️</span> Article Writer — Free</div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-info-title">ℹ️ About This Tool</div>', unsafe_allow_html=True)
    st.markdown('''<div class="sidebar-info-text">
    ✅ No API key needed for DA PA & Keywords<br>
    ✅ No signup required<br>
    ✅ 100% free forever<br>
    ✅ OpenAI optional for articles
    </div>''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-info-title">⚠️ Disclaimer</div>', unsafe_allow_html=True)
    st.markdown('''<div class="sidebar-info-text">
    DA/PA are estimated scores, not official Moz metrics. Volume & Difficulty are approximations.
    </div>''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# HELPERS - DA PA
# =========================
def normalize_url(url):
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url

def get_domain(url):
    parsed = urlparse(url)
    return parsed.netloc.replace("www.", "")

def safe_get(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        return r
    except Exception:
        return None

def extract_whois_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if not creation_date:
            return None, None
        today = datetime.now()
        age_days = (today - creation_date).days
        age_years = round(age_days / 365.25, 2)
        return creation_date, age_years
    except Exception:
        return None, None

def check_ssl(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain):
                return True
    except Exception:
        return False

def analyze_page(url):
    result = {
        "status_code": None,
        "title": "",
        "meta_description": "",
        "h1_count": 0,
        "h2_count": 0,
        "word_count": 0,
        "internal_links": 0,
        "external_links": 0,
        "images": 0,
        "images_missing_alt": 0,
        "canonical": False,
        "robots_meta": False,
        "https": url.startswith("https://"),
        "response_time": None,
    }
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        start = datetime.now()
        r = requests.get(url, headers=headers, timeout=15)
        end = datetime.now()
        result["response_time"] = round((end - start).total_seconds(), 2)
        result["status_code"] = r.status_code
        if r.status_code != 200:
            return result
        soup = BeautifulSoup(r.text, "html.parser")
        if soup.title and soup.title.text:
            result["title"] = soup.title.text.strip()
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            result["meta_description"] = meta_desc.get("content").strip()
        result["h1_count"] = len(soup.find_all("h1"))
        result["h2_count"] = len(soup.find_all("h2"))
        text = soup.get_text(" ", strip=True)
        words = re.findall(r"\w+", text)
        result["word_count"] = len(words)
        canonical = soup.find("link", attrs={"rel": "canonical"})
        result["canonical"] = canonical is not None
        robots_meta = soup.find("meta", attrs={"name": re.compile("^robots$", re.I)})
        result["robots_meta"] = robots_meta is not None
        domain = get_domain(url)
        links = soup.find_all("a", href=True)
        internal = 0
        external = 0
        for link in links:
            href = link["href"].strip()
            full = urljoin(url, href)
            parsed = urlparse(full)
            link_domain = parsed.netloc.replace("www.", "")
            if not parsed.netloc or link_domain == domain:
                internal += 1
            else:
                external += 1
        result["internal_links"] = internal
        result["external_links"] = external
        imgs = soup.find_all("img")
        result["images"] = len(imgs)
        missing_alt = 0
        for img in imgs:
            if not img.get("alt") or not img.get("alt").strip():
                missing_alt += 1
        result["images_missing_alt"] = missing_alt
        return result
    except Exception:
        return result

def calculate_da(domain_age, ssl_ok, page_data, domain):
    score = 0
    if domain_age:
        if domain_age >= 10:
            score += 25
        elif domain_age >= 5:
            score += 18
        elif domain_age >= 2:
            score += 12
        else:
            score += 6
    if ssl_ok:
        score += 10
    if len(domain) < 20:
        score += 5
    if "-" not in domain:
        score += 5
    if page_data["status_code"] == 200:
        score += 10
    if page_data["title"]:
        score += 5
    if page_data["meta_description"]:
        score += 5
    if page_data["canonical"]:
        score += 5
    if page_data["robots_meta"]:
        score += 2
    if page_data["internal_links"] >= 10:
        score += 8
    elif page_data["internal_links"] >= 5:
        score += 5
    if page_data["external_links"] >= 2:
        score += 3
    if page_data["word_count"] >= 1500:
        score += 7
    elif page_data["word_count"] >= 800:
        score += 5
    elif page_data["word_count"] >= 300:
        score += 3
    return min(score, 100)

def calculate_pa(page_data):
    score = 0
    if page_data["status_code"] == 200:
        score += 15
    if page_data["title"]:
        score += 10
    if page_data["meta_description"]:
        score += 8
    if page_data["h1_count"] == 1:
        score += 10
    elif page_data["h1_count"] > 1:
        score += 5
    if page_data["h2_count"] >= 3:
        score += 10
    elif page_data["h2_count"] >= 1:
        score += 5
    if page_data["word_count"] >= 2000:
        score += 20
    elif page_data["word_count"] >= 1200:
        score += 15
    elif page_data["word_count"] >= 600:
        score += 10
    elif page_data["word_count"] >= 300:
        score += 5
    if page_data["internal_links"] >= 10:
        score += 10
    elif page_data["internal_links"] >= 5:
        score += 6
    if page_data["external_links"] >= 3:
        score += 5
    if page_data["images"] > 0:
        good_alt_ratio = 1
        if page_data["images"] > 0:
            good_alt_ratio = (page_data["images"] - page_data["images_missing_alt"]) / page_data["images"]
        if good_alt_ratio >= 0.8:
            score += 7
        elif good_alt_ratio >= 0.5:
            score += 4
    if page_data["canonical"]:
        score += 5
    return min(score, 100)

def score_label(score):
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Strong"
    elif score >= 40:
        return "Average"
    elif score >= 20:
        return "Weak"
    return "Poor"

# =========================
# HELPERS - KEYWORD RESEARCH
# =========================
def get_google_suggestions(keyword):
    suggestions = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36"
        }
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={quote_plus(keyword)}"
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            suggestions = data[1] if len(data) > 1 else []
    except Exception:
        pass
    return suggestions

def get_related_searches(keyword):
    related = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36"
        }
        url = f"https://www.google.com/search?q={quote_plus(keyword)}&hl=en"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            divs = soup.find_all("div", class_="wCb7ib")
            for div in divs:
                text = div.get_text(strip=True)
                if text and text not in related:
                    related.append(text)
            spans = soup.find_all("div", attrs={"class": re.compile("related-question-pair")})
            for span in spans:
                text = span.get_text(strip=True)
                if text and text not in related:
                    related.append(text)
    except Exception:
        pass
    return related

def get_people_also_ask(keyword):
    questions = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36"
        }
        url = f"https://www.google.com/search?q={quote_plus(keyword)}&hl=en"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            divs = soup.find_all("div", attrs={"class": re.compile("related-question-pair")})
            for div in divs:
                text = div.get_text(strip=True)
                if text and text not in questions:
                    questions.append(text)
    except Exception:
        pass
    return questions

def get_long_tail_variations(keyword):
    prefixes = [
        "how to", "best way to", "why", "what is", "top 10",
        "guide to", "tips for", "benefits of", "vs", "review",
        "in 2024", "for beginners", "without", "at home", "near me",
        "free", "cheap", "online", "step by step", "tutorial"
    ]
    suffixes = [
        "guide", "tutorial", "tips", "tricks", "examples",
        "for beginners", "step by step", "in hindi", "in 2024",
        "without investment", "at home", "online", "free"
    ]
    variations = set()
    for prefix in prefixes:
        variations.add(f"{prefix} {keyword}")
    for suffix in suffixes:
        variations.add(f"{keyword} {suffix}")
    return list(variations)

def estimate_difficulty(keyword):
    words = keyword.split()
    word_count = len(words)
    difficulty = 30
    if word_count == 1:
        difficulty += 40
    elif word_count == 2:
        difficulty += 25
    elif word_count == 3:
        difficulty += 10
    else:
        difficulty -= 10
    commercial_words = ["buy", "price", "cost", "cheap", "best", "review", "discount", "offer", "deal"]
    for word in commercial_words:
        if word in keyword.lower():
            difficulty += 10
            break
    info_words = ["how", "what", "why", "guide", "tutorial", "learn"]
    for word in info_words:
        if word in keyword.lower():
            difficulty -= 10
            break
    return max(5, min(difficulty, 95))

def difficulty_label(score):
    if score >= 70:
        return "Hard", "#ff4444"
    elif score >= 45:
        return "Medium", "#ffaa00"
    else:
        return "Easy", "#44ff44"

def estimate_volume(keyword):
    words = keyword.split()
    base = 1000
    if len(words) == 1:
        base = 20000
    elif len(words) == 2:
        base = 5000
    elif len(words) == 3:
        base = 1500
    elif len(words) == 4:
        base = 500
    else:
        base = 150
    variation = random.uniform(0.6, 1.4)
    return int(base * variation)

# =========================
# HELPERS - ARTICLE WRITER
# =========================
def generate_article_openai(keyword, tone, length, api_key, extra=""):
    try:
        import openai
        openai.api_key = api_key
        length_map = {
            "Short (500 words)": 500,
            "Medium (1000 words)": 1000,
            "Long (2000 words)": 2000,
            "Very Long (3000+ words)": 3000
        }
        word_target = length_map.get(length, 1000)
        
        extra_text = f"\n\nAdditional instructions: {extra}" if extra.strip() else ""
        
        prompt = f"""Write a high-quality, SEO-optimized article about "{keyword}".

Requirements:
- Tone: {tone}
- Target length: approximately {word_target} words
- Include an engaging title
- Write a compelling introduction
- Use H2 and H3 headings for structure
- Include bullet points where appropriate
- Write in a natural, readable style
- End with a conclusion and call-to-action
- Format in clean HTML (use h2, h3, p, ul, li, strong tags)
{extra_text}

Do NOT include ```html or ``` tags. Just output the HTML directly."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert SEO content writer who creates engaging, well-structured articles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def generate_article_template(keyword, tone, length, extra=""):
    clean_keyword = keyword.title().strip()
    tone_map = {
        "Professional": "professional",
        "Casual": "friendly and casual",
        "Informative": "informative and educational",
        "Persuasive": "persuasive and convincing",
        "Storytelling": "storytelling and engaging"
    }
    tone_style = tone_map.get(tone, "professional")
    length_sections = {
        "Short (500 words)": 3,
        "Medium (1000 words)": 5,
        "Long (2000 words)": 8,
        "Very Long (3000+ words)": 12
    }
    num_sections = length_sections.get(length, 5)
    
    section_templates = {
        "Professional": [
            f"Understanding the Fundamentals of {clean_keyword}",
            f"Key Benefits of {clean_keyword}",
            f"Best Practices for {clean_keyword}",
            f"Common Mistakes to Avoid",
            f"How to Implement {clean_keyword} Effectively",
            f"Measuring Success with {clean_keyword}",
            f"Advanced Strategies for {clean_keyword}",
            f"Future Trends in {clean_keyword}",
            f"Case Studies: {clean_keyword} in Action",
            f"Tools and Resources for {clean_keyword}",
            f"Expert Insights on {clean_keyword}",
            f"Conclusion and Next Steps"
        ],
        "Casual": [
            f"So What Exactly is {clean_keyword}?",
            f"Why Should You Care About {clean_keyword}?",
            f"The Cool Things {clean_keyword} Can Do",
            f"Let's Talk About the Benefits",
            f"How to Get Started with {clean_keyword}",
            f"Some Pro Tips You'll Love",
            f"Mistakes I Made (So You Don't Have To)",
            f"Real Stories About {clean_keyword}",
            f"Quick Wins with {clean_keyword}",
            f"Where to Learn More",
            f"Final Thoughts",
            f"Now Go Try It Yourself!"
        ],
        "Informative": [
            f"What is {clean_keyword}? A Complete Explanation",
            f"The History and Evolution of {clean_keyword}",
            f"How {clean_keyword} Works: The Science Behind It",
            f"Key Components of {clean_keyword}",
            f"Statistics and Data on {clean_keyword}",
            f"Benefits Backed by Research",
            f"Step-by-Step Guide to {clean_keyword}",
            f"Common Myths About {clean_keyword}",
            f"Expert Opinions on {clean_keyword}",
            f"Resources for Deep Learning",
            f"Frequently Asked Questions",
            f"Summary and Key Takeaways"
        ],
        "Persuasive": [
            f"Why {clean_keyword} is a Game-Changer",
            f"The Problem You're Facing Right Now",
            f"How {clean_keyword} Solves Your Problem",
            f"Proof That {clean_keyword} Works",
            f"What Others Are Saying About {clean_keyword}",
            f"The Cost of NOT Using {clean_keyword}",
            f"How to Get the Best Results",
            f"Exclusive Tips for Maximum Impact",
            f"Success Stories That Inspire",
            f"Why Now is the Perfect Time",
            f"Your Action Plan Starts Here",
            f"Take the First Step Today"
        ],
        "Storytelling": [
            f"My Journey with {clean_keyword}",
            f"How I Discovered {clean_keyword}",
            f"The Turning Point",
            f"Lessons Learned Along the Way",
            f"The Challenges I Faced",
            f"Breakthrough Moments",
            f"What I Wish I Knew Earlier",
            f"The People Who Helped Me",
            f"Milestones and Achievements",
            f"Unexpected Discoveries",
            f"Looking Back and Looking Forward",
            f"Your Story Starts Now"
        ]
    }
    
    sections = section_templates.get(tone, section_templates["Professional"])[:num_sections]
    
    content_templates = {
        "Professional": [
            f"<p>In today's competitive landscape, understanding {clean_keyword} has become essential for professionals and businesses alike. This section explores the foundational concepts that form the backbone of {clean_keyword} and why it matters now more than ever.</p><p>{clean_keyword} represents a significant shift in how we approach [relevant field]. Organizations that have embraced this concept have seen measurable improvements in their outcomes.</p>",
            f"<p>When implemented correctly, {clean_keyword} offers numerous advantages that can transform your approach. Let's examine the most significant benefits:</p><ul><li><strong>Increased Efficiency:</strong> Streamlined processes lead to better resource utilization</li><li><strong>Cost Reduction:</strong> Optimized workflows reduce unnecessary expenses</li><li><strong>Improved Outcomes:</strong> Data-driven decisions yield superior results</li><li><strong>Competitive Advantage:</strong> Early adopters gain significant market positioning</li><li><strong>Scalability:</strong> Proven frameworks allow for sustainable growth</li></ul>",
            f"<p>Successful implementation of {clean_keyword} requires adherence to established best practices:</p><ul><li>Start with a clear strategy and defined objectives</li><li>Gather and analyze relevant data before making decisions</li><li>Implement changes incrementally with proper testing</li><li>Monitor performance metrics continuously</li><li>Iterate and optimize based on results</li><li>Document learnings for future reference</li></ul>",
            f"<p>While pursuing {clean_keyword}, many practitioners fall into common pitfalls. Being aware of these can save significant time and resources:</p><ul><li><strong>Skip Research:</strong> Not investing time in understanding the fundamentals</li><li><strong>Rush Implementation:</strong> Moving too quickly without proper planning</li><li><strong>Ignore Data:</strong> Making decisions based on assumptions rather than evidence</li><li><strong>Neglect Training:</strong> Failing to equip team members with necessary skills</li><li><strong>Set Unrealistic Goals:</strong> Expecting overnight transformation</li></ul>",
            f"<p>Implementing {clean_keyword} effectively requires a structured approach. Here's a proven framework:</p><ul><li><strong>Phase 1 - Assessment:</strong> Evaluate current state and identify gaps</li><li><strong>Phase 2 - Planning:</strong> Develop a detailed implementation roadmap</li><li><strong>Phase 3 - Execution:</strong> Implement changes according to plan</li><li><strong>Phase 4 - Monitoring:</strong> Track progress against defined KPIs</li><li><strong>Phase 5 - Optimization:</strong> Refine approach based on insights</li></ul>",
        ]
    }
    
    article_html = f'<h2>{clean_keyword}: The Complete Guide You Need</h2>'
    
    article_html += f'''<p>Are you looking to understand {clean_keyword} and how it can benefit you? You've come to the right place. In this comprehensive guide, we'll explore everything you need to know about {clean_keyword}, from the basics to advanced strategies.</p><p>Whether you're a beginner just starting out or an experienced professional looking to deepen your knowledge, this article will provide valuable insights that you can apply immediately.</p>'''
    
    if extra.strip():
        article_html += f"<p><em>Note: {extra}</em></p>"
    
    for i, section in enumerate(sections):
        article_html += f'\n<h3>{section}</h3>'
        if i < len(content_templates.get(tone, [])):
            article_html += content_templates[tone][i]
        else:
            article_html += f'''<p>When it comes to {clean_keyword}, there are several important factors to consider. Understanding these elements will help you make better decisions and achieve superior outcomes.</p><p>Many experts in the field recommend taking a systematic approach to {clean_keyword}. This means breaking down complex concepts into manageable pieces and addressing them one at a time.</p><ul><li>Focus on understanding the core principles first</li><li>Apply what you learn through practical exercises</li><li>Seek feedback from experienced practitioners</li><li>Stay updated with the latest developments</li><li>Continuously refine your approach</li></ul>'''
    
    article_html += f'''
<h3>Conclusion</h3>
<p>{clean_keyword} is a powerful concept that, when understood and applied correctly, can yield significant benefits. The key is to start with a solid foundation, follow proven methodologies, and continuously improve based on results.</p>
<p>We hope this guide has provided you with valuable insights into {clean_keyword}. Remember, the journey of mastery is ongoing, and every step you take brings you closer to your goals.</p>
<p><strong>Ready to get started with {clean_keyword}?</strong> Begin by implementing the strategies discussed in this article, and don't hesitate to seek additional resources and support as needed.</p>'''
    
    return article_html

def count_words(html_content):
    text = re.sub(r'<[^>]+>', ' ', html_content)
    words = re.findall(r'\w+', text)
    return len(words)

# =========================
# PAGE TITLE DYNAMIC
# =========================
if "DA PA" in page:
    page_title = "📈 DA PA Checker"
    page_desc = "No API key. No paid Moz nonsense. Estimated DA / PA based on real on-page and domain signals."
elif "Keyword" in page:
    page_title = "🔍 Keyword Research"
    page_desc = "Google Autocomplete, Related Searches, Long-tail variations — all free, no API needed."
else:
    page_title = "✍️ Article Writer"
    page_desc = "Generate SEO-optimized articles with or without OpenAI API."

st.markdown(f'<div class="main-title">{page_title}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">{page_desc}</div>', unsafe_allow_html=True)

# =========================
# PAGE 1: DA PA CHECKER
# =========================
if "DA PA" in page:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        url = st.text_input("Enter Website URL", placeholder="example.com or https://example.com", key="da_url")
        run = st.button("Check DA PA", use_container_width=True, key="da_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    if run:
        if not url.strip():
            st.error("URL daalo.")
            st.stop()

        url = normalize_url(url)
        domain = get_domain(url)

        with st.spinner("Analyzing domain and page..."):
            creation_date, domain_age = extract_whois_age(domain)
            ssl_ok = check_ssl(domain)
            page_data = analyze_page(url)
            da_score = calculate_da(domain_age, ssl_ok, page_data, domain)
            pa_score = calculate_pa(page_data)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">DA Score (Estimated)</div>
                <div class="metric-value">{da_score}</div>
                <div class="small">{score_label(da_score)}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">PA Score (Estimated)</div>
                <div class="metric-value">{pa_score}</div>
                <div class="small">{score_label(pa_score)}</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            age_text = f"{domain_age} years" if domain_age else "Not found"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Domain Age</div>
                <div class="metric-value" style="font-size:26px;">{age_text}</div>
                <div class="small">{creation_date.strftime("%Y-%m-%d") if creation_date else "WHOIS unavailable"}</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">HTTP Status</div>
                <div class="metric-value">{page_data["status_code"] if page_data["status_code"] else "-"}</div>
                <div class="small">SSL: {"Yes" if ssl_ok else "No"}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### Detailed SEO Signals")
        d1, d2 = st.columns(2)

        with d1:
            st.markdown('<div class="box">', unsafe_allow_html=True)
            st.write(f"**Title Present:** {'Yes' if page_data['title'] else 'No'}")
            st.write(f"**Meta Description:** {'Yes' if page_data['meta_description'] else 'No'}")
            st.write(f"**Canonical Tag:** {'Yes' if page_data['canonical'] else 'No'}")
            st.write(f"**Robots Meta Tag:** {'Yes' if page_data['robots_meta'] else 'No'}")
            st.write(f"**H1 Count:** {page_data['h1_count']}")
            st.write(f"**H2 Count:** {page_data['h2_count']}")
            st.write(f"**Word Count:** {page_data['word_count']}")
            st.markdown('</div>', unsafe_allow_html=True)

        with d2:
            st.markdown('<div class="box">', unsafe_allow_html=True)
            st.write(f"**Internal Links:** {page_data['internal_links']}")
            st.write(f"**External Links:** {page_data['external_links']}")
            st.write(f"**Images:** {page_data['images']}")
            st.write(f"**Images Missing Alt:** {page_data['images_missing_alt']}")
            st.write(f"**HTTPS:** {'Yes' if page_data['https'] else 'No'}")
            st.write(f"**Response Time:** {page_data['response_time']} sec" if page_data['response_time'] else "**Response Time:** -")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### Quick Verdict")
        if da_score >= 70 and pa_score >= 70:
            st.success("Strong website. Good authority and solid page-level optimization.")
        elif da_score >= 50 or pa_score >= 50:
            st.info("Decent site. Has some strength, but still room for SEO improvement.")
        else:
            st.warning("Low authority estimate. Improve content depth, technical SEO, internal linking, and trust signals.")

# =========================
# PAGE 2: KEYWORD RESEARCH
# =========================
elif "Keyword" in page:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        kw_input = st.text_input("Enter Seed Keyword", placeholder="e.g., best laptops 2024", key="kw_input")
        
        col_a, col_b = st.columns(2)
        with col_a:
            get_suggestions = st.checkbox("Google Suggestions", value=True, key="chk_suggest")
            get_related = st.checkbox("Related Searches", value=True, key="chk_related")
        with col_b:
            get_paa = st.checkbox("People Also Ask", value=True, key="chk_paa")
            get_longtail = st.checkbox("Long-tail Variations", value=True, key="chk_longtail")
        
        run_kw = st.button("🔍 Find Keywords", use_container_width=True, key="kw_btn")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if run_kw:
        if not kw_input.strip():
            st.error("Keyword daalo.")
            st.stop()
        
        all_keywords = []
        
        with st.spinner("Researching keywords..."):
            if get_suggestions:
                suggestions = get_google_suggestions(kw_input)
                for s in suggestions:
                    all_keywords.append({
                        "keyword": s,
                        "source": "Autocomplete",
                        "difficulty": estimate_difficulty(s),
                        "volume": estimate_volume(s)
                    })
            
            if get_related:
                related = get_related_searches(kw_input)
                for r in related:
                    if r.lower() not in [k["keyword"].lower() for k in all_keywords]:
                        all_keywords.append({
                            "keyword": r,
                            "source": "Related",
                            "difficulty": estimate_difficulty(r),
                            "volume": estimate_volume(r)
                        })
            
            if get_paa:
                paa = get_people_also_ask(kw_input)
                for q in paa:
                    if q.lower() not in [k["keyword"].lower() for k in all_keywords]:
                        all_keywords.append({
                            "keyword": q,
                            "source": "People Also Ask",
                            "difficulty": estimate_difficulty(q),
                            "volume": estimate_volume(q)
                        })
            
            if get_longtail:
                longtail = get_long_tail_variations(kw_input)
                for lt in longtail:
                    if lt.lower() not in [k["keyword"].lower() for k in all_keywords]:
                        all_keywords.append({
                            "keyword": lt,
                            "source": "Long-tail",
                            "difficulty": estimate_difficulty(lt),
                            "volume": estimate_volume(lt)
                        })
        
        if not all_keywords:
            st.warning("No keywords found. Try a different keyword.")
        else:
            st.success(f"Found {len(all_keywords)} keywords!")
            
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                diff_filter = st.selectbox("Difficulty Filter", ["All", "Easy", "Medium", "Hard"], key="diff_filter")
            with col_f2:
                source_filter = st.selectbox("Source Filter", ["All"] + list(set(k["source"] for k in all_keywords)), key="src_filter")
            with col_f3:
                sort_by = st.selectbox("Sort By", ["Volume: High to Low", "Volume: Low to High", "Difficulty: Low to High", "Difficulty: High to Low"], key="sort_by")
            
            filtered = all_keywords.copy()
            
            if diff_filter != "All":
                filtered = [k for k in filtered if difficulty_label(k["difficulty"])[0] == diff_filter]
            
            if source_filter != "All":
                filtered = [k for k in filtered if k["source"] == source_filter]
            
            if sort_by == "Volume: High to Low":
                filtered.sort(key=lambda x: x["volume"], reverse=True)
            elif sort_by == "Volume: Low to High":
                filtered.sort(key=lambda x: x["volume"])
            elif sort_by == "Difficulty: Low to High":
                filtered.sort(key=lambda x: x["difficulty"])
            elif sort_by == "Difficulty: High to Low":
                filtered.sort(key=lambda x: x["difficulty"], reverse=True)
            
            st.markdown(f"### Showing {len(filtered)} Keywords")
            
            for kw in filtered:
                diff_text, diff_color = difficulty_label(kw["difficulty"])
                
                st.markdown(f'''
                <div class="kw-box">
                    <div>
                        <div class="kw-text">{kw["keyword"]}</div>
                        <div class="small">Source: {kw["source"]}</div>
                    </div>
                    <div style="display:flex; gap:10px; align-items:center;">
                        <div class="small">~{kw["volume"]:,} searches</div>
                        <div class="kw-badge" style="background:{diff_color}22; color:{diff_color};">{diff_text} ({kw["difficulty"]})</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown("---")
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                csv_data = "Keyword,Source,Difficulty,Estimated Volume\n"
                for kw in filtered:
                    diff_text, _ = difficulty_label(kw["difficulty"])
                    csv_data += f'"{kw["keyword"]}","{kw["source"]}","{diff_text}","{kw["volume"]}"\n'
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"keywords_{kw_input.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_exp2:
                txt_data = ""
                for kw in filtered:
                    txt_data += f"{kw['keyword']}\n"
                st.download_button(
                    label="📥 Download TXT",
                    data=txt_data,
                    file_name=f"keywords_{kw_input.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# =========================
# PAGE 3: ARTICLE WRITER
# =========================
else:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        
        col_mode = st.radio("Generation Mode", ["Template (Free - No API)", "OpenAI API (Better Quality)"], key="mode_radio")
        
        article_keyword = st.text_input("Article Topic / Keyword", placeholder="e.g., how to start a blog", key="art_kw")
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            article_tone = st.selectbox("Tone", ["Professional", "Casual", "Informative", "Persuasive", "Storytelling"], key="art_tone")
        with col_opt2:
            article_length = st.selectbox("Length", ["Short (500 words)", "Medium (1000 words)", "Long (2000 words)", "Very Long (3000+ words)"], key="art_len")
        
        api_key = ""
        if "OpenAI" in col_mode:
            api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...", key="api_key_input")
        
        extra_instructions = st.text_area("Extra Instructions (Optional)", placeholder="Include specific points, exclude certain topics, etc.", key="art_extra", height=80)
        
        run_art = st.button("✍️ Generate Article", use_container_width=True, key="art_btn")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if run_art:
        if not article_keyword.strip():
            st.error("Topic/Keyword daalo.")
            st.stop()
        
        if "OpenAI" in col_mode and not api_key.strip():
            st.error("OpenAI API key daalo.")
            st.stop()
        
        with st.spinner("Generating article..."):
            if "OpenAI" in col_mode:
                article_html = generate_article_openai(article_keyword, article_tone, article_length, api_key, extra_instructions)
            else:
                article_html = generate_article_template(article_keyword, article_tone, article_length, extra_instructions)
        
        if article_html.startswith("Error:"):
            st.error(article_html)
        else:
            word_count = count_words(article_html)
            st.success(f"Article generated! ({word_count} words)")
            
            st.markdown('<div class="article-output">', unsafe_allow_html=True)
            st.markdown(article_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            col_act1, col_act2, col_act3 = st.columns(3)
            
            with col_act1:
                plain_text = re.sub(r'<[^>]+>', '\n', article_html)
                plain_text = re.sub(r'\n{3,}', '\n\n', plain_text)
                st.download_button(
                    label="📥 Download TXT",
                    data=plain_text,
                    file_name=f"{article_keyword.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_act2:
                st.download_button(
                    label="📥 Download HTML",
                    data=article_html,
                    file_name=f"{article_keyword.replace(' ', '_')}.html",
                    mime="text/html",
                    use_container_width=True
                )
            
            with col_act3:
                md_text = article_html
                md_text = re.sub(r'<h2>(.*?)</h2>', r'## \1', md_text)
                md_text = re.sub(r'<h3>(.*?)</h3>', r'### \1', md_text)
                md_text = re.sub(r'<p>(.*?)</p>', r'\1\n', md_text)
                md_text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', md_text)
                md_text = re.sub(r'<li>(.*?)</li>', r'- \1', md_text)
                md_text = re.sub(r'<ul>|</ul>', '', md_text)
                md_text = re.sub(r'\n{3,}', '\n\n', md_text)
                st.download_button(
                    label="📥 Download Markdown",
                    data=md_text,
                    file_name=f"{article_keyword.replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#666; font-size:13px;">
    <p>Built with ❤️ | Free SEO Tool Box</p>
</div>
""", unsafe_allow_html=True)
