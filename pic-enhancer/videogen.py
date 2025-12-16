import streamlit as st
import os
from PIL import Image
import replicate
from dotenv import load_dotenv
import requests
from io import BytesIO
import base64
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Video Generator - Veo 3.1",
    page_icon="🎬",
    layout="wide"
)

# Initialize API client
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

# Set the API token for Replicate
if REPLICATE_API_KEY:
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY
    replicate_client = replicate.Client(api_token=REPLICATE_API_KEY)
else:
    replicate_client = None

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #9B59B6;
        color: white;
        padding: 0.5rem;
        font-size: 16px;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #8E44AD;
        transform: translateY(-2px);
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Model ID
MODEL_ID = "lightricks/ltx-video:8c47da666861d081eeb4d1261853087de23923a268a69b63febdf5dc1dee08e4"

def generate_video(prompt, character_images=None, reference_video=None, aspect_ratio="16:9", 
                   duration=5, guidance_scale=3.0, num_inference_steps=50, debug=False):
    """
    Generate video using lightricks/ltx-video:8c47da666861d081eeb4d1261853087de23923a268a69b63febdf5dc1dee08e4 model
    Returns: (video_content, error, debug_info)
    """
    debug_info = {}
    try:
        # Prepare input parameters
        input_params = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps
        }
        
        # Add character images if provided
        if character_images and len(character_images) > 0:
            # Convert images to the format expected by the model
            # For multiple images, we'll use the first one as the main reference
            # The model might accept multiple images depending on its implementation
            img_byte_arr = BytesIO()
            character_images[0].save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            input_params["image"] = img_byte_arr
        
        # Add reference video if provided
        if reference_video is not None:
            input_params["video"] = reference_video
        
        # Generate the video
        if replicate_client:
            output = replicate_client.run(
                MODEL_ID,
                input=input_params
            )
        else:
            output = replicate.run(
                MODEL_ID,
                input=input_params
            )

        # Debug: Log the output to understand its format
        debug_info['output_type'] = str(type(output))
        debug_info['output_value'] = str(output)[:500]  # Truncate for safety
        
        if debug:
            print(f"DEBUG - Output type: {type(output)}")
            print(f"DEBUG - Output value: {output}")
        
        # The model returns a single URI string
        video_url = None
        
        if isinstance(output, str):
            # Direct string URL
            video_url = output
            debug_info['extraction_method'] = 'direct_string'
        elif hasattr(output, 'url'):
            # Object with url attribute
            video_url = output.url
            debug_info['extraction_method'] = 'object_attribute'
        elif isinstance(output, dict) and 'url' in output:
            # Dictionary with url key
            video_url = output['url']
            debug_info['extraction_method'] = 'dict_key'
        elif isinstance(output, list) and len(output) > 0:
            # List of URLs (fallback)
            video_url = output[0] if isinstance(output[0], str) else str(output[0])
            debug_info['extraction_method'] = 'list_first_item'
        else:
            # Show detailed error for debugging
            debug_info['extraction_method'] = 'failed'
            return None, f"Unexpected output format. Type: {type(output)}, Value: {str(output)[:200]}", debug_info
        
        if not video_url:
            return None, "Could not extract video URL from output", debug_info

        debug_info['video_url'] = video_url
        
        # Download the video
        if debug:
            print(f"DEBUG - Downloading from: {video_url}")
        
        response = requests.get(video_url, timeout=300)  # 5 minute timeout for large videos
        
        debug_info['http_status'] = response.status_code
        debug_info['content_size'] = len(response.content) if response.status_code == 200 else 0
        
        if response.status_code == 200:
            if debug:
                print(f"DEBUG - Video downloaded successfully, size: {len(response.content)} bytes")
            return response.content, None, debug_info
        else:
            return None, f"Failed to download video: HTTP {response.status_code}", debug_info

    except Exception as e:
        debug_info['error'] = str(e)
        debug_info['error_type'] = type(e).__name__
        return None, str(e), debug_info

