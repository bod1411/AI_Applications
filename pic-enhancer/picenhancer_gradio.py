import gradio as gr
import os
from PIL import Image
import replicate
from dotenv import load_dotenv
import requests
from io import BytesIO

# Load environment variables
load_dotenv()

# Initialize API client
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

# Set the API token for Replicate
if REPLICATE_API_KEY:
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY
    replicate_client = replicate.Client(api_token=REPLICATE_API_KEY)
else:
    replicate_client = None

# Define available models
MODELS = {
    "Real-ESRGAN": "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
    "Magic Image Refiner": "batouresearch/magic-image-refiner:cf47fb682f4992add797aa368591697e26be3259d86fd0501099f8a66b164b83",
    "Crystal Upscaler": "philz1337x/crystal-upscaler:95de3af5edafb719da778b9d2f001a4e5953aeef91e71b27fb33700c2759f06e"
}


def get_image_info(image):
    """Get image information string"""
    if image is None:
        return "No image uploaded"
    width, height = image.size
    total_pixels = width * height
    mp = total_pixels / 1_000_000

    info = f"Resolution: {width} x {height} pixels ({mp:.2f} MP)"

    if total_pixels > 5_000_000:
        info += "\n⚠️ Large image! Recommended: 2x scale or Local Enhancement"
    elif total_pixels > 2_000_000:
        info += "\n💡 Medium image. Recommended: 2x or 3x scale"

    return info


def enhance_image_replicate(image, scale_factor=4, selected_model="Real-ESRGAN"):
    """
    Enhance image using selected Replicate model
    """
    try:
        # GPU memory limit based on scale factor
        if scale_factor == 4:
            MAX_PIXELS = 900_000
        elif scale_factor == 3:
            MAX_PIXELS = 1_200_000
        else:
            MAX_PIXELS = 1_600_000

        width, height = image.size
        current_pixels = width * height

        processed_image = image
        resize_warning = ""

        if current_pixels > MAX_PIXELS:
            scale_factor_resize = (MAX_PIXELS / current_pixels) ** 0.5
            new_width = int(width * scale_factor_resize)
            new_height = int(height * scale_factor_resize)
            resize_warning = f"⚠️ Image resized from {width}x{height} to {new_width}x{new_height} to avoid GPU memory issues."
            processed_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert PIL image to BytesIO
        img_byte_arr = BytesIO()
        processed_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        model_id = MODELS[selected_model]

        input_params = {
            "image": img_byte_arr,
            "scale": scale_factor
        }

        if selected_model == "Real-ESRGAN":
            input_params["face_enhance"] = True

        if replicate_client:
            output = replicate_client.run(model_id, input=input_params)
        else:
            output = replicate.run(model_id, input=input_params)

        response = requests.get(output)
        enhanced_image = Image.open(BytesIO(response.content))

        return enhanced_image, resize_warning
    except Exception as e:
        return None, str(e)


def enhance_image_local(image, scale_factor=4):
    """
    Local enhancement using Lanczos resampling (fallback method)
    """
    try:
        width, height = image.size
        new_size = (width * scale_factor, height * scale_factor)
        enhanced_image = image.resize(new_size, Image.Resampling.LANCZOS)
        return enhanced_image, None
    except Exception as e:
        return None, str(e)


def enhance_image(image, enhancement_method, selected_model, scale_factor):
    """Main enhancement function"""
    if image is None:
        return None, "Please upload an image first."

    scale_factor = int(scale_factor)

    if enhancement_method == "AI Enhancement (Best Quality)":
        if not REPLICATE_API_KEY:
            return None, "⚠️ Replicate API key not found! Please add it to your .env file. Falling back to local enhancement..."

        enhanced_image, error = enhance_image_replicate(image, scale_factor, selected_model)
    else:
        enhanced_image, error = enhance_image_local(image, scale_factor)

    if error and enhanced_image is None:
        error_msg = f"❌ Error: {error}"
        if "CUDA out of memory" in str(error) or "memory" in str(error).lower():
            error_msg += "\n\n🚨 GPU Memory Error! Try:\n1. Use 2x scale instead\n2. Try Local Enhancement\n3. Resize image before uploading\n4. Wait and try again"
        return None, error_msg

    # Build success message
    if enhanced_image:
        success_msg = f"✅ Enhanced successfully! New resolution: {enhanced_image.size[0]} x {enhanced_image.size[1]} pixels"
        if error:  # This contains resize warning
            success_msg = f"{error}\n\n{success_msg}"
        return enhanced_image, success_msg

    return None, "Unknown error occurred"


