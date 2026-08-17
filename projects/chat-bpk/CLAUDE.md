# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
streamlit run src/app.py
```

## Architecture

Minimal Streamlit chat UI backed by a single OpenAI call, split across two files:

- `src/app.py` — renders the title ("Chat with Munna"), a text input, and a Submit button; on submit it calls `get_response()` from `response.py` and displays the result with `st.write`. There is no conversation history — each submission is a single, independent prompt.
- `src/response.py` — `create_client()` returns an `OpenAI()` client (credentials from environment, loaded via `python-dotenv`'s `load_dotenv()`); `get_response(prompt, model="gpt-4o-mini", max_tokens=150, temperature=0.7)` sends a single-message history to the Chat Completions API and returns the assistant's text.

`src/utils/__init__.py` is intentionally empty — no shared utilities currently exist.

Note `src/app.py` imports with `from response import get_response` (not `from src.response import ...`), so it must be run in a way that puts `src/` on the import path — running `streamlit run src/app.py` from the project root works because Streamlit adds the script's own directory to `sys.path`.

## Environment variables

- `OPENAI_API_KEY` — required, used implicitly by the `openai` client.
