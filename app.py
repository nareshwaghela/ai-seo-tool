import streamlit as st

st.title("AI SEO Automation Tool")

topic = st.text_input("Enter Topic")

if st.button("Generate SEO Data"):

    keywords = [
        f"{topic} tutorial",
        f"{topic} guide",
        f"best {topic} tools",
        f"{topic} examples",
        f"{topic} tips"
    ]

    meta = f"Learn about {topic} with this complete guide including tips, tools, and examples."

    st.subheader("SEO Keywords")
    st.write(keywords)

    st.subheader("Meta Description")
    st.write(meta)
