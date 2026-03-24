import streamlit as st
from seo_tools import generate_keywords, generate_meta_description

st.title("AI SEO Automation Tool")

topic = st.text_input("Enter Topic")

if st.button("Generate SEO Data"):

    keywords = generate_keywords(topic)
    meta = generate_meta_description(topic)

    st.subheader("SEO Keywords")
    st.write(keywords)

    st.subheader("Meta Description")
    st.write(meta)
