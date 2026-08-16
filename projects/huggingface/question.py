
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")


client = InferenceClient(
    provider="groq",
    api_key=hf_token,
)

completion = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)

print(completion.choices[0].message)