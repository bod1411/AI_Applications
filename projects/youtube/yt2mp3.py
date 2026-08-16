import streamlit as st
import yt_dlp
import os
from pathlib import Path
import tempfile

# Page configuration
st.set_page_config(
    page_title="YouTube Downloader - MP4 & MP3",
    page_icon="🎵",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF0000;
        color: white;
        height: 3rem;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #CC0000;
    }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.title("🎵 YouTube Downloader - MP4 & MP3")
st.markdown("Download YouTube videos as **MP4 video** or **MP3 audio** in highest quality")
st.markdown("---")

# Use user's Downloads folder (works on both Windows and Mac)
DOWNLOAD_FOLDER = str(Path.home() / "Downloads" / "YouTube")

# Create directory with error handling
try:
    Path(DOWNLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
except (FileNotFoundError, OSError):
    # Fallback to temp directory if creation fails
    DOWNLOAD_FOLDER = tempfile.mkdtemp(prefix='youtube_downloads_')
    st.warning(f"Using temporary folder for downloads: {DOWNLOAD_FOLDER}")

# Create a dedicated temp folder for yt-dlp's temporary files (reuse across reruns)
if 'temp_folder' not in st.session_state:
    st.session_state.temp_folder = tempfile.mkdtemp(prefix='yt_dlp_temp_')
    # Set environment variables for temp directory
    os.environ['TMPDIR'] = st.session_state.temp_folder  # Unix
    os.environ['TEMP'] = st.session_state.temp_folder    # Windows
    os.environ['TMP'] = st.session_state.temp_folder     # Windows

TEMP_FOLDER = st.session_state.temp_folder

# Input field for YouTube URL
url = st.text_input(
    "Enter YouTube URL:",
    placeholder="https://www.youtube.com/watch?v=...",
    help="Paste the full YouTube video URL here"
)

# Format selector
format_choice = st.radio(
    "Choose download format:",
    options=["MP4 (Video)", "MP3 (Audio Only)"],
    horizontal=True,
    help="MP4 includes video and audio, MP3 is audio only"
)

# Download button
if st.button("⬇️ Download", type="primary"):
    if not url:
        st.error("❌ Please enter a YouTube URL!")
    elif 'youtube.com' not in url and 'youtu.be' not in url:
        st.error("❌ Please enter a valid YouTube URL!")
    else:
        try:
            # Determine if MP3 or MP4
            is_mp3 = "MP3" in format_choice

            # Show progress
            progress_text = "🔄 Downloading and converting to MP3..." if is_mp3 else "🔄 Downloading video..."
            with st.spinner(progress_text):

                # Configure yt-dlp options based on format
                if is_mp3:
                    # MP3 audio extraction configuration
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'outtmpl': os.path.abspath(os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')),
                        'paths': {
                            'home': os.path.abspath(DOWNLOAD_FOLDER),
                            'temp': os.path.abspath(TEMP_FOLDER)
                        },
                        'ffmpeg_location': r'C:\ffmpeg\bin',
                        'quiet': True,
                        'no_warnings': True,
                        'progress_hooks': [],
                        'prefer_ffmpeg': True,
                    }
                else:
                    # MP4 video configuration (original)
                    ydl_opts = {
                        'format': 'best[ext=mp4]/best',  # Download pre-merged MP4 (no ffmpeg needed)
                        'outtmpl': os.path.abspath(os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')),
                        'paths': {
                            'home': os.path.abspath(DOWNLOAD_FOLDER),
                            'temp': os.path.abspath(TEMP_FOLDER)
                        },
                        'quiet': True,
                        'no_warnings': True,
                        'progress_hooks': [],
                    }

                # Download the video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_title = info.get('title', 'video')
                    filename = ydl.prepare_filename(info)

                    # For MP3, the extension changes after post-processing
                    if is_mp3:
                        filename = os.path.splitext(filename)[0] + '.mp3'

                    file_size = os.path.getsize(filename) / (1024 * 1024)  # Convert to MB

                st.success(f"✅ **Download Complete!**")

                # Display file information
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Title", video_title[:30] + "..." if len(video_title) > 30 else video_title)
                with col2:
                    st.metric("File Size", f"{file_size:.2f} MB")

                # Provide download button with appropriate format
                # Read file content into memory to avoid 0-byte downloads
                with open(filename, 'rb') as file:
                    file_data = file.read()

                # Set button label and MIME type based on format
                if is_mp3:
                    button_label = "💾 Download MP3 File"
                    mime_type = "audio/mpeg"
                else:
                    button_label = "💾 Download MP4 File"
                    mime_type = "video/mp4"

                st.download_button(
                    label=button_label,
                    data=file_data,
                    file_name=os.path.basename(filename),
                    mime=mime_type,
                    use_container_width=True
                )

                st.info(f"📁 File saved to: `{filename}`")

        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ **Error:** {error_msg}")

            # Provide specific troubleshooting tips
            if "Access is denied" in error_msg or "WinError 5" in error_msg:
                st.warning("""
                🔧 **Access Denied Error - Try these solutions:**

                1. **Check FFmpeg Installation:**
                   - Run in terminal: `ffmpeg -version`
                   - If not found, install FFmpeg: `winget install ffmpeg` or download from https://ffmpeg.org

                2. **Run Streamlit as Administrator:**
                   - Right-click Command Prompt → "Run as administrator"
                   - Navigate to your folder and run: `streamlit run yt2mp3.py`

                3. **Change Download Folder:**
                   - Close any programs that might be accessing the Downloads folder
                   - Try using a different folder (e.g., Desktop)
                """)
            elif "ffmpeg" in error_msg.lower():
                st.warning("⚠️ FFmpeg is required for MP3 conversion. Install it with: `winget install ffmpeg`")
            else:
                st.info("💡 **Tip:** Make sure the URL is correct and the video is publicly available.")

# Add footer with instructions
st.markdown("---")
st.markdown("""
### How to use:
1. Copy a YouTube video URL
2. Paste it in the text box above
3. Choose your preferred format (MP4 or MP3)
4. Click the **Download** button
5. Wait for the download to complete
6. Click the download button to save the file to your computer

### Features:
- ✅ MP4 video (highest quality with audio)
- ✅ MP3 audio extraction (192 kbps)
- ✅ No registration required
- ✅ Free and open source
""")

# Sidebar with additional info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This app uses **yt-dlp** to download YouTube content in the highest quality available.

    **No AI or LLM models needed!**

    **MP4 Mode:**
    - Selects best quality video
    - Includes audio
    - Merges into single MP4 file

    **MP3 Mode:**
    - Extracts best quality audio
    - Converts to MP3 format
    - 192 kbps bitrate
    """)

    st.markdown("---")
    st.markdown("**Note:** Please respect copyright laws and YouTube's Terms of Service.")
