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
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] .stSelectbox label { color: #f5c542 !important; font-weight: 700; font-size: 14px; }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(245,197,66,0.25) !important; border-radius: 12px !important; }
    [data-testid="stSidebar"] .stSelectbox span { color: #f5c542 !important; font-weight: 600; }
    
    .sidebar-title { font-size: 20px; font-weight: 800; color: #f5c542; text-align: center; margin-bottom: 4px; }
    .sidebar-subtitle { font-size: 12px; color: #888; text-align: center; margin-bottom: 20px; }
    .sidebar-divider { height: 1px; background: rgba(245,197,66,0.15); margin: 16px 0; }
    .sidebar-info { background: rgba(245,197,66,0.06); border: 1px solid rgba(245,197,66,0.12); border-radius: 12px; padding: 14px; margin-top: 16px; }
    .sidebar-info-title { font-size: 13px; font-weight: 700; color: #f5c542; margin-bottom: 8px; }
    .sidebar-info-text { font-size: 11px; color: #999; line-height: 1.6; }
    .main-title { font-size: 42px; font-weight: 800; color: #f5c542; margin-bottom: 8px; }
    .sub-title { font-size: 17px; color: #cfcfcf; margin-bottom: 24px; }
    .box { background: rgba(255,255,255,0.04); border: 1px solid rgba(245,197,66,0.18); border-radius: 18px; padding: 18px; margin-bottom: 16px; }
    .metric-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 18px; text-align: center; }
    .metric-label { color: #bbbbbb; font-size: 14px; }
    .metric-value { color: #f5c542; font-size: 34px; font-weight: 800; }
    .small { color: #aaaaaa; font-size: 13px; }
    .kw-box { background: rgba(245,197,66,0.06); border: 1px solid rgba(245,197,66,0.15); border-radius: 12px; padding: 12px 16px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .kw-text { color: #e0e0e0; font-size: 15px; }
    .kw-badge { background: rgba(245,197,66,0.2); color: #f5c542; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
    .article-output { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 24px; line-height: 1.8; color: #d4d4d4; font-size: 16px; }
    .article-output h2 { color: #f5c542; font-size: 22px; margin-top: 20px; margin-bottom: 10px; }
    .article-output h3 { color: #e0e0e0; font-size: 18px; margin-top: 16px; margin-bottom: 8px; }
    .article-output p { margin-bottom: 12px; }
    .article-output ul { margin-left: 20px; margin-bottom: 12px; }
    .article-output li { margin-bottom: 6px; }
    .sidebar-icon-row { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border-radius: 10px; background: rgba(255,255,255,0.03); margin-bottom: 6px; font-size: 14px; color: #ccc; }
    .sidebar-icon-row .icon { font-size: 20px; }
    
    /* SERP Scraping Styles */
    .serp-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 18px 20px; margin-bottom: 14px; transition: 0.2s; }
    .serp-card:hover { border-color: rgba(245,197,66,0.3); background: rgba(255,255,255,0.05); }
    .serp-rank { color: #666; font-size: 14px; font-weight: 700; margin-right: 12px; }
    .serp-url { color: #8ab4f8; font-size: 13px; margin-bottom: 4px; display: block; text-decoration: none; word-break: break-all; }
    .serp-title { color: #8ab4f8; font-size: 18px; font-weight: 500; margin-bottom: 6px; cursor: pointer; }
    .serp-desc { color: #bdc1c6; font-size: 14px; line-height: 1.6; }
    .paa-box { background: rgba(255,255,255,0.03); border-left: 4px solid #f5c542; padding: 12px 18px; margin-bottom: 10px; border-radius: 0 8px 8px 0; color: #d4d4d4; font-size: 15px; }

    /* SERP Preview Simulator Styles */
    .preview-window {
        background: #202124;
        border-radius: 12px;
        padding: 30px 40px;
        border: 1px solid rgba(255,255,255,0.05);
        max-width: 650px;
    }
    .sp-url-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 6px;
    }
    .sp-favicon {
        width: 28px;
        height: 28px;
        background: #333;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #aaa;
        font-size: 14px;
        font-weight: bold;
    }
    .sp-url {
        color: #bdc1c6;
        font-size: 14px;
        font-family: Arial, sans-serif;
    }
    .sp-path {
        color: #70757a;
    }
    .sp-title {
        color: #8ab4f8;
        font-size: 20px;
        font-weight: 400;
        line-height: 1.3;
        margin-bottom: 6px;
        font-family: Arial, sans-serif;
        cursor: pointer;
    }
    .sp-title:hover { text-decoration: underline; }
    .sp-desc {
        color: #bdc1c6;
        font-size: 14px;
        line-height: 1.58;
        font-family: Arial, sans-serif;
    }
    .counter-good { color: #4caf50; font-weight: bold; }
    .counter-warn { color: #ff9800; font-weight: bold; }
    .counter-bad { color: #f44336; font-weight: bold; }
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
            "👁️ SERP Preview",
            "🔎 SERP Analysis",
            "🔍 Keyword Research",
            "✍️ Article Writer"
        ],
        label_visibility="visible"
    )
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="sidebar-icon-row"><span class="icon">📈</span> DA/PA Checker</div>
    <div class="sidebar-icon-row"><span class="icon">👁️</span> SERP Preview</div>
    <div class="sidebar-icon-row"><span class="icon">🔎</span> SERP Analysis</div>
    <div class="sidebar-icon-row"><span class="icon">🔍</span> Keyword Research</div>
    <div class="sidebar-icon-row"><span class="icon">✍️</span> Article Writer</div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-info-title">ℹ️ About This Tool</div>', unsafe_allow_html=True)
    st.markdown('''<div class="sidebar-info-text">
    ✅ No API key needed for most tools<br>
    ✅ No signup required<br>
    ✅ 100% free forever
    </div>''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# COMMON HELPERS
# =========================
def normalize_url(url):
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"): url = "https://" + url
    return url

def get_domain(url):
    parsed = urlparse(url)
    return parsed.netloc.replace("www.", "")

def extract_whois_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list): creation_date = creation_date[0]
        if not creation_date: return None, None
        age_years = round((datetime.now() - creation_date).days / 365.25, 2)
        return creation_date, age_years
    except: return None, None

def check_ssl(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain): return True
    except: return False

def analyze_page(url):
    result = {"status_code": None, "title": "", "meta_description": "", "h1_count": 0, "h2_count": 0, "word_count": 0, "internal_links": 0, "external_links": 0, "images": 0, "images_missing_alt": 0, "canonical": False, "robots_meta": False, "https": url.startswith("https://"), "response_time": None}
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        start = datetime.now()
        r = requests.get(url, headers=headers, timeout=15)
        result["response_time"] = round((datetime.now() - start).total_seconds(), 2)
        result["status_code"] = r.status_code
        if r.status_code != 200: return result
        soup = BeautifulSoup(r.text, "html.parser")
        if soup.title and soup.title.text: result["title"] = soup.title.text.strip()
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"): result["meta_description"] = meta_desc.get("content").strip()
        result["h1_count"] = len(soup.find_all("h1"))
        result["h2_count"] = len(soup.find_all("h2"))
        words = re.findall(r"\w+", soup.get_text(" ", strip=True))
        result["word_count"] = len(words)
        result["canonical"] = soup.find("link", attrs={"rel": "canonical"}) is not None
        result["robots_meta"] = soup.find("meta", attrs={"name": re.compile("^robots$", re.I)}) is not None
        domain = get_domain(url)
        for link in soup.find_all("a", href=True):
            href = link["href"].strip()
            full = urljoin(url, href)
            link_domain = urlparse(full).netloc.replace("www.", "")
            if not urlparse(full).netloc or link_domain == domain: result["internal_links"] += 1
            else: result["external_links"] += 1
        imgs = soup.find_all("img")
        result["images"] = len(imgs)
        result["images_missing_alt"] = sum(1 for img in imgs if not img.get("alt") or not img.get("alt").strip())
        return result
    except: return result

def calculate_da(domain_age, ssl_ok, page_data, domain):
    score = 0
    if domain_age:
        if domain_age >= 10: score += 25
        elif domain_age >= 5: score += 18
        elif domain_age >= 2: score += 12
        else: score += 6
    if ssl_ok: score += 10
    if len(domain) < 20: score += 5
    if "-" not in domain: score += 5
    if page_data["status_code"] == 200: score += 10
    if page_data["title"]: score += 5
    if page_data["meta_description"]: score += 5
    if page_data["canonical"]: score += 5
    if page_data["robots_meta"]: score += 2
    if page_data["internal_links"] >= 10: score += 8
    elif page_data["internal_links"] >= 5: score += 5
    if page_data["external_links"] >= 2: score += 3
    if page_data["word_count"] >= 1500: score += 7
    elif page_data["word_count"] >= 800: score += 5
    elif page_data["word_count"] >= 300: score += 3
    return min(score, 100)

def calculate_pa(page_data):
    score = 15 if page_data["status_code"] == 200 else 0
    if page_data["title"]: score += 10
    if page_data["meta_description"]: score += 8
    if page_data["h1_count"] == 1: score += 10
    elif page_data["h1_count"] > 1: score += 5
    if page_data["h2_count"] >= 3: score += 10
    elif page_data["h2_count"] >= 1: score += 5
    if page_data["word_count"] >= 2000: score += 20
    elif page_data["word_count"] >= 1200: score += 15
    elif page_data["word_count"] >= 600: score += 10
    elif page_data["word_count"] >= 300: score += 5
    if page_data["internal_links"] >= 10: score += 10
    elif page_data["internal_links"] >= 5: score += 6
    if page_data["external_links"] >= 3: score += 5
    if page_data["images"] > 0:
        ratio = (page_data["images"] - page_data["images_missing_alt"]) / page_data["images"]
        if ratio >= 0.8: score += 7
        elif ratio >= 0.5: score += 4
    if page_data["canonical"]: score += 5
    return min(score, 100)

def score_label(score):
    if score >= 80: return "Excellent"
    elif score >= 60: return "Strong"
    elif score >= 40: return "Average"
    elif score >= 20: return "Weak"
    return "Poor"

def get_google_suggestions(keyword):
    try:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={quote_plus(keyword)}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        return r.json()[1] if r.status_code == 200 else []
    except: return []

def get_related_searches(keyword):
    try:
        url = f"https://www.google.com/search?q={quote_plus(keyword)}&hl=en"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            return [div.get_text(strip=True) for div in soup.find_all("div", class_="wCb7ib") if div.get_text(strip=True)]
        return []
    except: return []

def get_people_also_ask(keyword):
    try:
        url = f"https://www.google.com/search?q={quote_plus(keyword)}&hl=en"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            return [div.get_text(strip=True) for div in soup.find_all("div", attrs={"class": re.compile("related-question-pair")}) if div.get_text(strip=True)]
        return []
    except: return []

def get_long_tail_variations(keyword):
    prefixes = ["how to", "best way to", "why", "what is", "top 10", "guide to", "tips for", "for beginners", "free", "online"]
    suffixes = ["guide", "tutorial", "tips", "for beginners", "step by step", "in 2024", "online", "free"]
    variations = set()
    for p in prefixes: variations.add(f"{p} {keyword}")
    for s in suffixes: variations.add(f"{keyword} {s}")
    return list(variations)

def estimate_difficulty(kw):
    diff = 40 if len(kw.split()) == 1 else 25 if len(kw.split()) == 2 else 10
    if any(w in kw.lower() for w in ["buy", "price", "best", "review"]): diff += 10
    if any(w in kw.lower() for w in ["how", "what", "why", "guide"]): diff -= 10
    return max(5, min(diff, 95))

def difficulty_label(score):
    if score >= 70: return "Hard", "#ff4444"
    elif score >= 45: return "Medium", "#ffaa00"
    return "Easy", "#44ff44"

def estimate_volume(keyword):
    base = 20000 if len(keyword.split()) == 1 else 5000 if len(keyword.split()) == 2 else 1500 if len(keyword.split()) == 3 else 500
    return int(base * random.uniform(0.6, 1.4))

def scrape_serp(keyword):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(f"https://www.google.com/search?q={quote_plus(keyword)}&hl=en&num=10", headers=headers, timeout=15)
        if r.status_code != 200: return None, [], [], []
        soup = BeautifulSoup(r.text, "html.parser")
        total_text = "N/A"
        stats = soup.find("div", {"id": "result-stats"})
        if stats: total_text = stats.text.strip()
        results = []
        for g in soup.find_all("div", class_="g"):
            anchor = g.find("a")
            if not anchor or not anchor.get("href"): continue
            link = anchor["href"]
            if "/search?" in link or link.startswith("#") or "google.com" in link: continue
            title_tag = g.find("h3")
            title = title_tag.text if title_tag else "No Title"
            desc_tag = g.find("div", class_=["VwiC3b", "yXK7lf", "MUxGbd", "yDYNvb", "lEBKkf"])
            desc = desc_tag.text if desc_tag else ""
            if title != "No Title" or desc: results.append({"title": title, "url": link, "desc": desc})
        return total_text, results[:10], get_people_also_ask(keyword), get_related_searches(keyword)
    except: return None, [], [], []

def generate_article_openai(keyword, tone, length, api_key, extra=""):
    try:
        import openai
        openai.api_key = api_key
        word_target = {"Short (500 words)": 500, "Medium (1000 words)": 1000, "Long (2000 words)": 2000, "Very Long (3000+ words)": 3000}.get(length, 1000)
        extra_text = f"\n\nAdditional instructions: {extra}" if extra.strip() else ""
        prompt = f"""Write a high-quality, SEO-optimized article about "{keyword}".\nRequirements:\n- Tone: {tone}\n- Target length: approximately {word_target} words\n- Format in clean HTML (use h2, h3, p, ul, li, strong tags)\n{extra_text}\nDo NOT include ```html or ``` tags."""
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are an expert SEO content writer."}, {"role": "user", "content": prompt}], max_tokens=4000, temperature=0.7)
        return response.choices[0].message.content
    except Exception as e: return f"Error: {str(e)}"

def generate_article_template(keyword, tone, length, extra=""):
    ck = keyword.title().strip()
    num_sections = {"Short (500 words)": 3, "Medium (1000 words)": 5, "Long (2000 words)": 8, "Very Long (3000+ words)": 12}.get(length, 5)
    sections = [f"Understanding {ck}", f"Key Benefits", f"How to Implement", f"Common Mistakes", f"Advanced Strategies", f"Measuring Success", f"Future Trends", f"Expert Insights", f"Case Studies", f"Tools Needed", f"FAQs", f"Conclusion"][:num_sections]
    html = f'<h2>{ck}: The Complete Guide</h2><p>Are you looking to master {ck}? In this guide, we cover everything you need to know.</p>'
    if extra.strip(): html += f"<p><em>Note: {extra}</em></p>"
    for sec in sections:
        html += f'<h3>{sec}</h3><p>Understanding the core principles is essential. Experts recommend a structured approach to maximize results.</p><ul><li>Focus on fundamentals</li><li>Apply practically</li><li>Refine strategy</li></ul>'
    html += f'<h3>Conclusion</h3><p>Mastering {ck} takes time, but by following these steps, you will see significant improvements.</p>'
    return html

def count_words(html_content):
    return len(re.findall(r'\w+', re.sub(r'<[^>]+>', ' ', html_content)))

# =========================
# ROUTING LOGIC
# =========================
page_config = {
    "DA PA": {"title": "📈 DA PA Checker", "desc": "Estimated DA / PA based on real on-page and domain signals."},
    "SERP Preview": {"title": "👁️ SERP Preview Simulator", "desc": "See exactly how your page will look on Google Search Results."},
    "SERP Analysis": {"title": "🔎 Live SERP Analysis", "desc": "Scrape top 10 Google results, PAA, and Related Searches."},
    "Keyword": {"title": "🔍 Keyword Research", "desc": "Google Autocomplete, Related Searches, Long-tail variations."},
    "Article": {"title": "✍️ Article Writer", "desc": "Generate SEO-optimized articles with or without OpenAI API."}
}

p_type = next((k for k in page_config if k in page), "DA PA")
cfg = page_config[p_type]

st.markdown(f'<div class="main-title">{cfg["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">{cfg["desc"]}</div>', unsafe_allow_html=True)

# =========================
# PAGE 1: DA PA
# =========================
if p_type == "DA PA":
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        url = st.text_input("Enter Website URL", placeholder="example.com", key="da_url")
        run = st.button("Check DA PA", use_container_width=True, key="da_btn")
        st.markdown('</div>', unsafe_allow_html=True)
    if run:
        if not url.strip(): st.error("URL daalo."); st.stop()
        url = normalize_url(url)
        domain = get_domain(url)
        with st.spinner("Analyzing..."):
            creation_date, domain_age = extract_whois_age(domain)
            ssl_ok = check_ssl(domain)
            page_data = analyze_page(url)
            da, pa = calculate_da(domain_age, ssl_ok, page_data, domain), calculate_pa(page_data)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">DA Score</div><div class="metric-value">{da}</div><div class="small">{score_label(da)}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card"><div class="metric-label">PA Score</div><div class="metric-value">{pa}</div><div class="small">{score_label(pa)}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card"><div class="metric-label">Domain Age</div><div class="metric-value" style="font-size:26px;">{domain_age if domain_age else "N/A"} yrs</div><div class="small">{creation_date.strftime("%Y-%m-%d") if creation_date else "N/A"}</div></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="metric-card"><div class="metric-label">HTTP Status</div><div class="metric-value">{page_data["status_code"] or "-"}</div><div class="small">SSL: {"Yes" if ssl_ok else "No"}</div></div>', unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        with d1:
            st.markdown('<div class="box">', unsafe_allow_html=True)
            st.write(f"**Title:** {'Yes' if page_data['title'] else 'No'}")
            st.write(f"**Meta Desc:** {'Yes' if page_data['meta_description'] else 'No'}")
            st.write(f"**H1:** {page_data['h1_count']} | **H2:** {page_data['h2_count']}")
            st.write(f"**Words:** {page_data['word_count']}")
            st.markdown('</div>', unsafe_allow_html=True)
        with d2:
            st.markdown('<div class="box">', unsafe_allow_html=True)
            st.write(f"**Internal Links:** {page_data['internal_links']}")
            st.write(f"**External Links:** {page_data['external_links']}")
            st.write(f"**Images Missing Alt:** {page_data['images_missing_alt']}/{page_data['images']}")
            st.write(f"**Response Time:** {page_data['response_time']}s" if page_data['response_time'] else "**Response Time:** N/A")
            st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PAGE 2: SERP PREVIEW SIMULATOR
# =========================
elif p_type == "SERP Preview":
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        p_url = st.text_input("Page URL", placeholder="https://www.example.com/my-page", key="sp_url")
        p_title = st.text_input("SEO Title Tag", placeholder="My Awesome SEO Title (50-60 Characters)", key="sp_title")
        p_desc = st.text_area("Meta Description", placeholder="Write a compelling summary of your page here (150-160 Characters)...", key="sp_desc", height=80)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Character Counts Logic
    t_len = len(p_title)
    d_len = len(p_desc)
    
    def get_counter_class(length, min_good, max_good):
        if min_good <= length <= max_good: return "counter-good"
        elif (min_good - 10 <= length < min_good) or (max_good < length <= max_good + 10): return "counter-warn"
        return "counter-bad"

    t_class = get_counter_class(t_len, 50, 60)
    d_class = get_counter_class(d_len, 150, 160)
    
    # Truncation logic for Google
    display_title = p_title if t_len <= 60 else p_title[:57] + "..."
    display_desc = p_desc if d_len <= 160 else p_desc[:157] + "..."
    
    # Parse URL for display
    parsed_url = urlparse(p_url if p_url else "https://www.example.com")
    domain_name = parsed_url.netloc.replace("www.", "") if parsed_url.netloc else "example.com"
    path_name = parsed_url.path if parsed_url.path else ""
    favicon_letter = domain_name[0].upper() if domain_name else "E"

    st.markdown("### Google Search Result Preview")
    st.caption("This is exactly how users will see your link on Google.")
    
    st.markdown(f'''
    <div class="preview-window">
        <div class="sp-url-container">
            <div class="sp-favicon">{favicon_letter}</div>
            <div class="sp-url">{domain_name} <span class="sp-path">{path_name}</span></div>
        </div>
        <div class="sp-title">{display_title if p_title else "Your SEO Title Will Appear Here"}</div>
        <div class="sp-desc">{display_desc if p_desc else "Your meta description will appear here. Make sure it includes your target keyword and is compelling enough to click."}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 SEO Character Limits Check")
    
    col_ch1, col_ch2 = st.columns(2)
    with col_ch1:
        st.markdown(f'''
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:10px; border:1px solid rgba(255,255,255,0.05);">
            <div style="color:#ccc; font-size:14px; margin-bottom:5px;">Title Tag Length</div>
            <div style="font-size:28px; font-weight:bold;" class="{t_class}">{t_len}</div>
            <div style="color:#666; font-size:12px; margin-top:5px;">Recommended: 50 - 60 characters</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with col_ch2:
        st.markdown(f'''
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:10px; border:1px solid rgba(255,255,255,0.05);">
            <div style="color:#ccc; font-size:14px; margin-bottom:5px;">Meta Description Length</div>
            <div style="font-size:28px; font-weight:bold;" class="{d_class}">{d_len}</div>
            <div style="color:#666; font-size:12px; margin-top:5px;">Recommended: 150 - 160 characters</div>
        </div>
        ''', unsafe_allow_html=True)

    # Warnings / Tips
    if t_len > 60:
        st.warning("⚠️ Title is too long! Google will cut it off with '...' in search results.")
    elif t_len < 50 and t_len > 0:
        st.info("💡 Title is slightly short. You can add more keywords to utilize the full space.")
        
    if d_len > 160:
        st.warning("⚠️ Meta description is too long! It will be truncated.")
    elif d_len < 150 and d_len > 0:
        st.info("💡 Description is slightly short. Utilize the space to improve CTR.")
    elif d_len == 0 and t_len > 0:
        st.warning("⚠️ Missing Meta Description! Google will auto-generate one, which might not be ideal.")

# =========================
# PAGE 3: SERP ANALYSIS
# =========================
elif p_type == "SERP Analysis":
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        serp_kw = st.text_input("Enter Keyword to Analyze", placeholder="e.g., best seo tools 2024", key="serp_kw")
        run_serp = st.button("🔎 Analyze SERP", use_container_width=True, key="serp_btn")
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption("⚠️ Note: Google frequently blocks automated scraping. If empty, CAPTCHA might have been triggered.")
    if run_serp:
        if not serp_kw.strip(): st.error("Keyword daalo."); st.stop()
        with st.spinner("Scraping Google..."):
            total_res, organic, paa, related = scrape_serp(serp_kw)
        if total_res is None:
            st.error("Failed to fetch. Google blocked the request.")
        else:
            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Results</div><div class="metric-value" style="font-size:20px;">{total_res}</div></div>', unsafe_allow_html=True)
            with m2: st.markdown(f'<div class="metric-card"><div class="metric-label">Organic URLs</div><div class="metric-value">{len(organic)}</div></div>', unsafe_allow_html=True)
            with m3: st.markdown(f'<div class="metric-card"><div class="metric-label">PAA Questions</div><div class="metric-value">{len(paa)}</div></div>', unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("### 🌐 Top Organic Results")
            if not organic: st.warning("No organic results extracted.")
            else:
                for i, res in enumerate(organic):
                    st.markdown(f'<div class="serp-card"><div style="display:flex;align-items:start;"><div class="serp-rank">#{i+1}</div><div style="flex:1;"><a href="{res["url"]}" target="_blank" class="serp-url">{res["url"][:80]}...</a><div class="serp-title">{res["title"]}</div><div class="serp-desc">{res["desc"][:200]}...</div></div></div></div>', unsafe_allow_html=True)
            if paa:
                st.markdown("---"); st.markdown("### ❓ People Also Ask")
                for q in paa: st.markdown(f'<div class="paa-box">👉 {q}</div>', unsafe_allow_html=True)
            if related:
                st.markdown("---"); st.markdown("### 🔗 Related Searches")
                rel_cols = st.columns(3)
                for i, rel in enumerate(related[:9]):
                    with rel_cols[i % 3]: st.markdown(f'<div class="small" style="margin-bottom:8px;">• {rel}</div>', unsafe_allow_html=True)

# =========================
# PAGE 4: KEYWORD RESEARCH
# =========================
elif p_type == "Keyword":
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        kw_input = st.text_input("Enter Seed Keyword", placeholder="e.g., best laptops", key="kw_input")
        c1, c2 = st.columns(2)
        with c1: get_suggest = st.checkbox("Suggestions", value=True); get_rel = st.checkbox("Related", value=True)
        with c2: get_paa = st.checkbox("PAA", value=True); get_lt = st.checkbox("Long-tail", value=True)
        run_kw = st.button("🔍 Find Keywords", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    if run_kw:
        if not kw_input.strip(): st.error("Keyword daalo."); st.stop()
        all_kws = []
        with st.spinner("Finding keywords..."):
            if get_suggest:
                for s in get_google_suggestions(kw_input): all_kws.append({"kw": s, "src": "Auto", "diff": estimate_difficulty(s), "vol": estimate_volume(s)})
            if get_rel:
                for r in get_related_searches(kw_input):
                    if r.lower() not in [k["kw"].lower() for k in all_kws]: all_kws.append({"kw": r, "src": "Related", "diff": estimate_difficulty(r), "vol": estimate_volume(r)})
            if get_paa:
                for q in get_people_also_ask(kw_input):
                    if q.lower() not in [k["kw"].lower() for k in all_kws]: all_kws.append({"kw": q, "src": "PAA", "diff": estimate_difficulty(q), "vol": estimate_volume(q)})
            if get_lt:
                for lt in get_long_tail_variations(kw_input):
                    if lt.lower() not in [k["kw"].lower() for k in all_kws]: all_kws.append({"kw": lt, "src": "Long-tail", "diff": estimate_difficulty(lt), "vol": estimate_volume(lt)})
        if not all_kws: st.warning("No keywords found.")
        else:
            f1, f2, f3 = st.columns(3)
            with f1: d_filt = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"])
            with f2: s_filt = st.selectbox("Source", ["All"] + list(set(k["src"] for k in all_kws)))
            with f3: s_by = st.selectbox("Sort", ["Vol: High", "Vol: Low", "Diff: Low", "Diff: High"])
            filt = [k for k in all_kws if (d_filt=="All" or difficulty_label(k["diff"])[0]==d_filt) and (s_filt=="All" or k["src"]==s_filt)]
            if "High" in s_by: filt.sort(key=lambda x: x["vol" if "Vol" in s_by else "diff"], reverse=True)
            else: filt.sort(key=lambda x: x["vol" if "Vol" in s_by else "diff"])
            for k in filt:
                dt, dc = difficulty_label(k["diff"])
                st.markdown(f'<div class="kw-box"><div><div class="kw-text">{k["kw"]}</div><div class="small">{k["src"]}</div></div><div style="display:flex;gap:10px;"><div class="small">~{k["vol"]:,}</div><div class="kw-badge" style="color:{dc};background:{dc}22;">{dt} ({k["diff"]})</div></div></div>', unsafe_allow_html=True)

# =========================
# PAGE 5: ARTICLE WRITER
# =========================
elif p_type == "Article":
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        mode = st.radio("Mode", ["Template (Free)", "OpenAI (Better)"])
        a_kw = st.text_input("Topic", placeholder="how to start blogging", key="a_kw")
        o1, o2 = st.columns(2)
        with o1: tone = st.selectbox("Tone", ["Professional", "Casual", "Informative", "Persuasive"])
        with o2: length = st.selectbox("Length", ["Short (500 words)", "Medium (1000 words)", "Long (2000 words)"])
        api = ""
        if "OpenAI" in mode: api = st.text_input("API Key", type="password")
        extra = st.text_area("Extra Instructions (Optional)", key="a_extra")
        run_a = st.button("✍️ Generate", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    if run_a:
        if not a_kw.strip(): st.error("Topic daalo."); st.stop()
        if "OpenAI" in mode and not api.strip(): st.error("API key daalo."); st.stop()
        with st.spinner("Writing..."):
            html = generate_article_openai(a_kw, tone, length, api, extra) if "OpenAI" in mode else generate_article_template(a_kw, tone, length, extra)
        if html.startswith("Error:"): st.error(html)
        else:
            st.success(f"Done! ({count_words(html)} words)")
            st.markdown(f'<div class="article-output">{html}</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            plain = re.sub(r'<[^>]+>', '\n', html)
            md = re.sub(r'<h2>(.*?)</h2>', r'## \1', re.sub(r'<h3>(.*?)</h3>', r'### \1', re.sub(r'<li>(.*?)</li>', r'- \1', re.sub(r'<[^>]+>', '', html))))
            with c1: st.download_button("📥 TXT", plain, f"{a_kw}.txt")
            with c2: st.download_button("📥 HTML", html, f"{a_kw}.html", mime="text/html")
            with c3: st.download_button("📥 MD", md, f"{a_kw}.md", mime="text/markdown")

st.markdown("---")
st.markdown('<div style="text-align:center; color:#444; font-size:12px;">Built with ❤️ | Free SEO Tool Box</div>', unsafe_allow_html=True)
