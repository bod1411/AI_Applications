# Video Finetune

Fine-tunes a video LoRA model on Replicate (`zsxkib/hunyuan-video-lora`) using the clips in `training_videos/`, so the model learns to reproduce a specific person in generated video.

## ⚠️ Security note

`videofinetune.py` and `headshot_finetune.py` have a **Replicate API token hardcoded** in the source instead of read from `.env`. Even if that token is expired, treat this as a bug — move it to an environment variable before reusing these scripts.

## Files

- `videofinetune.py` — zips `training_videos/` (flat, no folders) and starts the Replicate training run.
- `headshot_finetune.py` / `genhs.py` — related training/generation scripts.
- `training_videos/` — source video clips used for training (personal data, not meant to be shared).

## Setup

```bash
pip install -r requirements.txt
```

Set `REPLICATE_API_TOKEN` as an environment variable rather than editing the script directly.

## Run

```bash
python videofinetune.py
```