def update_model_visibility(enhancement_method):
    """Show/hide model selection based on enhancement method"""
    return gr.update(visible=(enhancement_method == "AI Enhancement (Best Quality)"))


def update_scale_info(scale_factor):
    """Update scale factor information"""
    scale_factor = int(scale_factor)
    if scale_factor == 4:
        return "⚠️ 4x uses most GPU memory - may fail on large images"
    elif scale_factor == 3:
        return "ℹ️ 3x - good balance of quality and stability"
    else:
        return "✅ 2x - most reliable, lowest memory usage"


# Build Gradio interface
with gr.Blocks(
    title="4K Image Enhancer",
    theme=gr.themes.Soft(),
    css="""
        .main-title { text-align: center; margin-bottom: 20px; }
        .info-box { padding: 10px; border-radius: 8px; background: #f0f0f0; }
    """
) as app:

    gr.Markdown("# 🖼️ 4K Image Enhancer", elem_classes="main-title")
    gr.Markdown("### Upload your image and enhance it to 4K quality using AI")

    with gr.Row():
        # Left sidebar - Settings
        with gr.Column(scale=1):
            gr.Markdown("## ⚙️ Settings")

            enhancement_method = gr.Dropdown(
                choices=["AI Enhancement (Best Quality)", "Local Enhancement (Fast)"],
                value="AI Enhancement (Best Quality)",
                label="Enhancement Method"
            )

            selected_model = gr.Dropdown(
                choices=list(MODELS.keys()),
                value="Real-ESRGAN",
                label="AI Model",
                visible=True
            )

            scale_factor = gr.Radio(
                choices=["2", "3", "4"],
                value="2",
                label="Upscaling Factor"
            )

            scale_info = gr.Markdown("✅ 2x - most reliable, lowest memory usage")

            # API Status
            if REPLICATE_API_KEY:
                gr.Markdown("✅ **Replicate API:** Connected")
            else:
                gr.Markdown("⚠️ **Replicate API:** Not Found")

            gr.Markdown("---")
            gr.Markdown("## ℹ️ About")
            gr.Markdown("""
            **Features:**
            - 2x, 3x, or 4x Image Upscaling
            - AI-powered Enhancement
            - Face Enhancement
            - High-quality Output
            - Auto-resize for GPU compatibility

            **Supported Models:**
            - Real-ESRGAN
            - Magic Image Refiner
            - Crystal Upscaler
            - Local Enhancement (Fallback)
            """)

            gr.Markdown("---")
            gr.Markdown("## 🎯 Recommended Settings")
            gr.Markdown("""
            | Image Size | Scale | Method |
            |------------|-------|---------|
            | < 2MP | 2x-4x | Real-ESRGAN |
            | 2-5MP | 2x-3x | Real-ESRGAN |
            | > 5MP | 2x | Real-ESRGAN |
            | Any | 2x-4x | Local (Fast) |
            """)

        # Main content area
        with gr.Column(scale=3):
            with gr.Row():
                # Original Image Column
                with gr.Column():
                    gr.Markdown("## 📤 Upload Image")
                    input_image = gr.Image(
                        type="pil",
                        label="Original Image",
                        height=400
                    )
                    image_info = gr.Markdown("No image uploaded")

                # Enhanced Image Column
                with gr.Column():
                    gr.Markdown("## ✨ Enhanced Image")
                    output_image = gr.Image(
                        type="pil",
                        label="Enhanced Image",
                        height=400
                    )
                    status_message = gr.Markdown("")

            # Enhance button
            enhance_btn = gr.Button(
                "🚀 Enhance Image",
                variant="primary",
                size="lg"
            )

    gr.Markdown("---")
    gr.Markdown("<p style='text-align: center; color: gray;'>Made with ❤️ using Gradio and AI</p>")

    # Event handlers
    enhancement_method.change(
        fn=update_model_visibility,
        inputs=[enhancement_method],
        outputs=[selected_model]
    )

    scale_factor.change(
        fn=update_scale_info,
        inputs=[scale_factor],
        outputs=[scale_info]
    )

    input_image.change(
        fn=get_image_info,
        inputs=[input_image],
        outputs=[image_info]
    )

    enhance_btn.click(
        fn=enhance_image,
        inputs=[input_image, enhancement_method, selected_model, scale_factor],
        outputs=[output_image, status_message]
    )


if __name__ == "__main__":
    app.launch()
