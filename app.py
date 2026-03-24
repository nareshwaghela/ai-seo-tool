import streamlit as st
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_article(keyword):
    prompt = f"Write a SEO optimized article about {keyword} with headings and FAQs."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

st.title("AI SEO Article Generator")

keyword = st.text_input("Enter Keyword")

if st.button("Generate Article"):
    article = generate_article(keyword)
    st.write(article)
