import streamlit as st
import replicate
import os
from dotenv import load_dotenv
import requests
from pathlib import Path
import time
import tempfile
import zipfile
import io

# Load environment variables
load_dotenv()

# Configure Replicate API
replicate_api_key = os.getenv('REPLICATE_API_KEY')
if replicate_api_key:
    os.environ['REPLICATE_API_TOKEN'] = replicate_api_key

# Model options
MODELS = {
    "Demixing Model": "jimothyjohn/demixing:9e2f68224f32afad8929ca8f20fae238b78ad6ff82af7ea5ac0f526a4a68aea0",
    "MVSep MDX23": "lucataco/mvsep-mdx23-music-separation:510b9b91aec1bfa7d634e6c06ee80c18492fb0fc06aa1474533fbda90dd3dba4"
}

def download_file(url, save_path):
    """Download a file from a URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        st.error(f"Error downloading file: {str(e)}")
        return False

def extract_and_play_zip(zip_url):
    """Download and extract zip file, return audio files for playback"""
    try:
        # Download the zip file
        response = requests.get(zip_url)
        response.raise_for_status()

        # Extract files from zip
        audio_files = {}
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            for file_name in zip_file.namelist():
                # Check if it's an audio file
                if file_name.lower().endswith(('.mp3', '.wav', '.flac', '.m4a', '.ogg')):
                    audio_data = zip_file.read(file_name)
                    audio_files[file_name] = audio_data

        return audio_files
    except Exception as e:
        st.error(f"Error extracting zip file: {str(e)}")
        return None

def process_audio(audio_file, model_choice):
    """Process audio file using selected Replicate model"""
    temp_input = None
    try:
        # Create a temporary file
        temp_fd, temp_path = tempfile.mkstemp(suffix=Path(audio_file.name).suffix)
        temp_input = Path(temp_path)

        # Close the file descriptor and write the uploaded file
        os.close(temp_fd)
        with open(temp_input, "wb") as f:
            f.write(audio_file.read())

        # Get selected model
        model_version = MODELS[model_choice]

        st.info(f"Processing with {model_choice}... This may take a few minutes.")

        # Open the file for Replicate
        with open(temp_input, "rb") as audio:
            # Run the model
            output = replicate.run(
                model_version,
                input={"audio": audio}
            )

        # Clean up temp input file
        if temp_input.exists():
            temp_input.unlink()

        return output

    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        if temp_input and temp_input.exists():
            temp_input.unlink()
        return None

def main():
    st.set_page_config(
        page_title="Vocal & Music Separator",
        page_icon="🎵",
        layout="wide"
    )

    st.title("🎵 Vocal & Music Separator")
    st.markdown("Upload a song and separate vocals from music using AI models")

    # Check API key
    if not replicate_api_key:
        st.error("⚠️ REPLICATE_API_KEY not found in .env file!")
        st.stop()

    # Sidebar for model selection
    with st.sidebar:
        st.header("⚙️ Settings")
        model_choice = st.selectbox(
            "Select Model",
            options=list(MODELS.keys()),
            help="Choose the AI model for separation"
        )

        st.markdown("---")
        st.markdown("### Model Info")
        if model_choice == "Demixing Model":
            st.info("ℹ️ **Demixing Model**\n\nGeneral-purpose music source separation model.")
        else:
            st.info("ℹ️ **MVSep MDX23**\n\nAdvanced music separation using MDX23 architecture.")

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📤 Upload Audio")
        audio_file = st.file_uploader(
            "Choose an audio file",
            type=['mp3', 'wav', 'flac', 'm4a', 'ogg'],
            help="Upload a song file to separate vocals and music"
        )

        if audio_file:
            st.success(f"✅ File uploaded: {audio_file.name}")
            st.audio(audio_file, format=f'audio/{audio_file.name.split(".")[-1]}')

            # File info
            file_size_mb = len(audio_file.getvalue()) / (1024 * 1024)
            st.caption(f"File size: {file_size_mb:.2f} MB")

    with col2:
        st.header("🎧 Results")
        if audio_file:
            if st.button("🚀 Generate Separation", type="primary", use_container_width=True):
                with st.spinner("Processing... Please wait..."):
                    output = process_audio(audio_file, model_choice)

                    if output:
                        st.success("✅ Separation completed!")

                        # Handle different output formats
                        if isinstance(output, dict):
                            # If output is a dictionary with separate tracks
                            st.subheader("Separated Tracks")

                            for key, value in output.items():
                                if value and isinstance(value, str) and value.startswith('http'):
                                    # Check if it's a zip file
                                    if value.lower().endswith('.zip'):
                                        audio_files = extract_and_play_zip(value)
                                        if audio_files:
                                            for file_name, audio_data in audio_files.items():
                                                st.markdown(f"**{file_name}**")
                                                st.audio(audio_data)
                                                st.download_button(
                                                    label=f"💾 Download {file_name}",
                                                    data=audio_data,
                                                    file_name=file_name,
                                                    mime=f"audio/{file_name.split('.')[-1]}"
                                                )
                                                st.markdown("---")
                                    else:
                                        st.markdown(f"**{key.replace('_', ' ').title()}**")
                                        st.audio(value)
                                        st.markdown(f"[Download {key}]({value})")
                                        st.markdown("---")

                        elif isinstance(output, list):
                            # If output is a list of URLs
                            st.subheader("Separated Tracks")
                            track_names = ["Track 1 (Vocals)", "Track 2 (Music)", "Track 3", "Track 4"]

                            for idx, url in enumerate(output):
                                if url and isinstance(url, str):
                                    track_name = track_names[idx] if idx < len(track_names) else f"Track {idx + 1}"

                                    # Check if it's a zip file
                                    if url.lower().endswith('.zip'):
                                        audio_files = extract_and_play_zip(url)
                                        if audio_files:
                                            for file_name, audio_data in audio_files.items():
                                                st.markdown(f"**{file_name}**")
                                                st.audio(audio_data)
                                                st.download_button(
                                                    label=f"💾 Download {file_name}",
                                                    data=audio_data,
                                                    file_name=file_name,
                                                    mime=f"audio/{file_name.split('.')[-1]}"
                                                )
                                                st.markdown("---")
                                    else:
                                        st.markdown(f"**{track_name}**")
                                        st.audio(url)
                                        st.markdown(f"[Download]({url})")
                                        st.markdown("---")

                        elif isinstance(output, str) and output.startswith('http'):
                            # If output is a single URL
                            st.subheader("Result")

                            # Check if it's a zip file
                            if output.lower().endswith('.zip'):
                                st.info("📦 Extracting audio files from zip...")
                                audio_files = extract_and_play_zip(output)
                                if audio_files:
                                    for file_name, audio_data in audio_files.items():
                                        st.markdown(f"**{file_name}**")
                                        st.audio(audio_data)
                                        st.download_button(
                                            label=f"💾 Download {file_name}",
                                            data=audio_data,
                                            file_name=file_name,
                                            mime=f"audio/{file_name.split('.')[-1]}"
                                        )
                                        st.markdown("---")

                                    # Option to download all as zip
                                    st.download_button(
                                        label="📦 Download All (ZIP)",
                                        data=requests.get(output).content,
                                        file_name="separated_audio.zip",
                                        mime="application/zip"
                                    )
                            else:
                                st.audio(output)
                                st.markdown(f"[Download Result]({output})")

                        else:
                            st.warning("Output format not recognized. Raw output:")
                            st.json(output)
        else:
            st.info("👈 Please upload an audio file to get started")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        <p>Powered by Replicate AI | Built with Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
