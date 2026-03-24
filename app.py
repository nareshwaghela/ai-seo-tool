import streamlit as st
import openai

openai.api_key = st.secrets["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"]

st.title("AI SEO Automation Tool")

topic = st.text_input("Enter Topic")

if st.button("Generate SEO Data"):

    prompt = f"Generate 5 SEO keywords and a meta description for {topic}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}]
    )

    st.write(response["choices"][0]["message"]["content"])
