import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import io
import requests
from huggingface_hub import InferenceClient
import base64
import traceback

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Configure page
st.set_page_config(
    page_title="AI Headshot Generator",
    page_icon="📸",
    layout="wide"
)

# Available models for headshot generation
MODELS = {
    "Stable Diffusion XL": {
        "id": "stabilityai/stable-diffusion-xl-base-1.0",
        "description": "High-quality image generation with excellent detail",
        "type": "text-to-image"
    },
    "Stable Diffusion 2.1": {
        "id": "stabilityai/stable-diffusion-2-1",
        "description": "Reliable and versatile image generation",
        "type": "text-to-image"
    },
    "Stable Diffusion 1.5": {
        "id": "runwayml/stable-diffusion-v1-5",
        "description": "Fast and reliable image generation",
        "type": "text-to-image"
    },
    "Realistic Vision V5.1": {
        "id": "SG161222/Realistic_Vision_V5.1_noVAE",
        "description": "High-quality realistic portraits with excellent detail",
        "type": "text-to-image"
    }
}

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def generate_headshot_prompt(style="professional", gender="neutral"):
    """Generate optimized prompt for headshot generation"""
    base_prompts = {
        "professional": "professional corporate headshot, business attire, studio lighting, plain background, high quality, sharp focus, 8k uhd, dslr, professional photography",
        "casual": "casual professional portrait, natural lighting, soft smile, approachable, high quality, sharp focus, 8k uhd, dslr",
        "creative": "creative professional portrait, artistic lighting, confident expression, modern style, high quality, sharp focus, 8k uhd, dslr",
        "linkedin": "linkedin profile photo, professional business portrait, suit, studio lighting, neutral background, high quality, sharp focus, 8k uhd"
    }

    negative_prompt = "blurry, low quality, distorted, disfigured, ugly, bad anatomy, bad proportions, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, bad art, amateur"

    return base_prompts.get(style, base_prompts["professional"]), negative_prompt

def generate_with_api(model_id, prompt, negative_prompt, uploaded_image=None):
    """Generate headshot using Hugging Face Inference API"""
    try:
        # Initialize client with specific model
        client = InferenceClient(model=model_id, token=HF_TOKEN)

        st.info(f"Using model: {model_id}")
        st.info("Generating image... This may take 30-60 seconds.")

        # Generate image based on prompt
        # Note: negative_prompt support varies by model
        try:
            result = client.text_to_image(
                prompt=prompt,
                negative_prompt=negative_prompt,
            )
        except TypeError:
            # If negative_prompt is not supported, try without it
            st.warning("Note: This model doesn't support negative prompts")
            result = client.text_to_image(
                prompt=prompt,
            )

        return result
    except StopIteration as e:
        st.error("⚠️ Model Provider Error")
        st.warning(f"The model '{model_id}' is not available via the Inference API or requires a paid tier.")
        st.info("**Suggestions:**")
        st.markdown("""
        - Try a different model from the dropdown (Stable Diffusion 1.5 or 2.1 are most reliable)
        - Check if the model requires a Pro subscription at https://huggingface.co/pricing
        - Verify your HF token has the necessary permissions
        """)
        return None
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        st.error(f"Error type: {type(e).__name__}")

        # Show full traceback for debugging
        with st.expander("View Full Error Details"):
            traceback_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            st.code(traceback_str, language="python")

            # Show exception arguments if available
            if hasattr(e, 'args') and e.args:
                st.error(f"Exception args: {e.args}")

        # Provide helpful debugging information
        if "model" in str(e).lower() or "not found" in str(e).lower():
            st.warning("⚠️ This model might not be available via the Inference API. Try selecting a different model.")
        elif "token" in str(e).lower() or "unauthorized" in str(e).lower():
            st.warning("⚠️ Token issue detected. Please check your HF_TOKEN in the .env file.")
        elif "rate" in str(e).lower() or "quota" in str(e).lower():
            st.warning("⚠️ Rate limit or quota exceeded. Please wait a few minutes and try again.")

        return None

