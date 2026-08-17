# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app (from the `summarizer` project root, not from inside `src/`):
```bash
streamlit run src/app.py
```

## Architecture

Small three-module Streamlit app:

- `src/app.py` — UI only. Takes either pasted text or an uploaded `.docx`/`.pdf` file, and calls into the other two modules.
- `src/summarizer.py` — `summarize_text()` sends the full input text to OpenAI's `gpt-4o-mini` via `client.chat.completions.create()` in a single non-streaming call (`max_tokens=150`), with the entire document interpolated directly into one user message (no chunking — long documents rely on the model's context window, and the 150-token cap means summaries are always short regardless of input length).
- `src/utils/file_handler.py` — `handle_file_upload()` dispatches on file extension: `.docx` via `python-docx` (concatenates paragraph text), `.pdf` via `PyPDF2` (concatenates per-page `extract_text()`). Raises `ValueError` for any other extension.

`app.py` imports `summarizer` and `utils.file_handler` as top-level modules (`from summarizer import ...`, not `from src.summarizer import ...`), which only resolves because Streamlit adds the script's own directory (`src/`) to `sys.path` — this is why the app must be launched as `streamlit run src/app.py` rather than as a package from the repo root.

External dependency: **OpenAI API** (Chat Completions, `gpt-4o-mini`) — no other external service.

## Environment Variables

- `OPENAI_API_KEY` — required, loaded via `python-dotenv` from a `.env` file; consumed implicitly by `OpenAI()` in `summarizer.py`.
