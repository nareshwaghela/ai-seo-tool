import streamlit as st

st.title("AI SEO Automation Tool")

topic = st.text_input("Enter Topic")

if st.button("Generate SEO Content"):

    if topic == "":
        st.warning("Please enter a topic")

    else:

        keywords = [
            f"best {topic}",
            f"{topic} guide",
            f"{topic} tutorial",
            f"{topic} examples",
            f"{topic} tools"
        ]

        meta = f"Learn everything about {topic}. Complete guide, tools, and tips."

        outline = [
            f"What is {topic}",
            f"Benefits of {topic}",
            f"Best {topic} tools",
            f"How to use {topic}",
            f"Future of {topic}"
        ]

        article = f"""
Introduction

{topic} is becoming increasingly important in modern technology and digital productivity.

What is {topic}

{topic} refers to tools and techniques that help automate tasks and improve efficiency.

Benefits of {topic}

Using {topic} can save time, increase productivity, and simplify complex tasks.

Best Tools

Many tools related to {topic} help individuals and businesses work smarter.

Future of {topic}

The future of {topic} looks promising as AI and automation continue to evolve.
"""

        st.subheader("SEO Keywords")
        for k in keywords:
            st.write("•", k)

        st.subheader("Meta Description")
        st.write(meta)

        st.subheader("Article Outline")
        for o in outline:
            st.write("•", o)

        st.subheader("Generated Article")
        st.write(article)
