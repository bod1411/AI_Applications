import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Method 1: Set API key as environment variable (recommended)
# Add this to your .env file or system environment:
# OPENAI_API_KEY=your_api_key_here

# Method 2: Pass API key directly (less secure)
# client = OpenAI(api_key="your_api_key_here")

# Method 1 - using environment variable
client = OpenAI()  # This will automatically use OPENAI_API_KEY from environment

# Initialize conversation history
history = [
    {
        "role": "user",
        "content": "tell me a joke"
    }
]

# Make the API call - correct method is chat.completions.create
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=history,
    max_tokens=150,
    temperature=0.7
)

# Get the response content
response_content = response.choices[0].message.content
print("First response:", response_content)

# Add the assistant's response to history
history.append({
    "role": "assistant", 
    "content": response_content
})

# Add the next user message
history.append({
    "role": "user", 
    "content": "tell me another"
})

# Make second API call
second_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=history,
    max_tokens=150,
    temperature=0.7
)

second_response_content = second_response.choices[0].message.content
print("Second response:", second_response_content)

# Optional: Add the second response to history for continued conversation
history.append({
    "role": "assistant",
    "content": second_response_content
})