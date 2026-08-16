# OpenAI Basics

Minimal example of calling the OpenAI Chat Completions API and keeping a multi-turn conversation history.

## Files

- `response.py` — sends two chained chat messages (`gpt-4o-mini`) and prints each reply, demonstrating how to build up `history` for multi-turn context.

## Setup

```bash
pip install openai python-dotenv
```

Create a `.env` file in this folder with:

```
OPENAI_API_KEY=your_key_here
```

## Run

```bash
python response.py
```
