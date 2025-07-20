import os
from huggingface_hub import InferenceClient

os.environ["HF_TOKEN"] = "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"

client = InferenceClient(
    provider="fireworks-ai",
    api_key=os.environ["HF_TOKEN"],
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