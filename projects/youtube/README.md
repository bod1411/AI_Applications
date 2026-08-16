# YouTube Video Downloader

A simple web application to download YouTube videos in the highest quality MP4 format.

## Features

- Download YouTube videos in highest quality MP4
- Clean and modern web interface
- No LLM or AI required - uses yt-dlp library
- Automatic format conversion and merging

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Streamlit App (Recommended - Easiest!)

1. Start the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. Your browser will automatically open to the app

3. Paste a YouTube URL and click "Download Video"

4. Click the download button to save the MP4 file

### Option 2: Flask Web Interface

1. Start the Flask web server:
```bash
python app.py
```

2. Open your browser and go to: `http://localhost:5000`

3. Paste a YouTube URL and click "Download Video"

### Option 3: Command Line

Run the script directly:
```bash
python yttomp4.py
```

Then enter the YouTube URL when prompted.

## How It Works

This application uses **yt-dlp** (a fork of youtube-dl) to:
1. Extract video information from YouTube
2. Download the best quality video and audio streams
3. Merge them into a single MP4 file

**No AI or LLM models needed!** This is pure video downloading functionality.

## Requirements

- Python 3.7+
- yt-dlp
- Flask (for web interface)

## Notes

- Videos are downloaded to a temporary directory
- The app automatically selects the highest quality MP4 format available
- Some videos may take time to download depending on their size and your internet connection
