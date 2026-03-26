import streamlit as st
from PIL import Image
import random

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI SEO Automation Platform",
    page_icon="🚀",
    layout="wide"
)

# ---------------- Header ----------------
st.markdown("""
<h1 style='text-align:center;'>🚀 AI SEO Automation Platform</h1>
<p style='text-align:center;'>AI powered SEO content, keyword research and analysis tools</p>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.title("Dashboard")

menu = st.sidebar.selectbox(
    "Select Tool",
    ["SEO Generator", "Keyword Research", "Image Caption AI", "SEO Score Analyzer"]
)

# ---------------- SEO GENERATOR ----------------
if menu == "SEO Generator":

    st.header("SEO Content Generator")

    topic = st.text_input("Enter Topic")

    if st.button("Generate SEO Content"):

        if topic == "":
            st.warning("Please enter a topic")

        else:

            keywords = [
                f"best {topic}",
                f"{topic} tutorial",
                f"{topic} guide",
                f"{topic} tools",
                f"{topic} examples"
            ]

            meta = f"Learn everything about {topic}. Complete guide, tips and tools."

            outline = [
                f"What is {topic}",
                f"Benefits of {topic}",
                f"Best {topic} tools",
                f"How to use {topic}",
                f"Future of {topic}"
            ]

            article = f"""
Introduction

{topic} is becoming increasingly important in modern digital workflows.

What is {topic}

{topic} refers to technologies and tools that help automate processes.

Benefits of {topic}

Using {topic} improves productivity and efficiency.

Best Tools

Many tools exist that help users apply {topic} effectively.

Future of {topic}

The future of {topic} is promising with AI and automation.
"""

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("SEO Keywords")

                for k in keywords:
                    st.write("•", k)

                st.subheader("Meta Description")
                st.write(meta)

            with col2:

                st.subheader("Article Outline")

                for o in outline:
                    st.write("•", o)

            st.subheader("Generated Article")

            st.write(article)

            st.download_button(
                label="Download Article",
                data=article,
                file_name="seo_article.txt"
            )

# ---------------- KEYWORD RESEARCH ----------------
if menu == "Keyword Research":

    st.header("Keyword Research Tool")

    keyword = st.text_input("Enter keyword")

    if st.button("Generate Keywords"):

        suggestions = [
            f"{keyword} tools",
            f"{keyword} tutorial",
            f"{keyword} guide",
            f"{keyword} examples",
            f"{keyword} tips"
        ]

        difficulty = random.randint(20, 80)

        st.subheader("Keyword Suggestions")

        for s in suggestions:
            st.write("•", s)

        st.subheader("Keyword Difficulty")

        st.progress(difficulty)

# ---------------- IMAGE CAPTION AI ----------------
if menu == "Image Caption AI":

    st.header("AI Image Caption Generator")

    uploaded = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded:

        img = Image.open(uploaded)

        st.image(img, caption="Uploaded Image")

        captions = [
            "Artificial intelligence technology illustration",
            "Digital automation concept",
            "AI tools workflow visualization"
        ]

        st.subheader("Generated Caption")

        st.write(random.choice(captions))

# ---------------- SEO SCORE ANALYZER ----------------
if menu == "SEO Score Analyzer":

    st.header("SEO Score Analyzer")

    article = st.text_area("Paste your article")

    if st.button("Analyze SEO"):

        score = random.randint(60, 95)

        st.subheader("SEO Score")

        st.progress(score)

        if score > 80:
            st.success("Excellent SEO optimization")

        else:
            st.warning("SEO can be improved by adding more keywords")
