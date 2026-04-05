import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import whois
from datetime import datetime, date
import re
import socket
import ssl

st.set_page_config(page_title="Free DA PA Checker", page_icon="📈", layout="wide")

# =========================
# STYLES
# =========================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0f13 0%, #161622 100%);
        color: white;
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
</style>
""", unsafe_allow_html=True)

# =========================
# HELPERS
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
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
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

    # domain age
    if domain_age:
        if domain_age >= 10:
            score += 25
        elif domain_age >= 5:
            score += 18
        elif domain_age >= 2:
            score += 12
        else:
            score += 6

    # ssl
    if ssl_ok:
        score += 10

    # domain shape
    if len(domain) < 20:
        score += 5
    if "-" not in domain:
        score += 5

    # page health
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
# UI
# =========================
st.markdown('<div class="main-title">📈 Free DA PA Checker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">No API key. No paid Moz nonsense. This gives you a smart estimated DA / PA score based on real on-page and domain signals.</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="box">', unsafe_allow_html=True)
    url = st.text_input("Enter Website URL", placeholder="example.com or https://example.com")

    run = st.button("Check DA PA", use_container_width=True)
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

    st.markdown("### Notes")
    st.caption("This is an estimated DA/PA checker built without any external API. It does not return official Moz scores.")
