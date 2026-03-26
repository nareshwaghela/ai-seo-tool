import streamlit as st
from openai import OpenAI

# ---------- CONFIG ----------
st.set_page_config(
    page_title="AI SEO Writer",
    page_icon="🚀",
    layout="wide"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align:center;'>🚀 AI SEO Writer</h1>
<p style='text-align:center;'>Generate SEO articles, keywords and internal links</p>
""", unsafe_allow_html=True)

# ---------- TOOL SELECT ----------
tool = st.sidebar.selectbox(
    "Select Tool",
    [
        "AI Article Writer",
        "SEO Keyword Generator"
    ]
)

# ---------- ARTICLE WRITER ----------
if tool == "AI Article Writer":

    st.header("AI Blog Article Generator")

    topic = st.text_input("Enter Topic")

    if st.button("Generate Article"):

        if topic == "":
            st.warning("Enter topic first")

        else:

            prompt = f"""
Write a 1500 word SEO optimized blog article about:

{topic}

Include:
- introduction
- headings
- internal linking suggestions
- conclusion

Make it blog ready.
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            article = response.choices[0].message.content

            st.subheader("Generated Article")

            edited = st.text_area(
                "Edit Article",
                article,
                height=400
            )

            word_count = len(edited.split())
            st.info(f"Word Count: {word_count}")

            st.download_button(
                "Download Article",
                edited,
                file_name="seo_article.txt"
            )

# ---------- KEYWORD TOOL ----------
if tool == "SEO Keyword Generator":

    st.header("SEO Keyword Generator")

    topic = st.text_input("Enter Keyword Topic")

    if st.button("Generate Keywords"):

        prompt = f"""
Generate 20 SEO keywords for:

{topic}

Return as bullet list.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        keywords = response.choices[0].message.content

        st.subheader("SEO Keywords")

        st.write(keywords)
