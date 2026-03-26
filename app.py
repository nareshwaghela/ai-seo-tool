import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="AI SEO Automation Tool",
    page_icon="🚀",
    layout="wide"
)

# Header
st.markdown(
    """
    <h1 style='text-align: center;'>🚀 AI SEO Automation Tool</h1>
    <p style='text-align: center;'>Generate SEO Keywords, Meta Description and Article Ideas Instantly</p>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.title("AI SEO Tool")
st.sidebar.info("Upload an image or enter a topic to generate SEO content.")

# Image Upload
uploaded_image = st.sidebar.file_uploader(
    "Upload an Image (optional)", type=["png", "jpg", "jpeg"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.sidebar.image(image, caption="Uploaded Image", use_column_width=True)

# Main Input
topic = st.text_input("Enter Topic")

generate = st.button("Generate SEO Content")

if generate:

    if topic == "":
        st.warning("Please enter a topic")
    else:

        # SEO Keywords
        keywords = [
            f"best {topic}",
            f"{topic} tutorial",
            f"{topic} guide",
            f"{topic} examples",
            f"{topic} tools"
        ]

        # Meta description
        meta = f"Learn everything about {topic}. Complete guide, tools, and examples."

        # Outline
        outline = [
            f"What is {topic}",
            f"Benefits of {topic}",
            f"Best {topic} tools",
            f"How to use {topic}",
            f"Future of {topic}"
        ]

        # Article
        article = f"""
Introduction

{topic} is becoming increasingly important in modern technology.

What is {topic}

{topic} refers to tools and technologies that help automate tasks and improve productivity.

Benefits of {topic}

Using {topic} can improve efficiency and save time.

Best Tools

Many powerful tools related to {topic} are available today.

Future of {topic}

The future of {topic} looks promising as AI continues to evolve.
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
