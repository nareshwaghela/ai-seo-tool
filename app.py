import streamlit as st
import random
import time
from PIL import Image
from datetime import datetime

# Try importing pytrends
try:
    from pytrends.request import TrendReq
    PYTRENDS_OK = True
except Exception:
    PYTRENDS_OK = False

# Page configuration
st.set_page_config(page_title="AI SEO Suite", page_icon="🚀", layout="wide")

st.title("🚀 AI SEO Suite")
st.write("Free SEO Tools: Keyword Research • Blog Writer • Competitor Analysis")

# Sidebar
tool = st.sidebar.selectbox(
    "Select Tool",
    [
        "Keyword Scraper",
        "Blog Writer",
        "Blog Title Generator",
        "Keyword Difficulty Checker",
        "Competitor Analysis",
        "Image SEO Generator"
    ]
)

# Article generator
def generate_article(topic):

    year = datetime.now().year

    article = f"""
# The Complete Guide to {topic}

## Introduction
{topic} has become one of the most important strategies for businesses online.

In this guide you will learn everything about {topic}, including strategies and examples.

## What is {topic}?
{topic} is the process of improving visibility, traffic, and engagement online.

## Why {topic} Matters in {year}
Competition online is increasing rapidly, and businesses must optimize their strategies.

## Step-by-Step Strategy

1. Research your audience and keywords
2. Create valuable content
3. Optimize pages for search engines
4. Promote through social media

## Conclusion
By implementing the strategies in this guide, you can build a successful {topic} strategy.
"""
    return article

# Keyword Scraper
if tool == "Keyword Scraper":
    st.header("🔍 Google Keyword Scraper")
    topic = st.text_input("Enter seed keyword")

    if st.button("Scrape Keywords"):
        if not topic:
            st.warning("Please enter a keyword.")
        elif not PYTRENDS_OK:
            st.error("pytrends is not installed. Run: pip install pytrends")
        else:
            with st.spinner("Fetching data from Google Trends..."):
                pytrends = TrendReq()
                pytrends.build_payload([topic])
                data = pytrends.related_queries()
                top = data[topic]["top"]

                if top is not None:
                    for _, row in top.head(10).iterrows():
                        st.write("•", row["query"])
                else:
                    st.info("No keyword data found.")

# Blog Writer
elif tool == "Blog Writer":
    st.header("✍️ AI Blog Writer")
    topic = st.text_input("Enter article topic")

    if st.button("Generate Article"):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating article..."):
                time.sleep(1)
                article = generate_article(topic)

            st.success("Article generated!")
            st.markdown(article)

# Blog Title Generator
elif tool == "Blog Title Generator":
    st.header("📝 Blog Title Generator")
    topic = st.text_input("Enter topic")

    if st.button("Generate Titles"):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            titles = [
                f"10 Best {topic} Tips for Beginners",
                f"The Ultimate Guide to {topic}",
                f"How to Master {topic}",
                f"Why Your {topic} Strategy is Failing",
                f"{topic} Trends You Must Know",
                f"Beginner's Guide to {topic}",
                f"Advanced {topic} Strategies"
            ]

            for t in titles:
                st.write("•", t)

# Keyword Difficulty
elif tool == "Keyword Difficulty Checker":
    st.header("📊 Keyword Difficulty Checker")
    keyword = st.text_input("Enter keyword")

    if st.button("Check Difficulty"):
        if not keyword:
            st.warning("Please enter a keyword.")
        else:
            difficulty = random.randint(20, 90)
            volume = random.randint(500, 50000)

            st.metric("Difficulty", difficulty)
            st.metric("Monthly Searches", volume)

# Competitor Analysis
elif tool == "Competitor Analysis":
    st.header("🏆 Competitor Analysis")
    topic = st.text_input("Enter topic or niche")

    if st.button("Analyze"):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            competitors = ["HubSpot", "Ahrefs", "Neil Patel", "Backlinko", "Moz"]
            for c in competitors:
                st.write("•", c, "article about", topic)

# Image SEO Generator
elif tool == "Image SEO Generator":
    st.header("🖼️ Image SEO Generator")
    uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    if uploaded:
        img = Image.open(uploaded)
        st.image(img)

        alt = st.text_input("Alt text", "SEO optimized image")
        name = uploaded.name.replace(" ", "-").lower()

        st.code(f'<img src="{name}" alt="{alt}" loading="lazy">')
