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
    page_title="4K Image Enhancer",
    page_icon="🖼️",
    layout="wide"
)

# Initialize API client
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

# Set the API token for Replicate (Replicate looks for REPLICATE_API_TOKEN)
if REPLICATE_API_KEY:
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY
    # Also set the client explicitly
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
        background-color: #4CAF50;
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

# Define available models
MODELS = {
    "Google Upscaler": "google/upscaler",
    "Real-ESRGAN": "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
    "Magic Image Refiner": "batouresearch/magic-image-refiner:cf47fb682f4992add797aa368591697e26be3259d86fd0501099f8a66b164b83",
    "Crystal Upscaler": "philz1337x/crystal-upscaler:95de3af5edafb719da778b9d2f001a4e5953aeef91e71b27fb33700c2759f06e"
}

def enhance_image_replicate(image_file, scale_factor=4, selected_model="Google Upscaler"):
    """
    Enhance image using selected Replicate model
    Supports multiple models for image upscaling and enhancement
    """
    try:
        # Get the model ID based on the selected model name
        model_id = MODELS[selected_model]
        
        # For Google Upscaler, handle larger images (supports up to 10MB)
        if selected_model == "Google Upscaler":
            MAX_PIXELS = 3_000_000  # More generous limit for Google's upscaler
        else:
            # GPU memory limit for other models - reduced to be more conservative
            if scale_factor == 4:
                MAX_PIXELS = 900_000  # ~950x950 for 4x scale
            elif scale_factor == 3:
                MAX_PIXELS = 1_200_000  # ~1095x1095 for 3x scale
            else:  # scale_factor == 2
                MAX_PIXELS = 1_600_000  # ~1265x1265 for 2x scale
        
        # Calculate current image pixels
        width, height = image_file.size
        current_pixels = width * height
        
        # Resize if image is too large
        processed_image = image_file
        if current_pixels > MAX_PIXELS:
            # Calculate scaling factor to fit within GPU limits
            scale_factor_resize = (MAX_PIXELS / current_pixels) ** 0.5
            new_width = int(width * scale_factor_resize)
            new_height = int(height * scale_factor_resize)
            
            st.warning(f"⚠️ Your image is large. Resizing from {width}x{height} to {new_width}x{new_height} to avoid GPU memory issues...")
            if selected_model != "Google Upscaler":
                st.info(f"💡 Tip: Try Google Upscaler for larger images, or use 2x scale for better success rate!")
            processed_image = image_file.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert PIL image to BytesIO object
        img_byte_arr = BytesIO()
        processed_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)  # Reset pointer to beginning
        
        # Prepare input parameters based on the selected model
        if selected_model == "Google Upscaler":
            # Google Upscaler only supports 2x or 4x upscaling
            # If user selected 3x, default to 4x
            upscale_factor = 4 if scale_factor >= 3 else 2
            if scale_factor == 3:
                st.info("ℹ️ Google Upscaler supports 2x or 4x. Using 4x for your 3x request.")
            
            input_params = {
                "image": img_byte_arr,
                "upscale_factor": upscale_factor
            }
        else:
            # Other models use "scale" parameter
            input_params = {
                "image": img_byte_arr,
                "scale": scale_factor
            }
            
            # Add face_enhance parameter only for Real-ESRGAN model
            if selected_model == "Real-ESRGAN":
                input_params["face_enhance"] = True
        
        # Use the initialized client if available, otherwise use default
        if replicate_client:
            output = replicate_client.run(
                model_id,
                input=input_params
            )
        else:
            output = replicate.run(
                model_id,
                input=input_params
            )

        # Download the enhanced image
        # Google upscaler returns a URL directly, other models might return a list
        if isinstance(output, str):
            response = requests.get(output)
        else:
            response = requests.get(output)
            
        enhanced_image = Image.open(BytesIO(response.content))

        return enhanced_image, None
    except Exception as e:
        return None, str(e)

def enhance_image_local(image_file, scale_factor=4):
    """
    Local enhancement using Lanczos resampling (fallback method)
    """
    try:
        width, height = image_file.size
        new_size = (width * scale_factor, height * scale_factor)
        enhanced_image = image_file.resize(new_size, Image.Resampling.LANCZOS)
        return enhanced_image, None
    except Exception as e:
        return None, str(e)

