# LangChain Experiments

Small LangChain + local-LLM (Ollama) experiments for note-taking and Q&A.

## Files

- `chatwithnotes.py` — Streamlit app: save free-text notes, then ask questions about them. Uses spaCy embeddings to find the most relevant note chunks, then answers via a local Ollama model (`llama3.1:8b`).
- `prompt.py` — prompt-template experiments.
- `response.py` / `response copy.py` — response-handling experiments.

## Setup

```bash
pip install -r ../../requirements.txt
python -m spacy download en_core_web_md
```

Requires [Ollama](https://ollama.com) running locally with the `llama3.1:8b` model pulled.

## Run

```bash
streamlit run chatwithnotes.py
```
