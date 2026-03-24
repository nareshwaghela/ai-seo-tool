import openai

openai.api_key = "YOUR_API_KEY"

def generate_keywords(topic):
    prompt = f"Generate 10 SEO keywords for {topic}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}]
    )

    return response["choices"][0]["message"]["content"]


def generate_meta_description(topic):
    prompt = f"Write an SEO meta description for {topic}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}]
    )

    return response["choices"][0]["message"]["content"]
