
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")


client = InferenceClient(
    provider="fireworks-ai",
    api_key=hf_token,
)

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1-0528",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)

print(completion.choices[0].message)