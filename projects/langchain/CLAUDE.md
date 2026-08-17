# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This folder has no `requirements.txt` of its own; install from the repo-root one, plus the spaCy model used for similarity search:
```bash
pip install -r ../../requirements.txt
python -m spacy download en_core_web_md
```

Run the main app ("chat with your notes"):
```bash
streamlit run chatwithnotes.py
```

Run the smaller experiment scripts (each is its own standalone Streamlit app):
```bash
streamlit run prompt.py
streamlit run "response copy.py"
streamlit run response.py
```

All of the above require a local Ollama server running with `llama3.1:8b` pulled (`ollama pull llama3.1:8b`).

## Architecture

`chatwithnotes.py` is the main app and works as a simple retrieval-then-generate pipeline over a local flat file:
1. A Streamlit form appends submitted notes to `note.text` in the current working directory (created/read relative to wherever `streamlit run` is invoked from — not an absolute or configurable path).
2. On question submit, the full contents of `note.text` are re-read and split into chunks with LangChain's `RecursiveCharacterTextSplitter` (chunk_size=1000, overlap=150).
3. Each chunk and the question are embedded with spaCy's `en_core_web_md` vectors (`nlp(...).similarity(...)`) — this is the only "retrieval" step; there is no vector store, just an in-memory similarity loop over all chunks every time.
4. The top-3 chunks by similarity score are concatenated and passed, along with the question, into a LangChain `PromptTemplate` + `LLMChain` backed by `langchain.llms.Ollama(model='llama3.1:8b')`.
5. The answer and the per-chunk similarity scores are rendered in the Streamlit UI.

`prompt.py`, `response.py`, and `response copy.py` are smaller, standalone experiments (not imported by `chatwithnotes.py`) showing progressively more LangChain usage: `response.py`/`response copy.py` call `Ollama` directly with no chain, while `prompt.py` wires up a `PromptTemplate` + `LLMChain` around a fixed template.

All four scripts depend on `langchain.llms.Ollama`, which requires a running local Ollama daemon (default `http://localhost:11434`) — there is no cloud/API-key LLM in this folder.

## Environment Variables

None — no `.env` usage in this folder. The only external dependency is the local Ollama server.

## Notes

- `chatwithnotes.py` opens `note.text` in read mode (`open("note.text", 'r')`) on both save and ask, and will raise `FileNotFoundError` if that file doesn't exist yet in the working directory — there's no bootstrap/create-if-missing logic, so a `note.text` file must be created (e.g. by an initial note save with an empty starting file) before it works cleanly.
- The model name `llama3.1:8b` is hardcoded in every script; there's no env var or UI control to change it.
