import requests

API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query({
    "inputs": "What is Shock Wave?",
})
print(output[0]['generated_text'])