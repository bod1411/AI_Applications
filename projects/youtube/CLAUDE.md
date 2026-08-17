# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the Flask web app (serves `templates/index.html` on `http://localhost:5000`):
```bash
python app.py
```

Run the Streamlit MP4 downloader:
```bash
streamlit run yt2mp4.py
```

Run the Streamlit MP4/MP3 downloader (adds an MP3 audio-extraction option):
```bash
streamlit run yt2mp3.py
```

## Architecture

There are two independent, unconnected front ends over `yt-dlp` — they don't share code or call into each other:

- **Flask app** (`app.py` + `templates/index.html`): a JSON API consumed by the bundled HTML/JS page. `POST /download` runs `yt_dlp.YoutubeDL` with `bestvideo+bestaudio` merged to MP4, saving into a temp directory (`%TEMP%/youtube_downloads`). `GET /get-file/<filename>` streams the resulting file back as an attachment. `POST /cleanup` wipes the temp download folder. All download state lives on disk in the temp folder between requests — there's no database or session tracking.
- **Streamlit apps** (`yt2mp4.py`, `yt2mp3.py`): self-contained scripts, each with their own `yt_dlp.YoutubeDL` config, that download straight into `~/Downloads/YouTube` (falling back to a temp dir if that path can't be created) and then hand the file back to the browser via `st.download_button` (loaded fully into memory first, to avoid 0-byte downloads on some setups). `yt2mp3.py` is the superset of `yt2mp4.py`: it adds a format toggle and, for MP3, runs yt-dlp's `FFmpegExtractAudio` postprocessor at 192kbps.

Both Streamlit apps also redirect `TMPDIR`/`TEMP`/`TMP` to a per-session temp folder so yt-dlp's intermediate files don't collide across reruns.

No AI/LLM involved anywhere in this project — it's pure `yt-dlp` wrapping.

## Environment variables

None required — no `.env`/`.env.example` file and no `os.getenv`/`os.environ` reads for configuration in this project.

## Notes

- `yt2mp3.py` hardcodes `ffmpeg_location` to `C:\ffmpeg\bin` — MP3 conversion will fail on any machine without ffmpeg installed at that exact path (the error handling in the script surfaces `winget install ffmpeg` as the suggested fix, but the hardcoded path itself needs to be updated if ffmpeg lives elsewhere, e.g. non-Windows).
- The README documents `streamlit run streamlit_app.py` and `python yttomp4.py` as entrypoints, but no such files exist in this project — the actual Streamlit entrypoints are `yt2mp4.py` and `yt2mp3.py`, and there is no plain CLI script.
- `yt2mp4.py`'s format selector (`best[ext=mp4]/best`) intentionally avoids yt-dlp's separate video+audio merge (unlike `app.py`) so it doesn't require ffmpeg to be installed at all — only the MP3 path in `yt2mp3.py` needs ffmpeg.
