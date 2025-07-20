import os
from huggingface_hub import InferenceClient

os.environ["HF_TOKEN"] = "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"

client = InferenceClient(
    provider="featherless-ai",
    api_key=os.environ["HF_TOKEN"],
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