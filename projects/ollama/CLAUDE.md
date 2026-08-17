# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

`requirements.txt` in this folder is empty; install the `ollama` Python package (and `streamlit` for the UI script) via the repo-root requirements instead:
```bash
pip install -r ../../requirements.txt
```

Run individual example scripts directly:
```bash
python async-chat.py    # async chat example
python ps.py             # pulls llama3.2, chats with it, then shows `ollama ps`-style status
python response.py       # simple sync chat example
```

Run the one Streamlit script in this folder:
```bash
streamlit run str_response.py
```

All scripts require a local Ollama server running (`ollama serve`, default `http://localhost:11434`) with the referenced models pulled (`llama3.1:8b` for most scripts, `llama3.2` for `ps.py`).

## Architecture

Each file is an independent, self-contained example against the `ollama` Python client — none import each other:
- `response.py` — synchronous `ollama.chat(model, messages=[...])` one-shot call.
- `async-chat.py` — same idea via `ollama.AsyncClient` and `asyncio.run`.
- `ps.py` — demonstrates the full lifecycle: `pull()` a model with streamed progress events, `chat()` to force it to load, then `ps()` to inspect loaded-model status (digest, VRAM size, expiry, context length).
- `str_response.py` — wraps `ollama.generate(model, prompt)` (the completion-style API, as opposed to `chat`) in a minimal Streamlit text-box UI.

There is no shared module or config between these scripts; each talks directly to the local Ollama daemon over its default REST API.

## Environment Variables

None used — no `.env`/`os.getenv` calls in this folder. Ollama connection defaults to localhost and is not configured via environment variables here.

## Notes

- The README.md in this folder is the generic upstream `ollama-python` examples README and lists many example files (`chat.py`, `chat-stream.py`, `generate.py`, `tools.py`, `multimodal-chat.py`, etc.) that do **not** exist in this folder — only `async-chat.py`, `ps.py`, `response.py`, and `str_response.py` are actually present. Don't trust the README's file list; check the directory contents directly.
- Model names (`llama3.1:8b`, `llama3.2`) are hardcoded per-script, not configurable via args or env vars.
