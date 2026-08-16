# Avatar Transformer

A Streamlit app that turns a selfie into a cartoon/anime-style avatar. It uses GPT-4o (vision) to describe the facial features in the uploaded photo, then DALL-E 3 to generate a stylized avatar from that description.

## How it works

1. Upload a selfie (jpg/png).
2. GPT-4o analyzes the facial features in the image.
3. DALL-E 3 generates a cartoon/anime avatar based on the analysis.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder with:

```
OPENAI_API_KEY=your_key_here
```

## Run

```bash
streamlit run src/app.py
```

## Files

- `src/app.py` — Streamlit UI and OpenAI calls.
- `src/utils/` — helper utilities.
