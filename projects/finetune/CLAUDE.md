# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Start a LoRA training run:
```bash
python headshot_finetune.py
```

Check status of a previously started training run:
```bash
python headshot_finetune.py --check <training_id>
```

Generate headshots from the trained model:
```bash
python genhs.py
```

Quick connectivity/diagnostics check against the Replicate API and model:
```bash
python test_api.py
```

`headshot_finetune copy.py` is an earlier variant of `headshot_finetune.py`, not part of the normal workflow.

## Architecture

All scripts talk directly to the Replicate API via the `replicate` SDK — there is no server/UI component.

- `headshot_finetune.py` — zips every image in `training_images/` (skipping non-image files), copies the zip to `C:/personel/training_data.zip` (explicitly done to dodge OneDrive sync issues with the temp file, since this project folder lives under a synced directory), then calls `replicate.trainings.create()` against `replicate/fast-flux-trainer` with a fixed trigger word, step count, and learning rate, creating/updating the destination model `bod1411/quest-headshot`. Supports `--check <training_id>` to poll `replicate.trainings.get()`.
- `genhs.py` — calls `replicate.run()` against the trained destination model (`bod1411/quest-headshot`) with a text prompt that must contain the trigger word `QSTSHOT` (auto-prepended if missing), downloads resulting image URLs into `./generated_images/`.
- `test_api.py` — sanity-checks that the API token works, that the destination model exists, and that the `replicate/fast-flux-trainer` base model is accessible.

Training and generation are coupled only through the shared `DESTINATION_MODEL` name (`bod1411/quest-headshot`) and trigger word (`QSTSHOT`), which must stay in sync between the training script and the generation scripts if either is changed.

## Environment variables

- `REPLICATE_API_TOKEN` — should be the way credentials are supplied, but currently is not (see note below).

## Project-specific notes

- **Hardcoded API token**: `headshot_finetune.py`, `headshot_finetune copy.py`, and `test_api.py` all have a Replicate API token hardcoded directly in source (`REPLICATE_API_TOKEN = "..."`) and then pushed into `os.environ` at import time, instead of being read from `.env`/the environment. This is a known issue — treat the token as compromised even if expired, and do not add new hardcoded tokens when touching these files; the fix (reading from env) has been deliberately left undone.
- **`training_images/` contains personal photos** (selfies, portraits) that are tracked in git — treat this directory as personal data, not sample/test assets.
