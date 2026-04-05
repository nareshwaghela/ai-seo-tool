import streamlit as st
from datetime import datetime
import re

st.set_page_config(page_title="Advanced SERP Simulator", page_icon="🔍", layout="wide")

# =========================
# ADVANCED GOOGLE-EXACT CSS
# =========================
st.markdown("""
<style>
    /* Main App Background */
    .stApp { background: linear-gradient(135deg, #0f0f13 0%, #161622 100%); }
    
    /* Form Section Styles */
    .input-label { color: #e0e0e0; font-size: 14px; font-weight: 600; margin-bottom: 6px; display: block; }
    .input-box { 
        width: 100%; padding: 10px 12px; background: rgba(255,255,255,0.05); 
        border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: white;
        font-size: 14px; margin-bottom: 16px; outline: none; transition: 0.2s;
    }
    .input-box:focus { border-color: #f5c542; }
    .input-box::placeholder { color: #666; }
    textarea.input-box { resize: vertical; min-height: 80px; font-family: inherit; }
    
    /* Char Counters */
    .counter-good { color: #4caf50; font-size: 13px; font-weight: 700; float: right; }
    .counter-warn { color: #ff9800; font-size: 13px; font-weight: 700; float: right; }
    .counter-bad { color: #f44336; font-size: 13px; font-weight: 700; float: right; }

    /* STRICT GOOGLE SERP PREVIEW STYLES (Pixel Perfect) */
    .serp-container {
        background: #ffffff;
        padding: 20px 30px;
        border-radius: 8px;
        font-family: arial, sans-serif;
        color: #202124;
        overflow: hidden;
    }
    .g-wrapper-mobile {
        max-width: 380px; /* Mobile Width */
        margin: 0 auto;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        background: #fff;
    }
    .g-wrapper-desktop {
        max-width: 650px; /* Desktop Width */
        margin: 0 auto;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        background: #fff;
    }
    
    /* URL & Breadcrumb */
    .g-url { color: #202124; font-size: 14px; line-height: 1.3; }
    .g-url span { color: #70757a; }
    .g-breadcrumb { color: #70757a; font-size: 12px; margin-bottom: 4px; }
    
    /* Title */
    .g-title { 
        color: #1a0dab; font-size: 20px; font-weight: 400; line-height: 1.3; 
        margin: 4px 0 2px 0; cursor: pointer; font-family: arial, sans-serif;
    }
    .g-title:hover { text-decoration: underline; }
    .g-wrapper-mobile .g-title { font-size: 18px; } /* Slightly smaller on mobile */
    
    /* Description */
    .g-desc { color: #4d5156; font-size: 14px; line-height: 1.58; font-family: arial, sans-serif; }
    .g-date { color: #70757a; font-weight: 700; font-size: 14px; margin-right: 6px; }
    
    /* Sitelinks */
    .g-sitelinks-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 12px 20px;
        margin-top: 14px; padding-top: 10px; border-top: 1px solid #ebebeb;
    }
    .g-sitelink-title { color: #1a0dab; font-size: 14px; margin-bottom: 2px; cursor: pointer; }
    .g-sitelink-url { color: #006621; font-size: 12px; margin-bottom: 2px; }
    .g-sitelink-desc { color: #545454; font-size: 12px; line-height: 1.5; }
    
    /* Hide Streamlit defaults for cleaner look */
    [data-testid="stSidebar"] { display: none; }
    div[data-testid="stVerticalBlock"] > div > div { gap: 0px; }
</style>
""", unsafe_allow_html=True)

# =========================
# HELPER FUNCTIONS
# =========================
def get_color_css(current, max_limit, warn_start=None):
    if not warn_start: warn_start = int(max_limit * 0.85)
    if current <= max_limit and current >= warn_start: return "counter-good"
    elif current > max_limit: return "counter-bad"
    else: return "counter-warn"

def truncate_text(text, limit):
    if len(text) <= limit: return text
    return text[:limit-3] + "..."

# =========================
# UI LAYOUT (Split View)
# =========================
st.markdown("<h1 style='text-align:center; color:#f5c542; font-weight:800;'>Advanced SERP Simulator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#aaa; margin-bottom:30px;'>Exactly like Google. Desktop & Mobile Views.</p>", unsafe_allow_html=True)

col_form, col_preview = st.columns([1, 1.5])

