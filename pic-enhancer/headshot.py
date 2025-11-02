import streamlit as st
import os
from PIL import Image
import replicate
from dotenv import load_dotenv
import requests
from io import BytesIO
import base64

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Professional Headshot Generator",
    page_icon="=T",
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
        background-color: #2E86AB;
        color: white;
        padding: 0.5rem;
        font-size: 16px;
    }
    .upload-text {
        text-align: center;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Professional Headshot Model
# Option 1: Flux Schnell (Fast and good quality)
HEADSHOT_MODEL = "black-forest-labs/flux-schnell"

# Option 2: SDXL (Uncomment to use)
# HEADSHOT_MODEL = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"

# Option 3: Flux Dev (Higher quality but slower)
# HEADSHOT_MODEL = "black-forest-labs/flux-dev"

def generate_professional_headshot(image_file, style="professional", num_outputs=1, guidance_scale=3.5, num_steps=4):
    """
    Generate professional headshot using Replicate's Flux model

    Args:
        image_file: PIL Image object
        style: Style of headshot (professional, corporate, casual, etc.)
        num_outputs: Number of variations to generate (1-4)
        guidance_scale: How closely to follow the prompt (1.0-10.0)
        num_steps: Number of inference steps (1-4 for Flux Schnell)

    Returns:
        List of enhanced images or error
    """
    try:
        # Convert PIL image to base64 data URI
        img_byte_arr = BytesIO()
        image_file.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        data_uri = f"data:image/png;base64,{img_base64}"

        # Prepare input parameters
        input_params = {
            "image": data_uri,  # Use base64 data URI instead of BytesIO
            "num_outputs": num_outputs,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_steps,  # Flux Schnell supports max 4 steps
            "prompt": f"{style} headshot, professional photography, studio lighting, high quality, sharp focus"
        }

        # Run the model
        if replicate_client:
            output = replicate_client.run(
                HEADSHOT_MODEL,
                input=input_params
            )
        else:
            output = replicate.run(
                HEADSHOT_MODEL,
                input=input_params
            )

        # Download generated images
        generated_images = []
        if isinstance(output, list):
            for img_url in output:
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))
                generated_images.append(img)
        else:
            # Single output
            response = requests.get(output)
            img = Image.open(BytesIO(response.content))
            generated_images.append(img)

        return generated_images, None

    except Exception as e:
        return None, str(e)

def get_image_download_link(img, filename="professional_headshot.png"):
    """Generate a download link for the headshot image"""
    buffered = BytesIO()
    img.save(buffered, format="PNG", quality=95)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">Download Headshot</a>'
    return href