def get_image_download_link(img, filename="enhanced_image.png"):
    """Generate a download link for the enhanced image"""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">Download Enhanced Image</a>'
    return href

# Main app
def main():
    # Initialize session state for enhanced image
    if 'enhanced_image' not in st.session_state:
        st.session_state.enhanced_image = None
    if 'enhancement_info' not in st.session_state:
        st.session_state.enhancement_info = {}
    
    st.title("🖼️ 4K Image Enhancer")
    st.markdown("### Upload your image and enhance it to 4K quality using AI")

    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This app uses advanced AI models to enhance your images to 4K quality.

        **Features:**
        - 2x, 3x, or 4x Image Upscaling
        - AI-powered Enhancement
        - Multiple AI Models
        - High-quality Output
        - Auto-resize for GPU compatibility

        **Supported Models:**
        - **Google Upscaler** (Best for large images)
        - Real-ESRGAN (Replicate AI)
        - Magic Image Refiner
        - Crystal Upscaler
        - Local Enhancement (Fallback)
        
        **💡 Tips for Success:**
        - **Large images (>5MP):** Use Google Upscaler or 2x scale
        - **Medium images (2-5MP):** Try any model with 2x or 3x
        - **Small images (<2MP):** All models and scales work
        - **If GPU error:** Switch to Google Upscaler or Local Enhancement
        """)
        
        st.header("🎯 Recommended Settings")
        st.markdown("""
        | Image Size | Scale | Best Model |
        |------------|-------|-------------|
        | < 2MP | 2x-4x | Any Model |
        | 2-5MP | 2x-3x | Google / Real-ESRGAN |
        | > 5MP | 2x | Google Upscaler |
        | Any | 2x-4x | Local (Fast) |
        """)

        st.header("⚙️ Settings")
        enhancement_method = st.selectbox(
            "Enhancement Method",
            ["AI Enhancement (Best Quality)", "Local Enhancement (Fast)"]
        )
        
        # Show model selection only for AI Enhancement
        selected_model = None
        if enhancement_method == "AI Enhancement (Best Quality)":
            selected_model = st.selectbox(
                "AI Model",
                list(MODELS.keys()),
                help="Choose the AI model for image enhancement. Google Upscaler is recommended for large images."
            )
            
            # Show model-specific info
            if selected_model == "Google Upscaler":
                st.success("✅ Google Upscaler: Best for large images, supports up to 10MB")
        
        # Scale factor selector with helpful tips
        st.markdown("**Upscaling Factor:**")
        scale_factor = st.selectbox(
            "Choose scale",
            [2, 3, 4],
            index=0,  # Default to 2x for better stability
            help="Higher values create larger images but use more GPU memory",
            label_visibility="collapsed"
        )
        
        # Memory usage guide
        if scale_factor == 4:
            st.warning("⚠️ 4x uses most GPU memory - may fail on large images")
        elif scale_factor == 3:
            st.info("ℹ️ 3x - good balance of quality and stability")
        else:
            st.success("✅ 2x - most reliable, lowest memory usage")
        
        # Show API key status
        if REPLICATE_API_KEY:
            st.success("✅ Replicate API Key: Connected")
        else:
            st.warning("⚠️ Replicate API Key: Not Found")

        st.header("📊 Image Info")
        if 'uploaded_image' in st.session_state:
            img = st.session_state.uploaded_image
            st.write(f"**Original Size:** {img.size[0]} x {img.size[1]} px")
            st.write(f"**Format:** {img.format}")
            st.write(f"**Mode:** {img.mode}")

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload an image to enhance to 4K quality"
        )

        if uploaded_file is not None:
            # Display original image
            image = Image.open(uploaded_file)
            st.session_state.uploaded_image = image
            
            # Clear enhanced image if a new file is uploaded
            if 'last_uploaded_file' not in st.session_state:
                st.session_state.last_uploaded_file = uploaded_file.name
            elif st.session_state.last_uploaded_file != uploaded_file.name:
                st.session_state.enhanced_image = None
                st.session_state.enhancement_info = {}
                st.session_state.last_uploaded_file = uploaded_file.name
            
            st.image(image, caption="Original Image", use_column_width=True)

            # Show image details
            st.info(f"Original Resolution: {image.size[0]} x {image.size[1]} pixels")
            
            # Warn if image is very large
            total_pixels = image.size[0] * image.size[1]
            if total_pixels > 5_000_000:  # > 5MP
                st.warning("⚠️ Large image detected! For best results:")
                st.markdown("- Use **Google Upscaler** (handles large images)")
                st.markdown("- Or start with **2x scale**")
                st.markdown("- Or use **Local Enhancement**")
            elif total_pixels > 2_000_000:  # > 2MP
                st.info("💡 Medium-sized image. Recommended: **2x or 3x scale**")

    with col2:
        st.subheader("✨ Enhanced Image")

        if uploaded_file is not None:
            if st.button(f"🚀 Enhance Image ({scale_factor}x)", type="primary"):
                with st.spinner("Enhancing your image... This may take a minute."):

                    if enhancement_method == "AI Enhancement (Best Quality)":
                        # Check if API key is available
                        if not REPLICATE_API_KEY:
                            st.error("⚠️ Replicate API key not found! Please add it to your .env file.")
                            st.info("Falling back to local enhancement method...")
                            enhanced_image, error = enhance_image_local(image, scale_factor)
                        else:
                            enhanced_image, error = enhance_image_replicate(image, scale_factor, selected_model)
                    else:
                        enhanced_image, error = enhance_image_local(image, scale_factor)

                    if error:
                        st.error(f"❌ Error enhancing image: {error}")
                        
                        # Check if it's a GPU memory error
                        if "CUDA out of memory" in str(error) or "memory" in str(error).lower():
                            st.error("🚨 GPU Memory Error Detected!")
                            st.info("**Try these solutions:**")
                            st.markdown("""
                            1. **Try Google Upscaler** (handles larger images)
                            2. **Use 2x scale instead of 4x** (requires less GPU memory)
                            3. **Try Local Enhancement method** (no GPU needed)
                            4. **Resize your image smaller** before uploading
                            5. **Wait a minute and try again** (GPU might be busy with other users)
                            """)
                        else:
                            st.info("💡 Try using Google Upscaler or Local Enhancement method instead.")
                        
                        st.session_state.enhanced_image = None
                    else:
                        # Save to session state
                        st.session_state.enhanced_image = enhanced_image
                        st.session_state.enhancement_info = {
                            'scale_factor': scale_factor,
                            'resolution': f"{enhanced_image.size[0]} x {enhanced_image.size[1]}",
                            'model': selected_model if enhancement_method == "AI Enhancement (Best Quality)" else "Local"
                        }
                        st.success(f"✅ Image enhanced successfully ({scale_factor}x upscale)!")
            
            # Display enhanced image and download button (persists across reruns)
            if st.session_state.enhanced_image is not None:
                st.image(
                    st.session_state.enhanced_image, 
                    caption=f"Enhanced Image ({st.session_state.enhancement_info['scale_factor']}x)", 
                    use_column_width=True
                )
                
                # Show enhanced image details
                st.info(f"✨ Enhanced Resolution: {st.session_state.enhancement_info['resolution']} pixels")
                st.info(f"🤖 Model Used: {st.session_state.enhancement_info['model']}")

                # Download button - always visible when enhanced image exists
                buffered = BytesIO()
                st.session_state.enhanced_image.save(buffered, format="PNG", quality=95)
                buffered.seek(0)
                
                col_download, col_clear = st.columns([3, 1])
                
                with col_download:
                    st.download_button(
                        label="📥 Download Enhanced Image",
                        data=buffered.getvalue(),
                        file_name=f"enhanced_{st.session_state.enhancement_info['scale_factor']}x_image.png",
                        mime="image/png",
                        key="download_button",
                        use_container_width=True
                    )
                
                with col_clear:
                    if st.button("🔄 New", help="Clear to enhance again", use_container_width=True):
                        st.session_state.enhanced_image = None
                        st.session_state.enhancement_info = {}
                        st.rerun()
        else:
            st.info("👈 Please upload an image to get started")

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Made with ❤️ using Streamlit and AI</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()