with col_form:
    st.markdown('<div class="input-label">Website URL</div>', unsafe_allow_html=True)
    url_input = st.text_input("url", label_visibility="collapsed", placeholder="https://www.example.com/page", key="url")
    
    st.markdown('<div class="input-label">SEO Title Tag <span class="counter-warn" id="title-counter">0 / 60</span></div>', unsafe_allow_html=True)
    title_input = st.text_input("title", label_visibility="collapsed", placeholder="My Awesome SEO Title (Max 60 Characters)", key="title")
    
    st.markdown(f'<div class="input-label">Meta Description <span class="{get_color_css(len(title_input), 160)}">{len(title_input)} / 160</span></div>', unsafe_allow_html=True)
    desc_input = st.text_area("desc", label_visibility="collapsed", placeholder="Write a compelling summary of your page here...", key="desc", height=90)
    
    with st.expander("Optional: Advanced Snippets", expanded=False):
        date_input = st.date_input("Published Date", value=None, format="MMM DD, YYYY")
        breadcrumb_input = st.text_input("Breadcrumb", placeholder="Home > Blog > Post", key="bread")
        
        st.markdown('<div style="color:#ccc; font-size:13px; margin:10px 0 5px 0;">Sitelinks (Max 4)</div>')
        sl1_t = st.text_input("Sitelink 1 Title", placeholder="About Us", key="sl1t")
        sl1_u = st.text_input("Sitelink 1 URL", placeholder="/about", key="sl1u")
        sl2_t = st.text_input("Sitelink 2 Title", placeholder="Contact", key="sl2t")
        sl2_u = st.text_input("Sitelink 2 URL", placeholder="/contact", key="sl2u")

# Update Title Counter dynamically via HTML injection
title_len = len(title_input)
st.markdown(f"""
<script>
    document.getElementById('title-counter').innerText = '{title_len} / 60';
    document.getElementById('title-counter').className = '{get_color_css(title_len, 60, 50)}';
</script>
""", unsafe_allow_html=True)


with col_preview:
    # Extract domain and path for preview
    clean_url = url_input if url_input else "https://www.example.com/page"
    domain = clean_url.split("//")[-1].split("/")[0]
    path = "/" + "/".join(clean_url.split("//")[-1].split("/")[1:]) if "/" in clean_url.split("//")[-1] else ""
    
    # Format Date
    date_str = ""
    if date_input:
        date_str = date_input.strftime("%b %d, %Y") + " —"

    # Truncate for limits
    disp_title = truncate_text(title_input if title_input else "Your Page Title Will Appear Here", 60)
    disp_desc = truncate_text(desc_input if desc_input else "Your meta description will appear here. Make sure it includes your target keyword and is compelling enough to click.", 160)
    
    # Build Sitelinks HTML
    sitelinks_html = ""
    if sl1_t or sl2_t:
        sitelinks_html = '<div class="g-sitelinks-grid">'
        if sl1_t: sitelinks_html += f'<div><div class="g-sitelink-title">{sl1_t}</div><div class="g-sitelink-url">{domain}{sl1_u}</div></div>'
        if sl2_t: sitelinks_html += f'<div><div class="g-sitelink-title">{sl2_t}</div><div class="g-sitelink-url">{domain}{sl2_u}</div></div>'
        sitelinks_html += '</div>'

    # Build Breadcrumb HTML
    breadcrumb_html = f'<div class="g-breadcrumb">{breadcrumb_input}</div>' if breadcrumb_input else ""

    # -------------------------
    # DESKTOP PREVIEW HTML
    # -------------------------
    desktop_html = f'''
    <div class="g-wrapper-desktop">
        {breadcrumb_html}
        <div class="g-url">{domain} <span>› {path.replace("/", "") if path != "/" else "page"}</span></div>
        <div class="g-title">{disp_title}</div>
        <div class="g-desc">
            <span class="g-date">{date_str}</span>
            {disp_desc}
        </div>
        {sitelinks_html}
    </div>
    '''

    # -------------------------
    # MOBILE PREVIEW HTML
    # -------------------------
    mobile_html = f'''
    <div class="g-wrapper-mobile">
        {breadcrumb_html}
        <div class="g-url">{domain} <span>› {path.replace("/", "") if path != "/" else "page"}</span></div>
        <div class="g-title">{disp_title}</div>
        <div class="g-desc">
            <span class="g-date">{date_str}</span>
            {disp_desc}
        </div>
    </div>
    '''

    st.markdown("### 🖥️ Desktop View", unsafe_allow_html=True)
    st.markdown(desktop_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📱 Mobile View", unsafe_allow_html=True)
    st.markdown(mobile_html, unsafe_allow_html=True)
