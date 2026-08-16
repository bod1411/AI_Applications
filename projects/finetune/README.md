# Finetune (Headshot LoRA training)

Scripts that fine-tune an image model on Replicate to generate headshots of a specific person, using the photos in `training_images/`.

## ⚠️ Security note

`headshot_finetune.py` and `headshot_finetune copy.py` have a **Replicate API token hardcoded** in the source instead of read from `.env`. Even if that token is expired, treat this as a bug — move it to an environment variable before reusing these scripts.

## Files

- `headshot_finetune.py` — zips `training_images/` and starts a Replicate LoRA training run (`replicate/fast-flux-trainer`).
- `headshot_finetune copy.py` — earlier variant of the same script.
- `genhs.py` — generation script using the trained model.
- `test_api.py` — quick Replicate API connectivity check.
- `training_images/` — source photos used for training (personal data, not meant to be shared).

## Setup

```bash
pip install -r requirements.txt
```

Set `REPLICATE_API_TOKEN` as an environment variable rather than editing the script directly.

## Run

```bash
python headshot_finetune.py
python headshot_finetune.py --check <training_id>
```
