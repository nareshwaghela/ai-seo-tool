import streamlit as st
from openai import OpenAI

# Load API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI SEO Automation Tool")

topic = st.text_input("Enter Topic")

if st.button("Generate SEO Content"):

    if topic == "":
        st.warning("Please enter a topic")

    else:
        try:

            # SEO Keywords
            keyword_prompt = f"Generate 10 SEO keywords for {topic}"

            keyword_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": keyword_prompt}]
            )

            keywords = keyword_response.choices[0].message.content.split("\n")

            st.subheader("SEO Keywords")
            for k in keywords:
                if k.strip():
                    st.write("•", k)


            # Meta Description
            meta_prompt = f"Write an SEO meta description for {topic}"

            meta_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": meta_prompt}]
            )

            meta = meta_response.choices[0].message.content

            st.subheader("Meta Description")
            st.write(meta)


            # Article Outline
            outline_prompt = f"Create a blog article outline about {topic}"

            outline_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": outline_prompt}]
            )

            outline = outline_response.choices[0].message.content.split("\n")

            st.subheader("Article Outline")
            for o in outline:
                if o.strip():
                    st.write("•", o)


            # Full Article
            article_prompt = f"Write a detailed blog article about {topic} with headings"

            article_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": article_prompt}]
            )

            article = article_response.choices[0].message.content

            st.subheader("Generated Article")
            st.write(article)

        except Exception as e:
            st.error("OpenAI API limit reached or billing not enabled.")
            st.info("Add billing at https://platform.openai.com/account/billing")
