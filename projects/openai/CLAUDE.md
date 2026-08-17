# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dependencies:
```bash
pip install openai python-dotenv
```

Run the example:
```bash
python response.py
```

## Architecture

Single-file script (`response.py`). It instantiates `openai.OpenAI()` (reads the API key from the environment automatically) and makes two sequential calls to `client.chat.completions.create()` using the `gpt-4o-mini` model, manually appending each assistant reply to a local `history` list before the next call — demonstrating how to carry multi-turn context with the Chat Completions API rather than an Assistants/threads API.

## Environment Variables

- `OPENAI_API_KEY` — required, loaded via `python-dotenv` from a `.env` file in this folder.
