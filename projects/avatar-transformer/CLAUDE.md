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

Single-page Streamlit app (`src/app.py`) with a two-step OpenAI pipeline:

1. The user uploads a selfie through `st.file_uploader`.
2. `analyze_face()` sends the image (base64-encoded data URL) to `gpt-4o` via the Chat Completions API with a vision prompt, asking it to describe the subject's facial features for a cartoon transformation.
3. `generate_avatar()` sends a text prompt built from a fixed template (plus the base64 image bytes) to `dall-e-3` via `client.images.generate()` to produce the stylized avatar; the returned image URL is rendered directly in the page.

`src/utils/file_handler.py` (docx/PDF text extraction helpers) is not used by `src/app.py` — it appears to be leftover/unused utility code, not part of the avatar pipeline.

The OpenAI client (`OpenAI()`) picks up credentials from the environment automatically; `.env` is loaded via `python-dotenv` at import time.

## Environment variables

- `OPENAI_API_KEY` — required, used implicitly by the `openai` client.
