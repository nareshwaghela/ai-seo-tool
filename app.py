import streamlit as st
from openai import OpenAI

# Load API key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI SEO Automation Tool")

topic = st.text_input("Enter Topic")

if st.button("Generate SEO Content"):

    if topic == "":
        st.warning("Please enter a topic")

    else:

        keyword_prompt = f"Generate 10 SEO keywords for {topic}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": keyword_prompt}]
        )

        keywords = response.choices[0].message.content

        st.subheader("SEO Keywords")
        st.write(keywords)
