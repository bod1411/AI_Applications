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
    page_title="AI Headshot Generator",
    page_icon="🎨",
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
        background-color: #FF6B6B;
        color: white;
        padding: 0.5rem;
        font-size: 16px;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF5252;
        transform: translateY(-2px);
    }
    .prompt-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Model ID
MODEL_ID = "bod1411/quest-headshot:8339b931bee0c270e9cd7807d93effba91aba5a4dc9b69a2307000a5b0f1ad73"

def generate_image(prompt, negative_prompt="", num_outputs=1, guidance_scale=7.5, num_inference_steps=50):
    """
    Generate image using Replicate's quest-headshot model
    """
    try:
        # Prepare input parameters
        input_params = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_outputs": num_outputs,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps
        }
        
        # Generate the image
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

        # Output is a list of URLs for the generated images
        generated_images = []
        if isinstance(output, list):
            for image_url in output:
                response = requests.get(image_url)
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

# Main app
def main():
    # Initialize session state
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    if 'last_prompt' not in st.session_state:
        st.session_state.last_prompt = ""
    
    st.title("🎨 AI Headshot Generator")
    st.markdown("### Create professional headshots using AI")

    # Sidebar with settings
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This app uses AI to generate professional headshot images from text descriptions.

        **Features:**
        - Text-to-Image Generation
        - Professional Headshots
        - Customizable Parameters
        - Multiple Image Generation
        - High-Quality Output
        
        **Model:** Quest Headshot
        """)
        
        st.header("⚙️ Generation Settings")
        
        # Number of images to generate
        num_outputs = st.slider(
            "Number of Images",
            min_value=1,
            max_value=4,
            value=1,
            help="Generate multiple variations at once"
        )
        
        # Guidance scale
        guidance_scale = st.slider(
            "Guidance Scale",
            min_value=1.0,
            max_value=20.0,
            value=7.5,
            step=0.5,
            help="How closely to follow the prompt (higher = more strict)"
        )
        
        # Inference steps
        num_inference_steps = st.slider(
            "Inference Steps",
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

        st.header("💡 Prompt Tips")
        st.markdown("""
        **Good prompts include:**
        - Subject details (age, gender, etc.)
        - Style (professional, casual, artistic)
        - Lighting (studio, natural, dramatic)
        - Background (solid color, office, outdoor)
        - Camera angle (frontal, 3/4 view)
        
        **Example:**
        "Professional headshot of a 30-year-old woman, business attire, studio lighting, neutral background, confident expression"
        """)

    # Main content
    st.subheader("✍️ Describe Your Headshot")
    
    # Prompt input
    prompt = st.text_area(
        "Enter your prompt",
        height=100,
        placeholder="Example: Professional headshot of a businessman in a suit, studio lighting, grey background, confident smile",
        help="Describe the headshot you want to generate"
    )
    
    # Negative prompt (optional)
    with st.expander("🚫 Advanced: Negative Prompt (Optional)"):
        negative_prompt = st.text_area(
            "What to avoid in the image",
            height=80,
            placeholder="Example: blurry, distorted, low quality, cartoon, illustration",
            help="Describe what you DON'T want in the image"
        )
    
    # Example prompts
    st.markdown("### 📝 Example Prompts")
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    
    with col_ex1:
        if st.button("👔 Business Professional", use_container_width=True):
            prompt = "Professional corporate headshot of a confident business executive, formal business attire, studio lighting, neutral grey background, sharp focus, high quality"
            st.rerun()
    
    with col_ex2:
        if st.button("💼 Creative Professional", use_container_width=True):
            prompt = "Creative professional headshot, casual smart attire, natural lighting, blurred office background, friendly expression, modern style"
            st.rerun()
    
    with col_ex3:
        if st.button("🎓 Academic", use_container_width=True):
            prompt = "Academic professional headshot, smart casual clothing, library background, natural lighting, intelligent expression, scholarly appearance"
            st.rerun()

    # Generate button
    st.markdown("---")
    
    if st.button("🎨 Generate Headshot", type="primary", disabled=(not prompt.strip())):
        if not REPLICATE_API_KEY:
            st.error("❌ Replicate API key not found! Please add it to your .env file.")
        else:
            with st.spinner("🎨 Generating your headshot... This may take 30-60 seconds."):
                generated_images, error = generate_image(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_outputs=num_outputs,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps
                )
                
                if error:
                    st.error(f"❌ Error generating image: {error}")
                    st.info("💡 Tips if generation failed:")
                    st.markdown("""
                    - Check your API key is valid
                    - Ensure you have Replicate credits
                    - Try a simpler prompt
                    - Reduce the number of inference steps
                    """)
                else:
                    st.session_state.generated_images = generated_images
                    st.session_state.last_prompt = prompt
                    st.success(f"✅ Successfully generated {len(generated_images)} image(s)!")

    # Display generated images
    if st.session_state.generated_images:
        st.markdown("---")
        st.subheader("✨ Generated Headshots")
        
        # Show the prompt that was used
        with st.expander("📝 View Prompt Used"):
            st.write(st.session_state.last_prompt)
        
        # Display images in a grid
        if len(st.session_state.generated_images) == 1:
            st.image(st.session_state.generated_images[0], caption="Generated Headshot", use_column_width=True)
        else:
            cols = st.columns(min(len(st.session_state.generated_images), 2))
            for idx, img in enumerate(st.session_state.generated_images):
                with cols[idx % 2]:
                    st.image(img, caption=f"Variation {idx + 1}", use_column_width=True)
        
        # Download buttons
        st.markdown("### 📥 Download Images")
        download_cols = st.columns(len(st.session_state.generated_images))
        
        for idx, img in enumerate(st.session_state.generated_images):
            with download_cols[idx]:
                buffered = BytesIO()
                img.save(buffered, format="PNG", quality=95)
                buffered.seek(0)
                
                st.download_button(
                    label=f"💾 Image {idx + 1}",
                    data=buffered.getvalue(),
                    file_name=f"ai_headshot_{idx + 1}.png",
                    mime="image/png",
                    key=f"download_{idx}",
                    use_container_width=True
                )
        
        # Clear button
        st.markdown("---")
        if st.button("🔄 Generate New Headshot", use_container_width=True):
            st.session_state.generated_images = []
            st.session_state.last_prompt = ""
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Made with ❤️ using Streamlit and Replicate AI</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()