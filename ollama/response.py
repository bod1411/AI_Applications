from ollama import chat

messages = [
  {
    'role': 'user',
    'content': 'What is 10 + 23?',
  },
]

response = chat('llama3.1:8b', messages=messages)
print('Response:\n========\n\n' + response.message.content)