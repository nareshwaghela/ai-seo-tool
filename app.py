import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, quote_plus
import whois
from datetime import datetime
import re
import socket
import ssl
import random

st.set_page_config(page_title="Free SEO Tool Box", page_icon="🚀", layout="wide")

# =========================
# STYLES
# =========================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0f13 0%, #161622 100%); color: white; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #12121a 0%, #1a1a2e 100%); border-right: 1px solid rgba(245,197,66,0.15); }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] .stSelectbox label { color: #f5c542 !important; font-weight: 700; font-size: 14px; }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(245,197,66,0.25) !important; border-radius: 12px !important; }
    [data-testid="stSidebar"] .stSelectbox span { color: #f5c542 !important; font-weight: 600; }
    .sidebar-title { font-size: 20px; font-weight: 800; color: #f5c542; text-align: center; margin-bottom: 4px; }
    .sidebar-subtitle { font-size: 12px; color: #888; text-align: center; margin-bottom: 20px; }
    .sidebar-divider { height: 1px; background: rgba(245,197,66,0.15); margin: 16px 0; }
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
    
    .preview-window { background: #202124; border-radius: 12px; padding: 30px 40px; border: 1px solid rgba(255,255,255,0.05); max-width: 650px; }
    .sp-favicon { width: 28px; height: 28px; background: #333; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #aaa; font-size: 14px; font-weight: bold; margin-right: 12px; }
    .sp-url { color: #bdc1c6; font-size: 14px; font-family: Arial, sans-serif; }
    .sp-path { color: #70757a; }
    .sp-title { color: #8ab4f8; font-size: 20px; font-weight: 400; margin-bottom: 6px; font-family: Arial, sans-serif; cursor:pointer; }
    .sp-desc { color: #bdc1c6; font-size: 14px; line-height: 1.58; font-family: Arial, sans-serif; }
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
    st.markdown('<div class="sidebar-subtitle">Optimized for Cloud & Local</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    page = st.selectbox("Navigate To", [
        "👁️ SERP Preview", "📈 DA PA Checker", 
        "🔍 Keyword Research", "✍️ Article Writer"
    ], label_visibility="visible")
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="sidebar-icon-row"><span class="icon">👁️</span> SERP Preview (Auto Fetch)</div>
    <div class="sidebar-icon-row"><span class="icon">📈</span> DA/PA Checker</div>
    <div class="sidebar-icon-row"><span class="icon">🔍</span> Keyword Research</div>
    <div class="sidebar-icon-row"><span class="icon">✍️</span> Article Writer</div>
    ''', unsafe_allow_html=True)

# =========================
# COMMON HELPERS
# =========================
def normalize_url(url):
    url = url.strip()
    if not url.startswith("http"): url = "https://" + url
    return url

def get_domain(url):
    return urlparse(url).netloc.replace("www.", "")

def check_ssl(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain): return True
    except: return False

def fetch_meta_tags(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code != 200: return None, None, "HTTP Error"
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.text.strip() if soup.title and soup.title.text else ""
        desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"): desc = meta.get("content").strip()
        return title, desc, "Success"
    except requests.exceptions.Timeout: return None, None, "Timeout"
    except requests.exceptions.ConnectionError: return None, None, "Connection Blocked"
    except Exception as e: return None, None, str(e)

def analyze_page(url):
    result = {"status_code": None, "title": "", "meta_description": "", "h1_count": 0, "h2_count": 0, "word_count": 0, "internal_links": 0, "external_links": 0, "images": 0, "images_missing_alt": 0, "canonical": False, "https": url.startswith("https://"), "response_time": None}
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        start = datetime.now()
        r = requests.get(url, headers=headers, timeout=10)
        result["response_time"] = round((datetime.now() - start).total_seconds(), 2)
        result["status_code"] = r.status_code
        if r.status_code != 200: return result
        soup = BeautifulSoup(r.text, "html.parser")
        if soup.title and soup.title.text: result["title"] = soup.title.text.strip()
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"): result["meta_description"] = meta_desc.get("content").strip()
        result["h1_count"] = len(soup.find_all("h1"))
        result["h2_count"] = len(soup.find_all("h2"))
        result["word_count"] = len(re.findall(r"\w+", soup.get_text(" ", strip=True)))
        result["canonical"] = soup.find("link", attrs={"rel": "canonical"}) is not None
        domain = get_domain(url)
        for link in soup.find_all("a", href=True):
            link_domain = urlparse(urljoin(url, link["href"])).netloc.replace("www.", "")
            if not link_domain or link_domain == domain: result["internal_links"] += 1
            else: result["external_links"] += 1
        imgs = soup.find_all("img")
        result["images"] = len(imgs)
        result["images_missing_alt"] = sum(1 for img in imgs if not img.get("alt") or not img.get("alt").strip())
    except Exception as e: result["error"] = str(e)
    return result

def calculate_da(domain_age, ssl_ok, page_data, domain):
    score = 0
    if domain_age and domain_age > 0:
        if domain_age >= 10: score += 25
        elif domain_age >= 5: score += 18
        elif domain_age >= 2: score += 12
        else: score += 6
    if ssl_ok: score += 10
    if len(domain) < 20: score += 5
    if "-" not in domain: score += 5
    if page_data.get("status_code") == 200: score += 10
    if page_data.get("title"): score += 5
    if page_data.get("meta_description"): score += 5
    if page_data.get("canonical"): score += 5
    if page_data.get("internal_links", 0) >= 10: score += 8
    elif page_data.get("internal_links", 0) >= 5: score += 5
    if page_data.get("word_count", 0) >= 1500: score += 7
    elif page_data.get("word_count", 0) >= 800: score += 5
    return min(score, 100)

def calculate_pa(page_data):
    score = 15 if page_data.get("status_code") == 200 else 0
    if page_data.get("title"): score += 10
    if page_data.get("meta_description"): score += 8
    if page_data.get("h1_count") == 1: score += 10
    elif page_data.get("h1_count", 0) > 1: score += 5
    if page_data.get("h2_count", 0) >= 3: score += 10
    elif page_data.get("h2_count", 0) >= 1: score += 5
    if page_data.get("word_count", 0) >= 2000: score += 20
    elif page_data.get("word_count", 0) >= 1200: score += 15
    elif page_data.get("word_count", 0) >= 600: score += 10
    elif page_data.get("word_count", 0) >= 300: score += 5
    if page_data.get("internal_links", 0) >= 10: score += 10
    elif page_data.get("internal_links", 0) >= 5: score += 6
    if page_data.get("external_links", 0) >= 3: score += 5
    if page_data.get("images", 0) > 0:
        ratio = (page_data["images"] - page_data.get("images_missing_alt", 0)) / page_data["images"]
        if ratio >= 0.8: score += 7
        elif ratio >= 0.5: score += 4
    if page_data.get("canonical"): score += 5
    return min(score, 100)

def score_label(score):
    if score >= 80: return "Excellent"
    elif score >= 60: return "Strong"
    elif score >= 40: return "Average"
    elif score >= 20: return "Weak"
    return "Poor"

def get_google_suggestions(keyword):
    try:
        r = requests.get(f"https://suggestqueries.google.com/complete/search?client=firefox&q={quote_plus(keyword)}", timeout=5)
        return r.json()[1] if r.status_code == 200 else []
    except: return []

def get_related_searches_bing(keyword):
    try:
        r = requests.get(f"https://www.bing.com/search?q={quote_plus(keyword)}", headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            related = []
            for li in soup.find_all("li", class_="b_algo"):
                text = li.get_text(strip=True)
                if text and text not in related: related.append(text)
            return related[:10]
        return []
    except: return []

def get_long_tail_variations(keyword):
    prefixes = ["how to", "best", "what is", "top 10", "guide", "tips for", "vs", "review", "free", "online"]
    suffixes = ["guide", "tutorial", "tips", "for beginners", "in 2024", "online", "free"]
    variations = set()
    for p in prefixes: variations.add(f"{p} {keyword}")
    for s in suffixes: variations.add(f"{keyword} {s}")
    return list(variations)

def estimate_difficulty(kw):
    diff = 40 if len(kw.split()) == 1 else 25 if len(kw.split()) == 2 else 10
    if any(w in kw.lower() for w in ["buy", "price", "best"]): diff += 10
    if any(w in kw.lower() for w in ["how", "what", "why"]): diff -= 10
    return max(5, min(diff, 95))

def difficulty_label(score):
    if score >= 70: return "Hard", "#ff4444"
    elif score >= 45: return "Medium", "#ffaa00"
    return "Easy", "#44ff44"

def estimate_volume(keyword): return int((20000 if len(keyword.split()) == 1 else 5000 if len(keyword.split()) == 2 else 1500) * random.uniform(0.6, 1.4))

def generate_article_template(keyword, tone, length):
    ck = keyword.title().strip()
    num = {"Short": 3, "Medium": 5, "Long": 8}.get(length, 5)
    secs = ["Understanding", "Key Benefits", "How to Implement", "Common Mistakes", "Advanced Strategies", "Measuring Success", "Future Trends", "Conclusion"][:num]
    html = f'<h2>{ck}: Complete Guide</h2><p>Master {ck} with this comprehensive guide covering basics to advanced concepts.</p>'
    for s in secs: html += f'<h3>{s} {ck}</h3><p>Understanding the core principles of {s.lower()} {ck.lower()} is essential.</p><ul><li>Focus on fundamentals</li><li>Apply practically</li></ul>'
    return html

def count_words(t): return len(re.findall(r'\w+', re.sub(r'<[^>]+>', ' ', t)))

# =========================
# ROUTING
# =========================
page_config = {
    "SERP Preview": {"title": "👁️ SERP Preview Simulator", "desc": "Paste URL to auto-fetch Title & Meta, or enter manually."},
    "DA PA": {"title": "📈 DA PA Checker", "desc": "Estimated DA/PA. Works even if cloud blocks WHOIS."},
    "Keyword": {"title": "🔍 Keyword Research", "desc": "Keywords via Google Suggest API (Cloud Safe)."},
    "Article": {"title": "✍️ Article Writer", "desc": "Generate SEO articles (Free Template Mode)."}
}
p_type = next((k for k in page_config if k in page), "SERP Preview")
cfg = page_config[p_type]
st.markdown(f'<div class="main-title">{cfg["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">{cfg["desc"]}</div>', unsafe_allow_html=True)

# =========================
# PAGE 1: SERP PREVIEW (FIXED SESSION STATE)
# =========================
if p_type == "SERP Preview":
    
    # Initialize state for fetch messages
    if "fetch_msg" not in st.session_state:
        st.session_state.fetch_msg = ""

    def fetch_data_callback():
        url = st.session_state.get("sp_url", "")
        if not url.strip():
            st.session_state.fetch_msg = "error:Please enter a URL first."
            return
            
        clean_url = normalize_url(url)
        # We can't use st.spinner inside a callback, so just fetch normally
        title, desc, status = fetch_meta_tags(clean_url)
        
        if status == "Success":
            if title or desc:
                st.session_state.sp_title = title
                st.session_state.sp_desc = desc
                st.session_state.fetch_msg = "success:Data fetched successfully!"
            else:
                st.session_state.fetch_msg = "warning:Page loaded, but NO Title or Meta Description was found."
        else:
            st.session_state.fetch_msg = f"error:Failed to fetch ({status}). Cloud servers often block direct fetching. Please enter data manually."

    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        
        col_url, col_btn = st.columns([4, 1])
        
        with col_url:
            p_url = st.text_input("Page URL", placeholder="https://www.example.com/page", key="sp_url")
        with col_btn:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            fetch_btn = st.button("🔍 Fetch", use_container_width=True, on_click=fetch_data_callback)
        
        p_title = st.text_input("SEO Title Tag", placeholder="My Awesome Title (50-60 Characters)", key="sp_title")
        p_desc = st.text_area("Meta Description", placeholder="Summary of your page (150-160 Characters)...", key="sp_desc", height=80)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Show Fetch Status Message
    if st.session_state.fetch_msg:
        msg = st.session_state.fetch_msg
        if msg.startswith("success:"): st.success(msg.split(":", 1)[1])
        elif msg.startswith("error:"): st.error(msg.split(":", 1)[1])
        elif msg.startswith("warning:"): st.warning(msg.split(":", 1)[1])
        # Clear message after showing
        st.session_state.fetch_msg = ""

    # PREVIEW LOGIC
    t_len, d_len = len(p_title), len(p_desc)
    def get_cc(l, mn, mx): return "counter-good" if mn <= l <= mx else "counter-warn" if (mn-10 <= l < mn) or (mx < l <= mx+10) else "counter-bad"
    
    display_title = p_title if t_len <= 60 else p_title[:57] + "..."
    display_desc = p_desc if d_len <= 160 else p_desc[:157] + "..."
    parsed_url = urlparse(p_url if p_url else "https://www.example.com")
    domain_name = parsed_url.netloc.replace("www.", "") if parsed_url.netloc else "example.com"
    
    st.markdown("### Google Search Result Preview")
    st.caption("This is exactly how users will see your link on Google.")
    
    st.markdown(f'''
    <div class="preview-window">
        <div style="display:flex;align-items:center;margin-bottom:6px;">
            <div class="sp-favicon">{domain_name[0].upper() if domain_name else "E"}</div>
            <div class="sp-url">{domain_name} <span class="sp-path">{parsed_url.path}</span></div>
        </div>
        <div class="sp-title">{display_title if p_title else "Your SEO Title Will Appear Here"}</div>
        <div class="sp-desc">{display_desc if p_desc else "Your meta description will appear here. Make sure it includes your target keyword..."}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 SEO Character Limits Check")
    
    col_ch1, col_ch2 = st.columns(2)
    with col_ch1: 
        st.markdown(f'<div style="background:rgba(255,255,255,0.03);padding:15px;border-radius:10px;border:1px solid rgba(255,255,255,0.05);"><div style="color:#ccc;font-size:14px;margin-bottom:5px;">Title Tag Length</div><div style="font-size:28px;font-weight:bold;" class="{get_cc(t_len, 50, 60)}">{t_len}</div><div style="color:#666;font-size:12px;margin-top:5px;">Recommended: 50 - 60</div></div>', unsafe_allow_html=True)
    with col_ch2: 
        st.markdown(f'<div style="background:rgba(255,255,255,0.03);padding:15px;border-radius:10px;border:1px solid rgba(255,255,255,0.05);"><div style="color:#ccc;font-size:14px;margin-bottom:5px;">Meta Description Length</div><div style="font-size:28px;font-weight:bold;" class="{get_cc(d_len, 150, 160)}">{d_len}</div><div style="color:#666;font-size:12px;margin-top:5px;">Recommended: 150 - 160</div></div>', unsafe_allow_html=True)

    if t_len > 60: st.warning("⚠️ Title too long! Google will cut it off.")
    if d_len > 160: st.warning("⚠️ Description too long! It will be truncated.")
    if 0 < t_len < 50: st.info("💡 Title is slightly short. You can add more keywords.")

# =========================
# PAGE 2: DA PA CHECKER
# =========================
elif p_type == "DA PA":
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        url = st.text_input("Enter Website URL", placeholder="example.com")
        run = st.button("Check DA PA", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    if run:
        if not url.strip(): st.error("URL daalo."); st.stop()
        url = normalize_url(url)
        domain = get_domain(url)
        
        with st.spinner("Analyzing..."):
            page_data = analyze_page(url)
            if "error" in page_data: st.warning(f"⚠️ Direct page fetch blocked by target site. Using available data.")
            
            domain_age = None
            try:
                w = whois.whois(domain)
                cd = w.creation_date
                if isinstance(cd, list): cd = cd[0]
                if cd: domain_age = round((datetime.now() - cd).days / 365.25, 2)
            except: pass
                
            if not domain_age:
                with st.expander("🔧 WHOIS Blocked. Enter Domain Age Manually:", expanded=True):
                    man_age = st.number_input("Domain Age (in years)", min_value=0.0, max_value=30.0, value=1.0, step=0.5)
                    domain_age = man_age if man_age > 0 else None
            
            ssl_ok = check_ssl(domain)
            da = calculate_da(domain_age, ssl_ok, page_data, domain)
            pa = calculate_pa(page_data)

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">DA Score</div><div class="metric-value">{da}</div><div class="small">{score_label(da)}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card"><div class="metric-label">PA Score</div><div class="metric-value">{pa}</div><div class="small">{score_label(pa)}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card"><div class="metric-label">Domain Age</div><div class="metric-value" style="font-size:26px;">{domain_age if domain_age else "N/A"}</div><div class="small">{"Auto" if domain_age else "Manual"}</div></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="metric-card"><div class="metric-label">HTTP/SSL</div><div class="metric-value">{page_data.get("status_code") or "-"}</div><div class="small">SSL: {"Yes" if ssl_ok else "No"}</div></div>', unsafe_allow_html=True)

        d1, d2 = st.columns(2)
        with d1:
            st.markdown('<div class="box">', unsafe_allow_html=True)
            st.write(f"**Title:** {'Yes' if page_data.get('title') else 'No/Blocked'}")
            st.write(f"**Meta Desc:** {'Yes' if page_data.get('meta_description') else 'No/Blocked'}")
            st.write(f"**H1:** {page_data.get('h1_count', 0)} | **H2:** {page_data.get('h2_count', 0)}")
            st.write(f"**Words:** {page_data.get('word_count', 0)}")
            st.markdown('</div>', unsafe_allow_html=True)
        with d2:
            st.markdown('<div class="box">', unsafe_allow_html=True)
            st.write(f"**Internal Links:** {page_data.get('internal_links', 0)}")
            st.write(f"**External Links:** {page_data.get('external_links', 0)}")
            st.write(f"**Images Alt:** {page_data.get('images_missing_alt', 0)}/{page_data.get('images', 0)} missing")
            st.write(f"**Time:** {page_data.get('response_time', 'N/A')}s")
            st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PAGE 3: KEYWORD RESEARCH
# =========================
elif p_type == "Keyword":
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        kw_input = st.text_input("Enter Seed Keyword", placeholder="e.g., best laptops")
        run_kw = st.button("🔍 Find Keywords", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    if run_kw:
        if not kw_input.strip(): st.error("Keyword daalo."); st.stop()
        all_kws = []
        with st.spinner("Fetching from Google Suggest API..."):
            for s in get_google_suggestions(kw_input): all_kws.append({"kw": s, "src": "Auto", "diff": estimate_difficulty(s), "vol": estimate_volume(s)})
            for lt in get_long_tail_variations(kw_input):
                if lt.lower() not in [k["kw"].lower() for k in all_kws]: all_kws.append({"kw": lt, "src": "Long-tail", "diff": estimate_difficulty(lt), "vol": estimate_volume(lt)})
            with st.spinner("Fetching related from Bing..."):
                for rel in get_related_searches_bing(kw_input):
                    if rel.lower() not in [k["kw"].lower() for k in all_kws]: all_kws.append({"kw": rel, "src": "Related", "diff": estimate_difficulty(rel), "vol": estimate_volume(rel)})
        
        if not all_kws: st.warning("No keywords found.")
        else:
            for k in all_kws:
                dt, dc = difficulty_label(k["diff"])
                st.markdown(f'<div class="kw-box"><div><div class="kw-text">{k["kw"]}</div><div class="small">{k["src"]}</div></div><div style="display:flex;gap:10px;"><div class="small">~{k["vol"]:,}</div><div class="kw-badge" style="color:{dc};background:{dc}22;">{dt}</div></div></div>', unsafe_allow_html=True)

# =========================
# PAGE 4: ARTICLE WRITER
# =========================
elif p_type == "Article":
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        a_kw = st.text_input("Topic", placeholder="how to start blogging")
        o1, o2 = st.columns(2)
        with o1: tone = st.selectbox("Tone", ["Professional", "Casual", "Informative"])
        with o2: length = st.selectbox("Length", ["Short", "Medium", "Long"])
        run_a = st.button("✍️ Generate", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    if run_a:
        if not a_kw.strip(): st.error("Topic daalo."); st.stop()
        with st.spinner("Writing..."):
            html = generate_article_template(a_kw, tone, length)
        st.success(f"Done! ({count_words(html)} words)")
        st.markdown(f'<div class="article-output">{html}</div>', unsafe_allow_html=True)
        st.download_button("📥 Download TXT", re.sub(r'<[^>]+>', '\n', html), f"{a_kw}.txt")

st.markdown("---")
st.markdown('<div style="text-align:center; color:#444; font-size:12px;">Built with ❤️ | Cloud Optimized SEO Tool Box</div>', unsafe_allow_html=True)
