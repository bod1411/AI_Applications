import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def create_client():
    return OpenAI()  # This will automatically use OPENAI_API_KEY from environment

def get_response(prompt, model="gpt-4o-mini", max_tokens=150, temperature=0.7):
    client = create_client()
    history = [{"role": "user", "content": prompt}]
    
    response = client.chat.completions.create(
        model=model,
        messages=history,
        max_tokens=max_tokens,
        temperature=temperature
    )
    
    response_content = response.choices[0].message.content
    return response_content