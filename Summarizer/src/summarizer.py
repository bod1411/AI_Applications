import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()  # This will automatically use OPENAI_API_KEY from environment

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Please summarize the following text: {text}"}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()