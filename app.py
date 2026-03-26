import streamlit as st
import random
from PIL import Image

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI SEO Suite",
    page_icon="🚀",
    layout="wide"
)

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align:center;'>🚀 AI SEO Suite</h1>
<p style='text-align:center;'>All-in-one SEO content and analysis toolkit</p>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("SEO Dashboard")

tool = st.sidebar.selectbox(
    "Select Tool",
    [
        "SEO Generator",
        "Blog Title Generator",
        "Keyword Difficulty Checker",
        "Competitor Analysis",
        "AI Article Writer",
        "Image SEO Generator"
    ]
)

# ------------------------------------------------
# SEO GENERATOR
# ------------------------------------------------

if tool == "SEO Generator":

    st.header("SEO Keyword Generator")

    topic = st.text_input("Enter Topic")

    if st.button("Generate Keywords"):

        keywords = [
            f"best {topic}",
            f"{topic} tutorial",
            f"{topic} guide",
            f"{topic} tools",
            f"{topic} tips",
            f"{topic} strategies",
            f"{topic} examples",
            f"{topic} ideas"
        ]

        st.subheader("SEO Keywords")

        for k in keywords:
            st.write("•", k)

# ------------------------------------------------
# BLOG TITLE GENERATOR
# ------------------------------------------------

if tool == "Blog Title Generator":

    st.header("Blog Title Generator")

    topic = st.text_input("Enter Topic")

    if st.button("Generate Titles"):

        titles = [
            f"10 Best {topic} Tips for Beginners",
            f"The Ultimate Guide to {topic}",
            f"How to Master {topic} in 2026",
            f"{topic}: Everything You Need to Know",
            f"Top Strategies for {topic}",
            f"Why {topic} is Important Today"
        ]

        st.subheader("Generated Blog Titles")

        for t in titles:
            st.write("•", t)

# ------------------------------------------------
# KEYWORD DIFFICULTY
# ------------------------------------------------

if tool == "Keyword Difficulty Checker":

    st.header("Keyword Difficulty Checker")

    keyword = st.text_input("Enter Keyword")

    if st.button("Check Difficulty"):

        difficulty = random.randint(20, 90)

        st.subheader("Keyword Difficulty Score")

        st.progress(difficulty)

        st.write(f"Estimated difficulty: **{difficulty}/100**")

# ------------------------------------------------
# COMPETITOR ANALYSIS
# ------------------------------------------------

if tool == "Competitor Analysis":

    st.header("Competitor Content Analysis")

    topic = st.text_input("Enter Topic")

    if st.button("Analyze Competitors"):

        competitors = [
            f"{topic} guide by HubSpot",
            f"{topic} tutorial by Ahrefs",
            f"{topic} strategies by Neil Patel",
            f"{topic} tips by Backlinko"
        ]

        st.subheader("Top Competitor Content")

        for c in competitors:
            st.write("•", c)

# ------------------------------------------------
# ARTICLE WRITER
# ------------------------------------------------

if tool == "AI Article Writer":

    st.header("AI Article Writer")

    topic = st.text_input("Enter Article Topic")

    if st.button("Generate Article"):

        article = f"""
Introduction

{topic} is becoming increasingly important in modern digital marketing.

What is {topic}

{topic} refers to strategies and tools that help businesses grow online.

Benefits of {topic}

Using {topic} can improve productivity, increase traffic, and boost results.

Best Tools

Many tools exist that allow businesses to use {topic} effectively.

Future of {topic}

The future of {topic} looks promising as AI and automation continue to evolve.
"""

        st.subheader("Generated Article")

        editor = st.text_area(
            "Edit Article",
            article,
            height=350
        )

        word_count = len(editor.split())

        st.info(f"Word Count: {word_count}")

        st.download_button(
            "Download Article",
            editor,
            file_name="article.txt"
        )

# ------------------------------------------------
# IMAGE SEO GENERATOR
# ------------------------------------------------

if tool == "Image SEO Generator":

    st.header("Image SEO Generator")

    uploaded = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded:

        img = Image.open(uploaded)

        st.image(img, caption="Uploaded Image")

        captions = [
            "Artificial intelligence technology concept",
            "Digital marketing automation illustration",
            "AI tools and workflow visualization",
            "Modern SEO analytics dashboard"
        ]

        st.subheader("Suggested Image Alt Text")

        st.write(random.choice(captions))
