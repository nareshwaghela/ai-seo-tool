import streamlit as st

st.title("AI SEO Automation Tool")

topic = st.text_input("Enter Topic")

if st.button("Generate SEO Content"):

    if topic == "":
        st.warning("Please enter a topic")
    else:

        keywords = [
            f"best {topic}",
            f"{topic} tools",
            f"{topic} guide",
            f"{topic} tutorial",
            f"{topic} examples",
        ]

        meta = f"Learn everything about {topic}. Complete guide, tools, and tips."

        outline = [
            f"What is {topic}",
            f"Benefits of {topic}",
            f"Best {topic} tools",
            f"How to use {topic}",
            f"Future of {topic}"
        ]

        st.subheader("SEO Keywords")
        st.write(keywords)

        st.subheader("Meta Description")
        st.write(meta)

        st.subheader("Article Outline")
        st.write(outline)
