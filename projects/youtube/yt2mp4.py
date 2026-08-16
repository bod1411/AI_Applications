import streamlit as st
import yt_dlp
import os
from pathlib import Path
import tempfile

# Page configuration
st.set_page_config(
    page_title="YouTube to MP4 Downloader",
    page_icon="📹",
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
st.title("📹 YouTube to MP4 Downloader")
st.markdown("Download YouTube videos in the **highest quality MP4** format")
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

# Download button
if st.button("⬇️ Download Video", type="primary"):
    if not url:
        st.error("❌ Please enter a YouTube URL!")
    elif 'youtube.com' not in url and 'youtu.be' not in url:
        st.error("❌ Please enter a valid YouTube URL!")
    else:
        try:
            # Show progress
            with st.spinner("🔄 Downloading video... This may take a few minutes."):

                # Configure yt-dlp options
                # Use format that doesn't require ffmpeg (pre-merged videos)
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
                    file_size = os.path.getsize(filename) / (1024 * 1024)  # Convert to MB

                st.success(f"✅ **Download Complete!**")

                # Display video information
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Video Title", video_title[:30] + "..." if len(video_title) > 30 else video_title)
                with col2:
                    st.metric("File Size", f"{file_size:.2f} MB")

                # Provide download button
                # Read file content into memory to avoid 0-byte downloads
                with open(filename, 'rb') as file:
                    file_data = file.read()

                st.download_button(
                    label="💾 Download MP4 File",
                    data=file_data,
                    file_name=os.path.basename(filename),
                    mime="video/mp4",
                    use_container_width=True
                )

                st.info(f"📁 File saved to: `{filename}`")

        except Exception as e:
            st.error(f"❌ **Error:** {str(e)}")
            st.info("💡 **Tip:** Make sure the URL is correct and the video is publicly available.")

# Add footer with instructions
st.markdown("---")
st.markdown("""
### How to use:
1. Copy a YouTube video URL
2. Paste it in the text box above
3. Click the **Download Video** button
4. Wait for the download to complete
5. Click the **Download MP4 File** button to save it to your computer

### Features:
- ✅ Highest quality MP4 format
- ✅ Automatic video + audio merging
- ✅ No registration required
- ✅ Free and open source
""")

# Sidebar with additional info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This app uses **yt-dlp** to download YouTube videos in the highest quality available.

    **No AI or LLM models needed!**

    The app automatically:
    - Selects the best quality video
    - Selects the best quality audio
    - Merges them into a single MP4 file
    """)

    st.markdown("---")
    st.markdown("**Note:** Please respect copyright laws and YouTube's Terms of Service.")
