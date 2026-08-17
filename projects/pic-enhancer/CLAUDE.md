# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

This folder has no single `app.py` — it's a collection of independent Streamlit/Gradio apps and standalone scripts, each launched separately. The README describes only the image-enhancer app and references `app.py`, which does not exist in this folder; the actual entrypoint is `picenhancer.py`.

Image enhancer (the app described in README.md):
```bash
streamlit run picenhancer.py
```

Gradio version of the same enhancer:
```bash
python picenhancer_gradio.py
```

Enhancer variant with an extra "Google Upscaler" model option:
```bash
streamlit run superpic.py
```

Other Streamlit tools in this folder (each independent, each needs `REPLICATE_API_KEY`):
```bash
streamlit run headshot.py       # professional headshot generator (Flux Schnell via Replicate)
streamlit run imagegen.py       # headshot generator using a custom Replicate model (bod1411/quest-headshot)
streamlit run videogen.py       # character-driven video generator (Lightricks LTX-Video)
streamlit run vidgen.py         # fuller video generator studio (multiple video models, cost comparison UI)
streamlit run vocalremover.py   # vocal/music separation (Replicate demixing models)
```

Standalone (non-Streamlit) scripts:
```bash
python testapikey.py       # quick Replicate API key/auth check
python test_setup.py       # checks .env, dependencies, and Replicate connectivity together
python train_rvc_voice.py  # submits an RVC voice-cloning training job to Replicate using my_voice_dataset.zip, then polls until done
```

## Architecture

All apps share the same pattern: load `REPLICATE_API_KEY` from `.env`, copy it into `REPLICATE_API_TOKEN` (what the `replicate` SDK reads), build a `replicate.Client`, and call `client.run(model_id, input={...})` against a hardcoded Replicate model ID (usually pinned to a version hash). Results are URLs or lists of URLs that get downloaded with `requests` and displayed/offered for download.

- `picenhancer.py` / `picenhancer_gradio.py` / `superpic.py`: image upscaling. Primary model is Real-ESRGAN; a pixel-count-based resize step runs client-side before upload to stay under Replicate's GPU memory limits (thresholds vary by requested scale factor: 2x/3x/4x). Falls back to local Lanczos resizing (no API call) if no API key is set or the user selects "Local Enhancement."
- `headshot.py` / `imagegen.py`: text/image-to-headshot generation via different Replicate models (Flux Schnell vs. a custom fine-tuned model). Not image *enhancement* — these generate new images.
- `videogen.py` / `vidgen.py`: text-to-video generation. `vidgen.py` is the more built-out version with a multi-model catalog (`VIDEO_MODELS`) including per-model cost estimates and a "seed" option for character consistency across generations; `videogen.py` is an earlier, single-model (LTX-Video) version that also accepts character reference images and an optional reference video.
- `vocalremover.py`: audio source separation (vocals vs. instrumental), unrelated to image enhancement — handles zipped multi-track output from some separation models.
- `model_config.py`: a standalone reference module (extended video model list, prompt/character templates, error-message lookup tables). Not imported by any other file in this folder — treat it as notes/config scaffolding rather than active code.
- `train_rvc_voice.py`: one-off script (not a web app) that submits a voice-cloning training job to Replicate's Trainings API using `my_voice_dataset.zip` and polls `client.trainings.get()` until it succeeds/fails.

External dependency: **Replicate API** for nearly everything (image upscaling, headshot/video generation, audio separation, voice-model training). `imagegen.py` also lists `openai` in requirements.txt, but current source files only call Replicate, not OpenAI.

## Environment Variables

- `REPLICATE_API_KEY` — required by every app/script in this folder.

## Notes

- `my_voice_dataset/` (several personal audio recordings, ~31MB) and `my_voice_dataset.zip` (~16MB) are tracked in git in this folder. They're personal media used as training input for `train_rvc_voice.py`, not sample/test data — flagging for awareness, not attempting to remove them here.
- The README only documents the image-enhancer app; it doesn't mention headshot/video/vocal-separation tools or `train_rvc_voice.py` at all, and its `app.py` command is stale.
- Several Replicate model IDs are pinned to specific version hashes (e.g. in `MODELS` dicts); if a model call starts returning "not found," the pinned version was likely deprecated upstream.
