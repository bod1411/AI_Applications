# AI Applications

A collection of small, independent AI experiments and apps — each one lives in its own folder under `projects/` with its own `requirements.txt`, `.env`, and README.

## Projects

| Project | What it does |
|---|---|
| [avatar-transformer](projects/avatar-transformer) | Turns a selfie into a cartoon/anime avatar (GPT-4o vision + DALL-E 3). |
| [basics](projects/basics) | Small practice scripts (rectangle area, PDF↔Word converter). |
| [chat-bpk](projects/chat-bpk) | Chat app (see project README). |
| [finetune](projects/finetune) | Trains a Replicate LoRA headshot model on personal photos. |
| [huggingface](projects/huggingface) | AI professional headshot generator using Hugging Face Inference API models, plus small HF API test scripts. |
| [langchain](projects/langchain) | "Chat with your notes" app using LangChain + local Ollama + spaCy similarity search. |
| [odyssey-inspired](projects/odyssey-inspired) | Suno song-prompt configs (Odyssey/mythology themed). |
| [ollama](projects/ollama) | Local LLM (Ollama) usage examples. |
| [openai](projects/openai) | Minimal OpenAI Chat Completions multi-turn example. |
| [photo-restoration-app](projects/photo-restoration-app) | Photo restoration app (see project README). |
| [pic-enhancer](projects/pic-enhancer) | Image/photo enhancement tools (see project README). |
| [summarizer](projects/summarizer) | Text summarizer app (see project README). |
| [video-finetune](projects/video-finetune) | Trains a Replicate LoRA video model on personal video clips. |
| [youtube](projects/youtube) | YouTube download/convert app (see project README). |

The `suno-song-creator-plugin/` folder at the repo root is a Claude Code plugin cloned from its own GitHub repo. It is **gitignored** here on purpose — it's not part of this project, just installed alongside it. Don't move it or expect it to show up for anyone else cloning this repo.

## Structure

```
AI_Applications/
  README.md              <- you are here
  .gitignore              <- keeps .env, __pycache__, venvs out of git
  requirements.txt         <- shared/base packages for ad-hoc scripts
  projects/                <- every self-contained app/experiment
    <project-name>/
      README.md
      requirements.txt
      .env                <- per-project secrets, gitignored, never commit
      src/ (or loose .py files)
  suno-song-creator-plugin/ <- separate git repo, don't move/rename
  .claude/, .github/        <- Claude Code / repo tooling config
```

## Setup

Each project manages its own dependencies. From inside a project folder:

```bash
pip install -r requirements.txt
```

Secrets go in a per-project `.env` file (never commit these — see `.gitignore`).

## Notes

- `projects/finetune` and `projects/video-finetune` currently have a Replicate API token hardcoded in source rather than read from `.env` — treat as a known cleanup item even if the token is expired.
- `projects/finetune/training_images` and `projects/video-finetune/training_videos` and `projects/pic-enhancer/my_voice_dataset*` contain personal media files tracked in git — consider moving these out of version control if the repo is ever made public or shared.
