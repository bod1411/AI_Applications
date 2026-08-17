# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository structure

This is a monorepo of small, **independent** AI experiments and apps. There is no shared build system, package manager, or test runner at the root — each project under `projects/<name>/` is self-contained with its own `requirements.txt`, `.env`, and README.

```
AI_Applications/
  requirements.txt         <- base packages for ad-hoc root-level scripts only
  projects/
    <project-name>/
      README.md
      requirements.txt
      .env                <- per-project secrets, gitignored, never commit
      src/ (or loose .py files)
  suno-song-creator-plugin/ <- separate git repo, gitignored, don't move/rename
```

Each `projects/*` folder should be treated as its own workspace: read its local `CLAUDE.md`/`README.md` and install its own `requirements.txt` rather than assuming root-level dependencies apply.

## Commands

There is no root-level build/lint/test tooling. Per project, from inside `projects/<name>/`:

```bash
pip install -r requirements.txt
python <entrypoint>.py       # most projects are plain scripts
streamlit run <app>.py       # a few projects (e.g. avatar-transformer) are Streamlit apps
```

Check the individual project's README for its exact entrypoint and run command — they differ per project (see the project table in the root README.md).

## Projects

| Project | What it does |
|---|---|
| avatar-transformer | Selfie → cartoon/anime avatar (GPT-4o vision + DALL-E 3). |
| basics | Small practice scripts (rectangle area, PDF↔Word converter). |
| chat-bpk | Chat app. |
| finetune | Trains a Replicate LoRA headshot model on personal photos. |
| huggingface | AI professional headshot generator via Hugging Face Inference API, plus small HF API test scripts. |
| langchain | "Chat with your notes" app using LangChain + local Ollama + spaCy similarity search. |
| odyssey-inspired | Suno song-prompt configs (Odyssey/mythology themed). |
| ollama | Local LLM (Ollama) usage examples. |
| openai | Minimal OpenAI Chat Completions multi-turn example. |
| photo-restoration-app | Photo restoration app. |
| pic-enhancer | Image/photo enhancement tools. |
| summarizer | Text summarizer app. |
| video-finetune | Trains a Replicate LoRA video model on personal video clips. |
| youtube | YouTube download/convert app. |

## Known issues / things to be careful of

- `projects/finetune` and `projects/video-finetune` currently have a Replicate API token hardcoded in source rather than read from `.env` — treat as a known cleanup item even if the token is expired. Do not add new hardcoded secrets.
- `projects/finetune/training_images`, `projects/video-finetune/training_videos`, and `projects/pic-enhancer/my_voice_dataset*` contain personal media files tracked in git — be careful before making the repo public or sharing it.
- `suno-song-creator-plugin/` is a separately-cloned git repo living at the workspace root, intentionally gitignored. Don't move, rename, or edit it as if it were part of this repo.
