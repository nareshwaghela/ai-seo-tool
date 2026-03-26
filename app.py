import streamlit as st
from PIL import Image
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI SEO Automation Platform",
    page_icon="🚀",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;'>🚀 AI SEO Automation Platform</h1>
<p style='text-align:center;'>Generate SEO content, keywords and AI articles</p>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Dashboard")

menu = st.sidebar.selectbox(
    "Select Tool",
    ["SEO Generator", "AI Article Writer"]
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

# ---------------- ARTICLE WRITER ----------------
if menu == "AI Article Writer":

    st.header("AI Article Writer")

    topic = st.text_input("Enter Article Topic")

    if st.button("Generate Article"):

        if topic == "":
            st.warning("Please enter a topic")

        else:

            article = f"""
Introduction

{topic} is becoming increasingly important in modern digital workflows.

What is {topic}

{topic} refers to technologies and tools that help automate processes and improve productivity.

Benefits of {topic}

Using {topic} helps individuals and businesses save time and improve efficiency.

Best Tools

Many tools exist that allow users to apply {topic} effectively in different industries.

Future of {topic}

The future of {topic} looks promising as artificial intelligence and automation continue to grow.
"""

            st.subheader("Generated Article")

            st.write(article)

            st.download_button(
                label="Download Article",
                data=article,
                file_name="ai_article.txt"
            )
