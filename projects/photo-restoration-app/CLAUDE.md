# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the main app:
```bash
streamlit run app.py
```

Run the alternate "ultra-safe" variant (see Architecture below):
```bash
streamlit run app1.py
```

Verify the Replicate API key / dependencies before launching the app:
```bash
python test_api.py
```

## Architecture

Both `app.py` and `app1.py` are standalone Streamlit apps that follow the same pipeline:

1. User uploads a photo.
2. The image is resized locally (Lanczos resampling) if it exceeds a max-dimension threshold, purely to avoid GPU out-of-memory errors on the Replicate side.
3. `analyze_image_conditions()` (or `analyze_image_simple()` in `app1.py`) inspects the PIL image with `numpy`/`ImageStat` heuristics — no ML model — to detect black-and-white, darkness, damage/noise, blur, and a rough "has faces" signal (skin-tone pixel ratio in the center crop).
4. Based on detected conditions, `select_best_models()` (or `select_safe_model()`) picks one or more entries from a hardcoded `MODELS` catalog of Replicate model IDs (each pinned to a specific version hash).
5. `run_model()` sends the image to Replicate (`replicate.Client(...).run(model_id, input=params)`), downloads the resulting image URL via `requests`, and (in `app.py`) chains up to 3 models sequentially, feeding each model's output into the next.
6. Result and before/after comparison are rendered in Streamlit; the user can override auto-detection and pick a model manually from the sidebar.

`app.py` ("Smart Photo Restoration") is the full-featured version: up to 3 chained models, max dimension 2048px, 15 available models across damage/B&W/face/night categories.

`app1.py` ("Ultra-Safe Photo Restoration") is a deliberately conservative variant: exactly ONE lightweight model per run, max dimension 1200px, upscale always forced to 1x, and a smaller `SAFE_MODELS` subset — written specifically to avoid the GPU OOM errors that `app.py` can still hit on large images.

External dependency: **Replicate API** (all AI models — SwinIR, GFPGAN, DDColor, FLUX Kontext, CodeFormer, Real-ESRGAN, etc. — are hosted there; nothing runs locally).

`MODELS_GUIDE.md` documents a decision tree for manually picking a model per damage type — useful background if changing the auto-detection heuristics.

## Environment Variables

- `REPLICATE_API_KEY` — required. Read via `os.getenv` and copied into `REPLICATE_API_TOKEN` (the variable name the `replicate` SDK actually looks for) before constructing the client.
- `MAX_FILE_SIZE_MB` — optional upload size limit, defaults to 100.

## Notes

- Model IDs in the `MODELS`/`SAFE_MODELS` dicts are pinned to specific version hashes on Replicate; if a model starts failing with "not found," the pinned version has likely been deprecated upstream and needs updating.
- Image resizing happens twice in some paths (once for GPU safety, then again inside `run_model_safe` in `app1.py`) — intentional extra safety margin, not a bug.
