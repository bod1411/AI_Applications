# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the headshot generator app (the real entrypoint — `app.py` in this folder is currently empty):
```bash
streamlit run headshot_generator.py
```

Run the standalone HF Inference API test scripts individually:
```bash
python cla.py        # chat completion via the "featherless-ai" provider
python q.py           # chat completion via the "fireworks-ai" provider
python question.py    # chat completion via the "groq" provider
python response.py    # raw REST call to google/gemma-2-2b-it
```

## Architecture

`headshot_generator.py` is a single-file Streamlit app:
- Loads `HF_TOKEN` via `python-dotenv` and stops immediately with an error if it's missing.
- Presents a sidebar (model choice, style, gender, free-text extra description) and a two-column layout (upload photo / generated result).
- `generate_headshot_prompt()` builds a fixed positive/negative prompt pair per style, then appends the user's optional description text.
- `generate_with_api()` calls `huggingface_hub.InferenceClient(model=model_id, token=HF_TOKEN).text_to_image(...)`, retrying without `negative_prompt` on `TypeError` since not all models accept it. Errors are caught broadly and rendered in the UI with a full traceback expander plus heuristic hints (model/token/rate-limit) based on matching keywords in the exception string.
- The `MODELS` dict hardcodes 4 Hugging Face model IDs (Stable Diffusion XL/2.1/1.5, Realistic Vision V5.1); the README additionally advertises 5 models (Absolute Reality, Portrait+, Epic Realism, Deliberate V2) that are not actually present in this dict — only what's in `MODELS` is selectable in the running app.
- Note: despite the "headshot generator" framing and photo upload UI, the uploaded reference image is never actually sent to the API — generation is pure text-to-image from the constructed prompt, the uploaded photo is only displayed for reference.

`cla.py`, `q.py`, `question.py`, `response.py` are unrelated one-off scripts exercising different ways of hitting the Hugging Face Inference API (different `provider=` backends via `InferenceClient.chat.completions`, and a raw `requests.post` call) — useful as reference snippets, not wired into the Streamlit app.

## Environment Variables

- `HF_TOKEN` — Hugging Face API token, read via `os.getenv("HF_TOKEN")` in every script here. Required for all generation/inference calls.

## Notes

- `app.py` is empty; do not treat it as the entrypoint.
- The project's `requirements.txt` includes a wide set of packages (torch, diffusers, transformers, langchain, spacy, ollama, etc.) inherited from the broader repo template — only a subset (streamlit, huggingface_hub, python-dotenv, Pillow, requests) is actually used by the code in this folder.
