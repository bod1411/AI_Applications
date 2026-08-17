# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the video LoRA training pipeline (zips `training_videos/`, uploads, starts a Replicate training run):
```bash
python videofinetune.py
```

Run the headshot (image) LoRA training pipeline (zips `training_images/`, uploads, starts a Replicate training run):
```bash
python headshot_finetune.py
```

Check the status of a headshot training job already in progress:
```bash
python headshot_finetune.py --check <training_id>
```

Generate sample videos from the trained video model (downloads output MP4s to `./generated_videos/`):
```bash
python genhs.py
```

## Architecture

Three independent, standalone scripts (no shared modules) that each talk directly to the Replicate API via the `replicate` Python SDK:

- `videofinetune.py` — collects `.mp4/.mov/.avi` files from `training_videos/`, zips them **flat** (filenames only, no folder paths — Replicate's trainer rejects zips with nested paths), writes the zip to a hardcoded path outside OneDrive (`C:/personel/training_FINAL.zip`) to avoid OneDrive sync interfering with the file handle, then calls `replicate.trainings.create()` against the `zsxkib/hunyuan-video-lora` trainer version, publishing the result to the `bod1411/aman-video` destination model with trigger word `AMANVID`.
- `headshot_finetune.py` — same pattern but for still images (`training_images/`, `.jpg/.png/.webp`), using the `replicate/fast-flux-trainer` version, destination model `bod1411/quest-headshot`, trigger word `QSTSHOT`. Also writes its zip outside OneDrive (`C:/personel`) for the same reason, and supports a `--check <training_id>` CLI flag to poll training status instead of starting a new run.
- `genhs.py` — calls `replicate.run()` against the trained video model (`bod1411/aman-video`) to generate sample videos from text prompts, then downloads the resulting video URL to `./generated_videos/`. Despite the filename, this script generates **videos**, not headshots.

All three scripts auto-prepend the trigger word to a prompt if it's missing, since the destination models only respond correctly to their specific trigger word.

## Environment variables

- `REPLICATE_API_TOKEN` — should be the only required variable, read by the `replicate` SDK.

**Known issue:** `videofinetune.py`, `headshot_finetune.py`, and `genhs.py` currently hardcode the Replicate API token directly in source instead of reading it from the environment. This is a known problem — flag it if you touch these files, but do not fix it as a side effect of an unrelated change.

## Notes

- `training_videos/` contains personal video clips and is tracked in git (not gitignored) — be careful with any operation that would expose or transmit its contents beyond what's already intended.
- Replicate's video/image training endpoints reject zip archives containing folder paths; both training scripts explicitly flatten the archive and verify no `/`, `\`, or `:` appear in the zip's namelist before uploading.
