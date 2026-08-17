# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dependencies (this project has no local `requirements.txt`; it uses the repo root one):
```bash
pip install -r ../../requirements.txt
```

Run the scripts:
```bash
python f01.py
streamlit run pdf2word.py
```

`factorial.py` is currently empty (placeholder).

## Architecture

These are unrelated standalone scripts, not a single app:

- `f01.py` — CLI script that prompts for length/width on stdin and prints the rectangle area; validates for negative inputs.
- `pdf2word.py` — Streamlit app with two modes selected via `st.radio`: PDF→Word uses `pdf2docx.Converter` (writes/reads a temp `.pdf`/`.docx` pair on disk, then cleans up), and Word→PDF reads paragraphs with `python-docx` and re-renders them with `fpdf.FPDF` (text is encoded to `latin-1` with `replace`, so non-Latin-1 characters will be lossy/garbled).
- `factorial.py` — empty file, not implemented.

No external AI/API services are used in this project.

## Environment variables

None required.
