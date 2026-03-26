import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="AI SEO Automation Tool",
    page_icon="🚀",
    layout="wide"
)

# -------- Custom CSS --------
st.markdown("""
<style>

.main-title{
font-size:48px;
font-weight:700;
text-align:center;
background: linear-gradient(90deg,#00c6ff,#0072ff);
-webkit-background-clip:text;
color:transparent;
}

.subtitle{
text-align:center;
color:gray;
margin-bottom:40px;
}

.card{
padding:20px;
border-radius:10px;
background:#111827;
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# -------- Header --------
st.markdown('<div class="main-title">AI SEO Automation Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate SEO Keywords, Articles & Content Ideas Instantly</div>', unsafe_allow_html=True)

# -------- Theme Toggle --------
theme = st.toggle("🌙 Dark Mode")

# -------- Sidebar --------
st.sidebar.title("Tools")

uploaded_image = st.sidebar.file_uploader(
    "Upload Image (optional)", type=["png","jpg","jpeg"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.sidebar.image(image, caption="Uploaded Image")

# -------- Topic Input --------
topic = st.text_input("Enter Topic")

generate = st.button("Generate SEO Content")

if generate:

    if topic == "":
        st.warning("Please enter a topic")

    else:

        keywords = [
            f"best {topic}",
            f"{topic} tutorial",
            f"{topic} guide",
            f"{topic} examples",
            f"{topic} tools"
        ]

        meta = f"Learn everything about {topic}. Complete guide, tools, and examples."

        outline = [
            f"What is {topic}",
            f"Benefits of {topic}",
            f"Best {topic} tools",
            f"How to use {topic}",
            f"Future of {topic}"
        ]

        article = f"""
Introduction

{topic} is becoming increasingly important in modern technology.

What is {topic}

{topic} refers to tools that improve productivity and automate tasks.

Benefits of {topic}

Using {topic} helps businesses and individuals work faster.

Future of {topic}

The future of {topic} looks promising with AI and automation growth.
"""

        # -------- SEO Score --------
        seo_score = 85

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

            st.subheader("SEO Score")
            st.progress(seo_score)

        st.subheader("Generated Article")
        st.write(article)

        # -------- Download Button --------
        st.download_button(
            label="Download Article",
            data=article,
            file_name="seo_article.txt"
        )
