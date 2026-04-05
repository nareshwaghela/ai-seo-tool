import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Press Release - Coozmoo Digital Solutions", page_icon="📰", layout="wide")

# =========================
# ISSUEWIRE EXACT CSS THEME (Clean News Style)
# =========================
st.markdown("""
<style>
    /* Hide Streamlit Defaults */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    .stApp { background-color: #f4f5f7; }
    div[data-testid="stVerticalBlock"] > div > div { gap: 0px; }
    
    /* Top Navigation Bar */
    .news-nav {
        background: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        padding: 15px 5%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .news-logo {
        font-size: 28px;
        font-weight: 800;
        color: #1a73e8;
        font-family: 'Arial', sans-serif;
        letter-spacing: -0.5px;
    }
    .news-logo span { color: #333; }
    .nav-menu { display: flex; gap: 25px; align-items: center; }
    .nav-menu a {
        color: #555; text-decoration: none; font-size: 15px; font-weight: 500;
        transition: color 0.2s;
    }
    .nav-menu a:hover { color: #1a73e8; }
    .btn-submit-pr {
        background: #1a73e8; color: white; padding: 8px 20px; border-radius: 4px;
        text-decoration: none; font-weight: 600; font-size: 14px;
    }
    .btn-submit-pr:hover { background: #1557b0; }

    /* Main Container */
    .main-container {
        max-width: 1200px;
        margin: 30px auto;
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 30px;
        padding: 0 5%;
    }
    @media (max-width: 900px) {
        .main-container { grid-template-columns: 1fr; }
    }

    /* Article Card (Left Side) */
    .article-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 40px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .breadcrumb {
        font-size: 13px; color: #666; margin-bottom: 20px;
    }
    .breadcrumb a { color: #1a73e8; text-decoration: none; }
    
    .article-title {
        font-size: 32px; font-weight: 700; color: #222; line-height: 1.3;
        font-family: 'Georgia', serif; margin-bottom: 15px;
    }
    .article-meta {
        display: flex; gap: 20px; font-size: 14px; color: #777; 
        border-bottom: 1px solid #eee; padding-bottom: 15px; margin-bottom: 25px;
    }
    .article-meta strong { color: #444; }
    
    .article-content {
        font-size: 16px; line-height: 1.8; color: #333; text-align: justify;
        font-family: 'Georgia', serif;
    }
    .article-content p { margin-bottom: 20px; }
    
    .company-logo-box {
        float: right; margin: 0 0 20px 25px; width: 150px; height: 150px;
        background: #f9f9f9; border: 1px solid #eee; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        color: #aaa; font-size: 12px; text-align: center; padding: 10px;
    }
    
    .tags-box {
        margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;
    }
    .tag {
        background: #eef2ff; color: #1a73e8; padding: 5px 12px; border-radius: 20px;
        font-size: 13px; display: inline-block; margin-right: 8px; margin-bottom: 8px;
        text-decoration: none;
    }
    .tag:hover { background: #1a73e8; color: white; }
    
    .share-box {
        display: flex; gap: 10px; margin-top: 25px; align-items: center;
    }
    .share-btn {
        width: 40px; height: 40px; border-radius: 50%; display: flex; 
        align-items: center; justify-content: center; color: white; font-weight: bold;
        text-decoration: none;
    }
    .fb { background: #1877F2; } .tw { background: #1DA1F2; } .li { background: #0A66C2; } .wa { background: #25D366; }

    /* Sidebar (Right Side) */
    .sidebar {
        display: flex; flex-direction: column; gap: 25px;
    }
    .widget {
        background: #ffffff; border-radius: 8px; padding: 25px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .widget-title {
        font-size: 18px; font-weight: 700; color: #222; margin-bottom: 15px;
        padding-bottom: 10px; border-bottom: 2px solid #1a73e8;
    }
    .recent-pr { margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #eee; }
    .recent-pr:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
    .recent-pr a { color: #333; text-decoration: none; font-weight: 600; font-size: 15px; line-height: 1.4; }
    .recent-pr a:hover { color: #1a73e8; }
    .recent-pr-date { font-size: 12px; color: #888; margin-top: 5px; }
    
    .newsletter-input {
        width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;
        margin-bottom: 10px; box-sizing: border-box;
    }
    .newsletter-btn {
        width: 100%; padding: 10px; background: #1a73e8; color: white;
        border: none; border-radius: 4px; font-weight: 600; cursor: pointer;
    }

    /* Footer */
    .news-footer {
        background: #263238; color: #b0bec5; padding: 30px 5%; text-align: center;
        margin-top: 50px; font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# MOCK DATA
# =========================
recent_prs = [
    {"title": "TechCorp Announces AI Integration in Healthcare Solutions", "date": "Oct 25, 2023"},
    {"title": "Global Finance Forum to be Held in London Next Month", "date": "Oct 24, 2023"},
    {"title": "Eco-Friendly Packaging Startup Raises $20M in Series A", "date": "Oct 23, 2023"},
    {"title": "New Study Reveals Benefits of Remote Work on Mental Health", "date": "Oct 22, 2023"}
]

# =========================
# WEBSITE LAYOUT
# =========================

# 1. Navbar
st.markdown("""
<div class="news-nav">
    <div class="news-logo">Issue<span>Wire</span></div>
    <div class="nav-menu">
        <a href="#">Home</a>
        <a href="#">News</a>
        <a href="#">About</a>
        <a href="#" class="btn-submit-pr">Submit Press Release</a>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Main Grid Container
st.markdown("""
<div class="main-container">
    <!-- LEFT COLUMN: ARTICLE -->
    <div class="article-card">
        <div class="breadcrumb">
            <a href="#">Home</a> &rsaquo; <a href="#">Press Release</a> &rsaquo; <a href="#">Business</a> &rsaquo; Coozmoo Digital Solutions to Launch Digital Marketing Services
        </div>
        
        <h1 class="article-title">Coozmoo Digital Solutions to Launch Digital Marketing Services</h1>
        
        <div class="article-meta">
            <span><strong>Coozmoo Digital Solutions</strong></span>
            <span>October 24, 2023</span>
            <span>New Delhi, India</span>
        </div>
        
        <div class="article-content">
            <div class="company-logo-box">
                [ Company Logo ]<br>Coozmoo Digital
            </div>
            
            <p><strong>New Delhi, India</strong> – Coozmoo Digital Solutions, a rapidly growing digital agency, is proud to announce the official launch of its comprehensive suite of digital marketing services. Aimed at empowering small to medium-sized businesses (SMBs), the new services are designed to increase online visibility, drive targeted traffic, and maximize return on investment (ROI) in the digital landscape.</p>
            
            <p>In today’s highly competitive market, having a robust online presence is no longer optional; it is a critical necessity. Recognizing the challenges that many businesses face in navigating the complex world of SEO, social media, and paid advertising, Coozmoo Digital Solutions has curated a team of industry experts to deliver tailored strategies.</p>
            
            <p>"Our mission is to bridge the gap between traditional business practices and modern digital execution," said the Founder & CEO of Coozmoo Digital Solutions. "We don't just provide generic marketing packages; we dive deep into data analytics and consumer behavior to create campaigns that actually convert. Whether a business is looking to rank higher on Google or build a loyal community on social media, we have the tools and expertise to make it happen."</p>
            
            <p>The newly launched services include advanced Search Engine Optimization (SEO), Pay-Per-Click (PPC) advertising management, Social Media Marketing (SMM), Content Strategy, and Web Development. What sets Coozmoo apart is their commitment to complete transparency, providing clients with detailed monthly reports and real-time dashboards to track campaign performance.</p>
            
            <p>Furthermore, Coozmoo Digital Solutions is offering an initial free website audit and consultation for businesses looking to understand their current digital standing. This initiative reflects their confidence in delivering value from day one.</p>
            
            <p>For more information about Coozmoo Digital Solutions and their newly launched services, visit their official website or contact their support team.</p>
        </div>
        
        <div class="tags-box">
            <strong style="color:#333; margin-right:10px;">Tags:</strong>
            <a href="#" class="tag">Digital Marketing</a>
            <a href="#" class="tag">SEO</a>
            <a href="#" class="tag">Coozmoo Digital</a>
            <a href="#" class="tag">Business Growth</a>
            <a href="#" class="tag">Press Release</a>
        </div>
        
        <div class="share-box">
            <span style="font-weight:600; color:#555; font-size:15px;">Share:</span>
            <a href="#" class="share-btn fb">f</a>
            <a href="#" class="share-btn tw">𝕏</a>
            <a href="#" class="share-btn li">in</a>
            <a href="#" class="share-btn wa">✈</a>
        </div>
    </div>

    <!-- RIGHT COLUMN: SIDEBAR -->
    <div class="sidebar">
        <!-- Recent PRs Widget -->
        <div class="widget">
            <div class="widget-title">Recent Press Releases</div>
            
            <div class="recent-pr">
                <a href="#">TechCorp Announces AI Integration in Healthcare Solutions</a>
                <div class="recent-pr-date">Oct 25, 2023</div>
            </div>
            <div class="recent-pr">
                <a href="#">Global Finance Forum to be Held in London Next Month</a>
                <div class="recent-pr-date">Oct 24, 2023</div>
            </div>
            <div class="recent-pr">
                <a href="#">Eco-Friendly Packaging Startup Raises $20M in Series A</a>
                <div class="recent-pr-date">Oct 23, 2023</div>
            </div>
            <div class="recent-pr">
                <a href="#">New Study Reveals Benefits of Remote Work on Mental Health</a>
                <div class="recent-pr-date">Oct 22, 2023</div>
            </div>
        </div>

        <!-- Newsletter Widget -->
        <div class="widget">
            <div class="widget-title">Newsletter</div>
            <p style="font-size:14px; color:#666; margin-bottom:15px;">Subscribe to get the latest PR updates directly in your inbox.</p>
            <input type="email" class="newsletter-input" placeholder="Enter your email">
            <button class="newsletter-btn">Subscribe</button>
        </div>

        <!-- Categories Widget -->
        <div class="widget">
            <div class="widget-title">Categories</div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                <a href="#" class="tag">Technology</a>
                <a href="#" class="tag">Business</a>
                <a href="#" class="tag">Health</a>
                <a href="#" class="tag">Finance</a>
                <a href="#" class="tag">Entertainment</a>
                <a href="#" class="tag">Sports</a>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Footer
st.markdown("""
<div class="news-footer">
    <p>© 2023 IssueWire. All rights reserved. | About Us | Contact | Privacy Policy | Terms of Service</p>
</div>
""", unsafe_allow_html=True)