# Main app
def main():
    # Initialize session state
    if 'generated_video' not in st.session_state:
        st.session_state.generated_video = None
    if 'video_info' not in st.session_state:
        st.session_state.video_info = {}
    if 'character_images' not in st.session_state:
        st.session_state.character_images = []
    
    st.title("🎬 AI Video Generator - Veo 3.1 Fast")
    st.markdown("### Create cinematic videos with character images and scene descriptions")

    # Sidebar with settings
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        Generate AI videos using Google's Veo 3.1 Fast model.

        **Features:**
        - Text-to-Video Generation
        - Character Image Reference
        - Video-to-Video Transformation
        - Multiple Aspect Ratios
        - Customizable Duration
        - Professional Quality Output
        
        **Model:** Google Veo 3.1 Fast
        """)
        
        st.header("⚙️ Video Settings")
        
        # Aspect ratio selection
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            ["16:9", "9:16", "1:1", "4:3", "3:4"],
            index=0,
            help="Choose the aspect ratio for your video"
        )
        
        # Video duration
        duration = st.slider(
            "Video Duration (seconds)",
            min_value=2,
            max_value=10,
            value=5,
            step=1,
            help="Length of the generated video"
        )
        
        # Guidance scale
        guidance_scale = st.slider(
            "Guidance Scale",
            min_value=1.0,
            max_value=10.0,
            value=3.0,
            step=0.5,
            help="How closely to follow the prompt (higher = more strict)"
        )
        
        # Inference steps
        num_inference_steps = st.slider(
            "Quality Steps",
            min_value=20,
            max_value=100,
            value=50,
            step=10,
            help="More steps = better quality but slower generation"
        )
        
        # Show API key status
        if REPLICATE_API_KEY:
            st.success("✅ Replicate API Key: Connected")
        else:
            st.error("⚠️ Replicate API Key: Not Found")
            st.warning("Please add REPLICATE_API_KEY to your .env file")

        st.header("💡 Pro Tips")
        st.markdown("""
        **For Best Results:**
        - Use clear, high-quality character images
        - Be specific in scene descriptions
        - Include lighting, camera angles, mood
        - Mention character actions and emotions
        - Keep prompts under 200 words
        
        **Example Elements:**
        - Action: "walking", "talking", "running"
        - Setting: "sunny beach", "dark alley"
        - Camera: "close-up", "wide shot"
        - Mood: "dramatic", "comedic", "romantic"
        """)

    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload Assets", "✍️ Scene Description", "🎥 Generated Video"])
    
    # Tab 1: Upload Assets
    with tab1:
        st.subheader("📸 Upload Character Images")
        st.markdown("""
        <div class="info-box">
        Upload images of your characters (actors, actresses, side characters). 
        The AI will use these as reference for generating the video.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Main Characters")
            main_character_files = st.file_uploader(
                "Upload main character images",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
                key="main_chars",
                help="Upload images of your main actors/actresses"
            )
            
            if main_character_files:
                st.write(f"✅ {len(main_character_files)} image(s) uploaded")
                # Display thumbnails
                cols = st.columns(min(len(main_character_files), 3))
                for idx, img_file in enumerate(main_character_files):
                    with cols[idx % 3]:
                        img = Image.open(img_file)
                        st.image(img, caption=f"Character {idx+1}", use_column_width=True)
        
        with col2:
            st.markdown("##### Side Characters (Optional)")
            side_character_files = st.file_uploader(
                "Upload side character images",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
                key="side_chars",
                help="Upload images of supporting characters"
            )
            
            if side_character_files:
                st.write(f"✅ {len(side_character_files)} image(s) uploaded")
                cols = st.columns(min(len(side_character_files), 3))
                for idx, img_file in enumerate(side_character_files):
                    with cols[idx % 3]:
                        img = Image.open(img_file)
                        st.image(img, caption=f"Side Character {idx+1}", use_column_width=True)
        
        # Combine all character images
        all_character_files = []
        if main_character_files:
            all_character_files.extend(main_character_files)
        if side_character_files:
            all_character_files.extend(side_character_files)
        
        # Store in session state
        if all_character_files:
            st.session_state.character_images = [Image.open(f) for f in all_character_files]
        
        st.markdown("---")
        
        # Reference video upload (optional)
        st.subheader("🎞️ Reference Video (Optional)")
        st.markdown("""
        <div class="info-box">
        Upload a reference video to guide the style, motion, or structure of the generated video.
        This is optional but can help achieve specific visual styles.
        </div>
        """, unsafe_allow_html=True)
        
        reference_video = st.file_uploader(
            "Upload reference video",
            type=["mp4", "mov", "avi", "webm"],
            help="Optional: Use an existing video as style reference"
        )
        
        if reference_video:
            st.success(f"✅ Reference video uploaded: {reference_video.name}")
            st.video(reference_video)

    # Tab 2: Scene Description
    with tab2:
        st.subheader("✍️ Describe Your Scene")
        
        # Example prompts
        st.markdown("### 📝 Quick Start Examples")
        col_ex1, col_ex2, col_ex3 = st.columns(3)
        
        with col_ex1:
            if st.button("🎭 Dramatic Scene", use_container_width=True):
                st.session_state.prompt_example = "A dramatic close-up shot of the main character standing in the rain at night, city lights reflecting in puddles. Cinematic lighting with blue and orange tones. The character looks determined, rain dripping down their face. Slow camera push-in. Emotional and intense atmosphere."
        
        with col_ex2:
            if st.button("😄 Comedy Scene", use_container_width=True):
                st.session_state.prompt_example = "A funny scene with the main character slipping on a banana peel in a busy office. Wide shot capturing the entire fall in slow motion. Bright, cheerful lighting. Other characters react with surprise and amusement. Light-hearted and comedic timing."
        
        with col_ex3:
            if st.button("💑 Romantic Scene", use_container_width=True):
                st.session_state.prompt_example = "A romantic sunset scene on a beach with two characters walking hand in hand. Golden hour lighting, warm tones. Gentle waves in the background. Camera tracking shot following the couple. Soft focus, dreamy atmosphere. Both characters smiling and talking."
        
        st.markdown("---")
        
        # Main prompt input
        default_prompt = st.session_state.get('prompt_example', '')
        scene_prompt = st.text_area(
            "Scene Description",
            value=default_prompt,
            height=200,
            placeholder="Describe your scene in detail. Include:\n- Characters and their actions\n- Setting and environment\n- Lighting and mood\n- Camera angles and movement\n- Any specific emotions or atmosphere",
            help="The more detailed your description, the better the results"
        )
        
        # Prompt enhancement tips
        with st.expander("💡 How to Write Great Prompts"):
            st.markdown("""
            **Essential Elements:**
            1. **Characters**: Who is in the scene and what are they doing?
            2. **Setting**: Where does this take place? Time of day?
            3. **Action**: What specific movements or activities occur?
            4. **Camera**: Specify angles (close-up, wide shot, tracking)
            5. **Lighting**: Describe the lighting mood and style
            6. **Emotion**: What's the feeling or atmosphere?
            
            **Good Example:**
            "A suspenseful night scene in a foggy alley. The main character walks slowly forward, 
            looking around nervously. Dim streetlight creates dramatic shadows. Camera follows 
            from behind in a steady tracking shot. Tense, mysterious atmosphere with blue-grey tones."
            
            **Avoid:**
            - Vague descriptions ("something interesting happens")
            - Contradictory instructions
            - Too many unrelated elements
            - Overly complex scenes (keep it focused)
            """)
        
        # Negative prompt (optional)
        with st.expander("🚫 Advanced: Negative Prompt (Optional)"):
            negative_prompt = st.text_area(
                "What to avoid in the video",
                height=100,
                placeholder="Example: blurry, distorted, low quality, shaky camera, bad lighting, unrealistic motion",
                help="Describe what you DON'T want in the video"
            )
        
        # Show character preview
        if st.session_state.character_images:
            st.markdown("---")
            st.markdown(f"### 👥 Characters Selected: {len(st.session_state.character_images)}")
            img_cols = st.columns(min(len(st.session_state.character_images), 4))
            for idx, img in enumerate(st.session_state.character_images[:4]):
                with img_cols[idx]:
                    st.image(img, caption=f"Char {idx+1}", use_column_width=True)
            if len(st.session_state.character_images) > 4:
                st.info(f"+ {len(st.session_state.character_images) - 4} more character(s)")

    # Tab 3: Generated Video
    with tab3:
        st.subheader("🎥 Generate Your Video")
        
        # Show current settings
        with st.expander("⚙️ Current Settings"):
            col_set1, col_set2 = st.columns(2)
            with col_set1:
                st.write(f"**Aspect Ratio:** {aspect_ratio}")
                st.write(f"**Duration:** {duration} seconds")
                st.write(f"**Characters:** {len(st.session_state.character_images)}")
            with col_set2:
                st.write(f"**Guidance Scale:** {guidance_scale}")
                st.write(f"**Quality Steps:** {num_inference_steps}")
                st.write(f"**Reference Video:** {'Yes' if reference_video else 'No'}")
        
        # Debug mode toggle
        debug_mode = st.checkbox("🐛 Enable Debug Mode", help="Shows detailed output information for troubleshooting")
        
        # Generation requirements check
        can_generate = True
        requirements = []
        
        if not scene_prompt or len(scene_prompt.strip()) < 20:
            can_generate = False
            requirements.append("❌ Scene description required (minimum 20 characters)")
        else:
            requirements.append("✅ Scene description provided")
        
        if len(st.session_state.character_images) == 0:
            requirements.append("⚠️ No character images (optional, but recommended)")
        else:
            requirements.append(f"✅ {len(st.session_state.character_images)} character image(s) uploaded")
        
        # Display requirements
        st.markdown("### 📋 Generation Checklist")
        for req in requirements:
            st.markdown(req)
        
        st.markdown("---")
        
        # Generate button
        col_gen, col_clear = st.columns([3, 1])
        
        with col_gen:
            if st.button("🎬 Generate Video", type="primary", disabled=(not can_generate), use_container_width=True):
                if not REPLICATE_API_KEY:
                    st.error("❌ Replicate API key not found! Please add it to your .env file.")
                else:
                    # Prepare reference video if uploaded
                    ref_video_data = None
                    if reference_video:
                        ref_video_data = reference_video
                    
                    with st.spinner("🎬 Generating your video... This may take 2-5 minutes depending on duration and quality settings."):
                        # Progress indicator
                        progress_text = st.empty()
                        progress_bar = st.progress(0)
                        
                        progress_text.text("📤 Uploading assets...")
                        progress_bar.progress(20)
                        
                        progress_text.text("🎨 Processing characters and scene...")
                        progress_bar.progress(40)
                        
                        progress_text.text("🎥 Generating video frames...")
                        progress_bar.progress(60)
                        
                        video_content, error, debug_info = generate_video(
                            prompt=scene_prompt,
                            character_images=st.session_state.character_images if st.session_state.character_images else None,
                            reference_video=ref_video_data,
                            aspect_ratio=aspect_ratio,
                            duration=duration,
                            guidance_scale=guidance_scale,
                            num_inference_steps=num_inference_steps,
                            debug=debug_mode
                        )
                        
                        progress_text.text("✨ Finalizing video...")
                        progress_bar.progress(90)
                        
                        # Display debug info if debug mode is enabled
                        if debug_mode and debug_info:
                            with st.expander("🐛 Debug Information", expanded=True):
                                st.json(debug_info)
                        
                        if error:
                            progress_bar.empty()
                            progress_text.empty()
                            st.error(f"❌ Error generating video: {error}")
                            
                            st.info("💡 Troubleshooting tips:")
                            st.markdown("""
                            - **API Credits**: Ensure you have sufficient Replicate credits
                            - **Prompt Length**: Try shortening your scene description
                            - **Images**: Ensure character images are clear and high-quality
                            - **Duration**: Try reducing video duration to 3-4 seconds
                            - **Quality**: Lower the quality steps to 30-40
                            - **Wait & Retry**: The service might be busy, try again in a minute
                            """)
                        else:
                            progress_bar.progress(100)
                            progress_text.text("✅ Video generated successfully!")
                            time.sleep(1)
                            progress_bar.empty()
                            progress_text.empty()
                            
                            # Save to session state
                            st.session_state.generated_video = video_content
                            st.session_state.video_info = {
                                'duration': duration,
                                'aspect_ratio': aspect_ratio,
                                'prompt': scene_prompt[:100] + "..." if len(scene_prompt) > 100 else scene_prompt
                            }
                            st.success(f"✅ Video generated successfully! ({duration}s, {aspect_ratio})")
                            st.rerun()
        
        with col_clear:
            if st.session_state.generated_video:
                if st.button("🔄 New", help="Clear and generate new video", use_container_width=True):
                    st.session_state.generated_video = None
                    st.session_state.video_info = {}
                    st.rerun()
        
        # Display generated video
        if st.session_state.generated_video:
            st.markdown("---")
            st.markdown("### ✨ Your Generated Video")
            
            # Show video info
            with st.expander("📊 Video Information"):
                st.write(f"**Duration:** {st.session_state.video_info['duration']} seconds")
                st.write(f"**Aspect Ratio:** {st.session_state.video_info['aspect_ratio']}")
                st.write(f"**Prompt:** {st.session_state.video_info['prompt']}")
            
            # Display video
            st.video(st.session_state.generated_video)
            
            # Download button
            st.download_button(
                label="📥 Download Video (MP4)",
                data=st.session_state.generated_video,
                file_name=f"ai_generated_video_{int(time.time())}.mp4",
                mime="video/mp4",
                use_container_width=True
            )
            
            # Social sharing tip
            st.info("💡 Tip: You can share this video on social media or use it in your projects!")

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Made with ❤️ using Streamlit and Google Veo 3.1 Fast AI</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()