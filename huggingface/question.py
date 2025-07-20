import os
from huggingface_hub import InferenceClient

os.environ["HF_TOKEN"] = "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"

client = InferenceClient(
    provider="groq",
    api_key=os.environ["HF_TOKEN"],
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