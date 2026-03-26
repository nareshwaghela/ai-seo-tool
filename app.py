import streamlit as st
from PIL import Image
import random

st.set_page_config(
    page_title="AI SEO Automation Tool",
    page_icon="🚀",
    layout="wide"
)

# ---------- Header ----------
st.markdown(
"""
<h1 style='text-align:center;'>🚀 AI SEO Automation Tool</h1>
<p style='text-align:center;'>Generate SEO Keywords, Articles & Content Insights</p>
""",
unsafe_allow_html=True
)

# ---------- Sidebar ----------
st.sidebar.title("SEO Tools")

uploaded_image = st.sidebar.file_uploader(
    "Upload Image (optional)", type=["png","jpg","jpeg"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.sidebar.image(image, caption="Uploaded Image")

# ---------- Topic ----------
topic = st.text_input("Enter Topic")

generate = st.button("Generate SEO Content")

if generate:

    if topic == "":
        st.warning("Please enter a topic")

    else:

        # ---------- SEO Keywords ----------
        keywords = [
            f"best {topic}",
            f"{topic} tutorial",
            f"{topic} guide",
            f"{topic} examples",
            f"{topic} tools",
            f"{topic} strategies",
            f"{topic} tips",
            f"{topic} ideas"
        ]

        # ---------- Keyword Difficulty ----------
        keyword_difficulty = random.randint(30,80)

        # ---------- Meta Description ----------
        meta = f"Learn everything about {topic}. Discover tips, strategies and tools."

        # ---------- Outline ----------
        outline = [
            f"What is {topic}",
            f"Benefits of {topic}",
            f"Best {topic} tools",
            f"How to use {topic}",
            f"Future of {topic}"
        ]

        # ---------- AI Article ----------
        article = f"""
Introduction

{topic} is rapidly becoming an important part of modern digital strategy.

What is {topic}

{topic} refers to tools, technologies, and techniques that help people improve productivity and efficiency.

Benefits of {topic}

Using {topic} can help individuals and businesses automate processes, save time, and improve results.

Best Tools

There are many powerful tools available today that support {topic} and help users work smarter.

How to Use {topic}

To start using {topic}, identify your needs, choose the right tools, and implement strategies step by step.

Future of {topic}

The future of {topic} looks promising as AI, automation, and digital transformation continue to evolve.
"""

        # ---------- Competitor Analysis ----------
        competitors = [
            f"{topic} guide by HubSpot",
            f"{topic} tutorial by Ahrefs",
            f"{topic} tips by Neil Patel"
        ]

        col1,col2 = st.columns(2)

        with col1:

            st.subheader("SEO Keywords")

            for k in keywords:
                st.write("•",k)

            st.subheader("Meta Description")

            st.write(meta)

            st.subheader("Keyword Difficulty")

            st.progress(keyword_difficulty)

        with col2:

            st.subheader("Article Outline")

            for o in outline:
                st.write("•",o)

            st.subheader("Competitor Content")

            for c in competitors:
                st.write("•",c)

        st.subheader("Generated Article")

        st.write(article)

        st.download_button(
            label="Download Article",
            data=article,
            file_name="seo_article.txt"
        )
