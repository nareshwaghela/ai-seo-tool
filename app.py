import streamlit as st
import random

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI SEO Writer (Free)",
    page_icon="🚀",
    layout="wide"
)

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align:center;'>🚀 AI SEO Writer</h1>
<p style='text-align:center;'>Generate SEO content without API</p>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
tool = st.sidebar.selectbox(
    "Select Tool",
    [
        "SEO Generator",
        "AI Article Writer"
    ]
)

# ---------- SEO GENERATOR ----------
if tool == "SEO Generator":

    st.header("SEO Content Generator")

    topic = st.text_input("Enter Topic")

    if st.button("Generate SEO Content"):

        if topic == "":
            st.warning("Please enter topic")

        else:

            keywords = [
                f"best {topic}",
                f"{topic} tutorial",
                f"{topic} guide",
                f"{topic} tools",
                f"{topic} examples",
                f"{topic} tips",
                f"{topic} strategies"
            ]

            meta = f"Learn everything about {topic}. Complete guide, tips and tools."

            outline = [
                f"What is {topic}",
                f"Benefits of {topic}",
                f"Best {topic} tools",
                f"How to use {topic}",
                f"Future of {topic}"
            ]

            col1,col2 = st.columns(2)

            with col1:

                st.subheader("SEO Keywords")

                for k in keywords:
                    st.write("•",k)

                st.subheader("Meta Description")
                st.write(meta)

            with col2:

                st.subheader("Article Outline")

                for o in outline:
                    st.write("•",o)

# ---------- ARTICLE WRITER ----------
if tool == "AI Article Writer":

    st.header("AI Article Writer")

    topic = st.text_input("Enter Article Topic")

    if st.button("Generate Article"):

        if topic == "":
            st.warning("Enter topic")

        else:

            article = f"""
Introduction

{topic} is becoming increasingly popular in the modern digital world.

What is {topic}

{topic} refers to tools and strategies that help people work more efficiently.

Benefits of {topic}

Using {topic} can save time, increase productivity, and improve results.

Best Tools

Many powerful tools support {topic} and help businesses automate tasks.

How to Use {topic}

To use {topic}, start by identifying your goals and selecting the right tools.

Future of {topic}

The future of {topic} is promising as artificial intelligence and automation continue to grow.
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
