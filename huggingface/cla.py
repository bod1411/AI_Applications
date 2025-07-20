
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")


client = InferenceClient(
    provider="featherless-ai",
    api_key=hf_token,
)

completion = client.chat.completions.create(
    model="mlfoundations-dev/oh-dcft-v3.1-claude-3-5-sonnet-20241022",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)

print(completion.choices[0].message)