def main():
    st.title("📸 AI Professional Headshot Generator")
    st.markdown("Transform your photos into professional headshots using state-of-the-art AI models")

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Settings")

        # Model selection
        selected_model_name = st.selectbox(
            "Select AI Model",
            options=list(MODELS.keys()),
            help="Choose the model that best suits your needs"
        )

        selected_model = MODELS[selected_model_name]
        st.info(f"📝 {selected_model['description']}")

        # Style selection
        style = st.selectbox(
            "Headshot Style",
            options=["professional", "casual", "creative", "linkedin"],
            help="Choose the style of your headshot"
        )

        # Additional options
        st.subheader("Advanced Options")
        gender = st.selectbox("Gender Reference", ["neutral", "male", "female"])
        add_description = st.text_area(
            "Additional Description (optional)",
            placeholder="e.g., wearing glasses, short hair, smiling...",
            help="Add specific details you want in the headshot"
        )

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📤 Upload Reference Photo")
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear photo of yourself"
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Display image info
            st.caption(f"Image size: {image.size[0]}x{image.size[1]} pixels")

    with col2:
        st.subheader("✨ Generated Headshot")

        if uploaded_file is not None:
            if st.button("🎨 Generate Headshot", type="primary", use_container_width=True):
                with st.spinner("🎨 Creating your professional headshot..."):
                    # Generate prompt
                    base_prompt, negative_prompt = generate_headshot_prompt(style, gender)

                    # Add user description if provided
                    if add_description:
                        base_prompt = f"{base_prompt}, {add_description}"

                    # Display the prompt being used
                    with st.expander("View Generation Prompt"):
                        st.write("**Positive Prompt:**")
                        st.code(base_prompt)
                        st.write("**Negative Prompt:**")
                        st.code(negative_prompt)

                    # Generate image
                    generated_image = generate_with_api(
                        selected_model["id"],
                        base_prompt,
                        negative_prompt,
                        image
                    )

                    if generated_image:
                        st.success("✅ Headshot generated successfully!")
                        st.image(generated_image, caption="Generated Headshot", use_column_width=True)

                        # Download button
                        buf = io.BytesIO()
                        generated_image.save(buf, format="PNG")
                        btn = st.download_button(
                            label="⬇️ Download Headshot",
                            data=buf.getvalue(),
                            file_name="professional_headshot.png",
                            mime="image/png",
                            use_container_width=True
                        )
        else:
            st.info("👆 Please upload a photo to get started")

    # Information section
    st.markdown("---")
    st.subheader("ℹ️ How to Use")

    info_cols = st.columns(4)
    with info_cols[0]:
        st.markdown("**1️⃣ Select Model**")
        st.caption("Choose an AI model from the sidebar")

    with info_cols[1]:
        st.markdown("**2️⃣ Upload Photo**")
        st.caption("Upload a clear photo of yourself")

    with info_cols[2]:
        st.markdown("**3️⃣ Choose Style**")
        st.caption("Select your preferred headshot style")

    with info_cols[3]:
        st.markdown("**4️⃣ Generate**")
        st.caption("Click generate and download your headshot")

    # Tips section
    with st.expander("💡 Tips for Best Results"):
        st.markdown("""
        - **Upload a clear, well-lit photo** with your face clearly visible
        - **Choose the right style** based on your intended use (LinkedIn, resume, etc.)
        - **Use additional descriptions** to specify details like clothing, accessories, or expressions
        - **Try different models** to see which one works best for your photo
        - **Ensure good lighting** in your original photo for better results
        - **Face the camera directly** for more professional results
        """)

    # Footer
    st.markdown("---")
    st.caption("Powered by Hugging Face 🤗 | Built with Streamlit")

if __name__ == "__main__":
    # Check if HF_TOKEN is available
    if not HF_TOKEN:
        st.error("⚠️ HF_TOKEN not found in .env file. Please add your Hugging Face token.")
        st.stop()

    main()
