import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI SEO Automation Tool")

topic = st.text_input("Enter Topic")

if st.button("Generate SEO Content"):

    if topic == "":
        st.warning("Please enter a topic")
    else:

        # Keywords
        keyword_prompt = f"Generate 10 SEO keywords for {topic}"

        keywords = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": keyword_prompt}]
        )

        # Meta Description
        meta_prompt = f"Write an SEO meta description for {topic}"

        meta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": meta_prompt}]
        )

        # Article Outline
        outline_prompt = f"Create a blog article outline about {topic}"

        outline = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": outline_prompt}]
        )

        st.subheader("SEO Keywords")
        st.write(keywords.choices[0].message.content)

        st.subheader("Meta Description")
        st.write(meta.choices[0].message.content)

        st.subheader("Article Outline")
        st.write(outline.choices[0].message.content)