# Main app
def main():
    # Initialize session state
    if 'generated_headshots' not in st.session_state:
        st.session_state.generated_headshots = None
    if 'generation_info' not in st.session_state:
        st.session_state.generation_info = {}

    st.title("=T Professional Headshot Generator")
    st.markdown("### Transform your photo into a professional headshot using AI")

    # Sidebar with information
    with st.sidebar:
        st.header("9 About")
        st.write("""
        This app uses advanced AI (Flux) to generate professional headshots from your photos.

        **Features:**
        - Professional studio-quality headshots
        - Multiple style options
        - Generate up to 4 variations
        - High-quality output
        - Download in PNG format

        **Best Results:**
        - Use a clear, front-facing photo
        - Good lighting
        - Neutral background recommended
        - Face clearly visible
        """)

        st.header("� Settings")

        # Style selection
        headshot_style = st.selectbox(
            "Headshot Style",
            [
                "professional",
                "corporate executive",
                "business casual",
                "creative professional",
                "linkedin profile",
                "formal corporate"
            ],
            help="Choose the style for your professional headshot"
        )

        # Number of variations
        num_variations = st.slider(
            "Number of Variations",
            min_value=1,
            max_value=4,
            value=2,
            help="Generate multiple variations to choose from"
        )

        # Advanced settings
        with st.expander("=' Advanced Settings"):
            guidance_scale = st.slider(
                "Guidance Scale",
                min_value=1.0,
                max_value=10.0,
                value=3.5,
                step=0.5,
                help="Higher values follow the prompt more closely"
            )

            num_steps = st.slider(
                "Inference Steps",
                min_value=1,
                max_value=4,
                value=4,
                help="Flux Schnell supports 1-4 steps (4 recommended)"
            )

        # Show API key status
        if REPLICATE_API_KEY:
            st.success(" Replicate API Key: Connected")
        else:
            st.error("� Replicate API Key: Not Found")
            st.info("Please add REPLICATE_API_KEY to your .env file")

        st.header("=� Image Info")
        if 'uploaded_image' in st.session_state:
            img = st.session_state.uploaded_image
            st.write(f"**Size:** {img.size[0]} x {img.size[1]} px")
            st.write(f"**Format:** {img.format}")

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("=� Upload Your Photo")
        uploaded_file = st.file_uploader(
            "Choose a photo (best: clear front-facing photo)",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload a photo to transform into a professional headshot"
        )

        if uploaded_file is not None:
            # Display original image
            image = Image.open(uploaded_file)
            st.session_state.uploaded_image = image

            # Clear generated headshots if a new file is uploaded
            if 'last_uploaded_file' not in st.session_state:
                st.session_state.last_uploaded_file = uploaded_file.name
            elif st.session_state.last_uploaded_file != uploaded_file.name:
                st.session_state.generated_headshots = None
                st.session_state.generation_info = {}
                st.session_state.last_uploaded_file = uploaded_file.name

            st.image(image, caption="Original Photo", use_column_width=True)
            st.info(f"Original Resolution: {image.size[0]} x {image.size[1]} pixels")

    with col2:
        st.subheader("( Professional Headshots")

        if uploaded_file is not None:
            if st.button("<� Generate Professional Headshot", type="primary"):
                if not REPLICATE_API_KEY:
                    st.error("� Replicate API key not found! Please add it to your .env file.")
                else:
                    with st.spinner(f"Generating {num_variations} professional headshot(s)... This may take 30-60 seconds."):
                        # Prepare custom prompt
                        custom_prompt = f"{headshot_style} headshot, professional photography, studio lighting, high quality, sharp focus, professional attire"

                        # Generate headshot
                        generated_images, error = generate_professional_headshot(
                            image,
                            style=headshot_style,
                            num_outputs=num_variations,
                            guidance_scale=guidance_scale,
                            num_steps=num_steps
                        )

                        if error:
                            st.error(f"L Error generating headshot: {error}")
                            st.info("=� Try these solutions:")
                            st.markdown("""
                            1. Check if your image is clear and front-facing
                            2. Reduce the number of variations
                            3. Try a different image
                            4. Wait a moment and try again
                            """)
                            st.session_state.generated_headshots = None
                        else:
                            # Save to session state
                            st.session_state.generated_headshots = generated_images
                            st.session_state.generation_info = {
                                'style': headshot_style,
                                'num_variations': len(generated_images)
                            }
                            st.success(f" Generated {len(generated_images)} professional headshot(s)!")

            # Display generated headshots (persists across reruns)
            if st.session_state.generated_headshots is not None:
                st.markdown(f"**Style:** {st.session_state.generation_info['style']}")

                # Display all generated variations
                for idx, headshot in enumerate(st.session_state.generated_headshots, 1):
                    st.image(
                        headshot,
                        caption=f"Professional Headshot - Variation {idx}",
                        use_column_width=True
                    )

                    # Download button for each variation
                    buffered = BytesIO()
                    headshot.save(buffered, format="PNG", quality=95)
                    buffered.seek(0)

                    col_download, col_info = st.columns([2, 1])

                    with col_download:
                        st.download_button(
                            label=f"=� Download Variation {idx}",
                            data=buffered.getvalue(),
                            file_name=f"professional_headshot_v{idx}.png",
                            mime="image/png",
                            key=f"download_button_{idx}",
                            use_container_width=True
                        )

                    with col_info:
                        st.caption(f"{headshot.size[0]}x{headshot.size[1]}px")

                    if idx < len(st.session_state.generated_headshots):
                        st.markdown("---")

                # Clear button
                if st.button("= Generate New Headshots", use_container_width=True):
                    st.session_state.generated_headshots = None
                    st.session_state.generation_info = {}
                    st.rerun()
        else:
            st.info("=H Please upload a photo to get started")

    # Tips section
    st.markdown("---")
    st.markdown("### =� Tips for Best Results")

    tip_col1, tip_col2, tip_col3 = st.columns(3)

    with tip_col1:
        st.markdown("""
        **=� Photo Quality**
        - Use clear, high-resolution photos
        - Face should be well-lit
        - Avoid heavy shadows
        """)

    with tip_col2:
        st.markdown("""
        **=d Positioning**
        - Face the camera directly
        - Keep face in center
        - Shoulders visible
        """)

    with tip_col3:
        st.markdown("""
        **<� Background**
        - Neutral backgrounds work best
        - Avoid busy patterns
        - Good contrast with subject
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Professional Headshot Generator | Powered by Flux & Replicate AI</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
