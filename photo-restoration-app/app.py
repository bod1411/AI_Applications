import streamlit as st
import os
from PIL import Image, ImageStat
import replicate
from dotenv import load_dotenv
import requests
from io import BytesIO
import base64
import time
import numpy as np

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Smart Photo Restoration - AI Auto-Detect",
    page_icon="🖼️",
    layout="wide"
)

# Initialize API client
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 100))

# MEMORY MANAGEMENT SETTINGS
MAX_IMAGE_DIMENSION = 2048  # Maximum width or height to prevent GPU OOM
TARGET_DIMENSION = 1500     # Target size for large images
MIN_DIMENSION = 800         # Don't resize if already small

# Set the API token for Replicate
if REPLICATE_API_KEY:
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY
    replicate_client = replicate.Client(api_token=REPLICATE_API_KEY)
else:
    replicate_client = None

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem;
        font-size: 16px;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .detection-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 2px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .hero-section {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ORGANIZED MODEL CATALOG
MODELS = {
    "DAMAGED_PHOTOS": {
        "FLUX Restore": {
            "model": "flux-kontext-apps/restore-image",
            "description": "AI-powered complete restoration for heavily damaged photos",
            "memory_intensive": True,  # Mark memory-intensive models
            "params": {"image": None, "prompt": "Restore this damaged photo, fix scratches and tears, enhance quality"}
        },
        "SwinIR": {
            "model": "jingyunliang/swinir:660d922d33153019e8c263a3bba265de882e7f4f70396546b6c9c8f9d47a021a",
            "description": "Excellent for denoising, deblurring, and artifact removal",
            "memory_intensive": False,
            "params": {"image": None, "task_type": "Real-World Image Super-Resolution-Large"}
        },
        "CodeFormer": {
            "model": "sczhou/codeformer:cc4956dd26fa5a7185d5660cc9100fab1b8070a1d1654a8bb5eb6d443b020bb2",
            "description": "Robust face restoration with damage repair",
            "memory_intensive": False,
            "params": {"image": None, "codeformer_fidelity": 0.7, "background_enhance": True, "upscale": 2}
        },
        "BSRGAN": {
            "model": "zsxkib/bsrgan:1ae02b13920bbc43cedec32a680b836412a55d978d0a2f2f6a423acc85e332e4",
            "description": "Specialized for degraded images",
            "memory_intensive": False,
            "params": {"image": None}
        },
        "Old Photos Back to Life": {
            "model": "microsoft/bringing-old-photos-back-to-life:c75db81db6cbd809d93cc3b7e7a088a351a3349c9fa02b6d393e35e0d51ba799",
            "description": "Microsoft's model for restoring very old photos",
            "memory_intensive": False,
            "params": {"image": None, "HR": False, "with_scratch": True}
        },
        "MAXIM": {
            "model": "google-research/maxim:494ca4d578293b4b93945115601b6a38190519da18467556ca223d219c3af9f9",
            "description": "Google's multi-task denoising",
            "memory_intensive": False,
            "params": {"image": None, "model": "Denoising"}
        }
    },
    "BLACK_AND_WHITE": {
        "DDColor": {
            "model": "piddnad/ddcolor:ca494ba129e44e45f661d6ece83c4c98a9a7c774309beca01429b58fce8aa695",
            "description": "Most realistic colorization",
            "memory_intensive": False,
            "params": {"image": None, "model_size": "large"}
        },
        "DeOldify": {
            "model": "arielreplicate/deoldify_image:0da600fab0c45a66211339f1c16b71345d22f26ef5fea3dca1bb90bb5711e950",
            "description": "Classic deep learning colorization",
            "memory_intensive": False,
            "params": {"image": None, "render_factor": 35}
        },
        "BigColor": {
            "model": "cjwbw/bigcolor:9451bfbf652b21a9bccc741e5c7046540faa5586cfa3aa45abc7dbb46151a4f7",
            "description": "Multiple colorization variations",
            "memory_intensive": False,
            "params": {"image": None}
        }
    },
    "FACE_RESTORATION": {
        "VQFR": {
            "model": "cjwbw/vqfr:ccd53a9a38ebbaa783a1e6318d22fa68c14c3aed66cc3589e53ef07d07f5be1d",
            "description": "High-quality face restoration",
            "memory_intensive": False,
            "params": {"image": None, "scale": 2, "fidelity_ratio": 0.5}
        },
        "GPEN": {
            "model": "yangxy/gpen:cf4e15a70049c0119884eb2906c8ae8807af8317bea98313fefd941e414d0c91",
            "description": "GAN-based face enhancement",
            "memory_intensive": False,
            "params": {"image": None}
        },
        "CodeFormer Face": {
            "model": "lucataco/codeformer:78f2bab438ab0ffc85a68cdfd316a2ecd3994b5dd26aa6b3d203357b45e5eb1b",
            "description": "Advanced face restoration",
            "memory_intensive": False,
            "params": {"image": None, "codeformer_fidelity": 0.7, "upscale": 2}
        },
        "GFPGAN": {
            "model": "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
            "description": "Industry standard for face restoration",
            "memory_intensive": False,
            "params": {"img": None, "version": "v1.4", "scale": 2}
        }
    },
    "NIGHT_IMAGES": {
        "Night Enhancement": {
            "model": "cjwbw/night-enhancement:4328e402cfedafa70ad7cec04412e86ab61832204deccd94108ae5222c9b1ae1",
            "description": "Specialized for low-light photos",
            "memory_intensive": False,
            "params": {"image": None}
        }
    }
}

def smart_resize_image(image, max_dimension=MAX_IMAGE_DIMENSION, target_dimension=TARGET_DIMENSION):
    """
    Intelligently resize image to prevent GPU memory issues
    Returns: (resized_image, was_resized, original_size, new_size)
    """
    width, height = image.size
    max_side = max(width, height)
    
    # If image is already small enough, don't resize
    if max_side <= MIN_DIMENSION:
        return image, False, (width, height), (width, height)
    
    # If image is too large, resize it
    if max_side > max_dimension:
        # Calculate new dimensions maintaining aspect ratio
        if width > height:
            new_width = target_dimension
            new_height = int(height * (target_dimension / width))
        else:
            new_height = target_dimension
            new_width = int(width * (target_dimension / height))
        
        # Use high-quality Lanczos resampling
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return resized_image, True, (width, height), (new_width, new_height)
    
    return image, False, (width, height), (width, height)

def analyze_image_conditions(image):
    """
    Comprehensive image analysis to detect multiple conditions
    """
    conditions = {
        "is_bw": False,
        "is_damaged": False,
        "has_faces": False,
        "is_night": False,
        "is_blurry": False,
        "is_noisy": False,
        "confidence": {}
    }
    
    # Convert to RGB and numpy array
    rgb_image = image.convert('RGB')
    gray_image = image.convert('L')
    img_array = np.array(rgb_image)
    
    # 1. CHECK IF BLACK AND WHITE
    pixels = list(rgb_image.getdata())[::50]
    color_variance = 0
    for r, g, b in pixels[:min(200, len(pixels))]:
        variance = max(abs(r-g), abs(g-b), abs(r-b))
        color_variance += variance
    
    avg_color_variance = color_variance / len(pixels[:min(200, len(pixels))])
    
    if avg_color_variance < 15:
        conditions["is_bw"] = True
        conditions["confidence"]["bw"] = min(100, (15 - avg_color_variance) * 7)
    
    # 2. CHECK FOR DARKNESS/NIGHT IMAGES
    stat = ImageStat.Stat(gray_image)
    brightness = stat.mean[0]
    
    if brightness < 80:
        conditions["is_night"] = True
        conditions["confidence"]["night"] = min(100, (80 - brightness) * 1.5)
    
    # 3. CHECK FOR DAMAGE/NOISE
    img_std = np.std(img_array)
    
    if img_std > 60:
        conditions["is_noisy"] = True
        conditions["confidence"]["noisy"] = min(100, (img_std - 60) * 2)
    
    flat_array = img_array.flatten()
    extreme_pixels = np.sum((flat_array < 20) | (flat_array > 235))
    extreme_ratio = extreme_pixels / len(flat_array)
    
    if extreme_ratio > 0.05:
        conditions["is_damaged"] = True
        conditions["confidence"]["damaged"] = min(100, extreme_ratio * 1000)
    
    # 4. FACE DETECTION
    width, height = image.size
    aspect_ratio = width / height
    
    if 0.6 < aspect_ratio < 1.7:
        center_x, center_y = width // 2, height // 2
        region_size = min(width, height) // 4
        
        try:
            center_region = rgb_image.crop((
                max(0, center_x - region_size),
                max(0, center_y - region_size),
                min(width, center_x + region_size),
                min(height, center_y + region_size)
            ))
            
            skin_pixels = 0
            total_pixels = 0
            for r, g, b in list(center_region.getdata())[::10]:
                total_pixels += 1
                if 95 < r < 255 and 40 < g < 200 and 20 < b < 170:
                    if r > g > b:
                        skin_pixels += 1
            
            skin_ratio = skin_pixels / max(total_pixels, 1)
            if skin_ratio > 0.15:
                conditions["has_faces"] = True
                conditions["confidence"]["faces"] = min(100, skin_ratio * 300)
        except:
            pass
    
    # 5. BLUR DETECTION
    try:
        gray_array = np.array(gray_image)
        if gray_array.shape[0] > 1 and gray_array.shape[1] > 1:
            grad_x = np.abs(np.diff(gray_array, axis=1))
            grad_y = np.abs(np.diff(gray_array, axis=0))
            edge_strength = np.mean(grad_x) + np.mean(grad_y)
            
            if edge_strength < 15:
                conditions["is_blurry"] = True
                conditions["confidence"]["blurry"] = min(100, (15 - edge_strength) * 7)
    except:
        pass
    
    return conditions

def select_best_models(conditions, image_was_resized):
    """
    Select the best model(s) based on detected conditions
    Avoids memory-intensive models if image was large
    """
    selected_models = []
    
    # Priority 1: Night images
    if conditions["is_night"] and conditions["confidence"].get("night", 0) > 40:
        selected_models.append(("NIGHT_IMAGES", "Night Enhancement", MODELS["NIGHT_IMAGES"]["Night Enhancement"]))
    
    # Priority 2: Damage restoration
    if conditions["is_damaged"] or conditions["is_noisy"]:
        confidence = max(
            conditions["confidence"].get("damaged", 0),
            conditions["confidence"].get("noisy", 0)
        )
        
        if confidence > 30:
            if conditions["has_faces"]:
                selected_models.append(("DAMAGED_PHOTOS", "CodeFormer", MODELS["DAMAGED_PHOTOS"]["CodeFormer"]))
            elif confidence > 60:
                # Use SwinIR instead of Old Photos if image was resized (memory concern)
                if image_was_resized:
                    selected_models.append(("DAMAGED_PHOTOS", "SwinIR", MODELS["DAMAGED_PHOTOS"]["SwinIR"]))
                else:
                    selected_models.append(("DAMAGED_PHOTOS", "Old Photos Back to Life", MODELS["DAMAGED_PHOTOS"]["Old Photos Back to Life"]))
            else:
                selected_models.append(("DAMAGED_PHOTOS", "SwinIR", MODELS["DAMAGED_PHOTOS"]["SwinIR"]))
    
    # Priority 3: Face restoration
    if conditions["has_faces"] and conditions["confidence"].get("faces", 0) > 30:
        if not any("CodeFormer" in str(m) for m in selected_models):
            selected_models.append(("FACE_RESTORATION", "GFPGAN", MODELS["FACE_RESTORATION"]["GFPGAN"]))
    
    # Priority 4: Colorization
    if conditions["is_bw"] and conditions["confidence"].get("bw", 0) > 50:
        selected_models.append(("BLACK_AND_WHITE", "DDColor", MODELS["BLACK_AND_WHITE"]["DDColor"]))
    
    # Default: general enhancement
    if not selected_models:
        selected_models.append(("DAMAGED_PHOTOS", "SwinIR", MODELS["DAMAGED_PHOTOS"]["SwinIR"]))
    
    # Limit to 3 models max to avoid excessive processing
    return selected_models[:3]

def run_model(image, category, model_name, model_info):
    """
    Run a specific model with error handling
    """
    try:
        model_id = model_info["model"]
        params = model_info["params"].copy()
        
        # Convert to BytesIO
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Set image parameter
        if "image" in params:
            params["image"] = img_byte_arr
        elif "img" in params:
            params["img"] = img_byte_arr
        
        # Reduce upscale factor if present to save memory
        if "upscale" in params and params["upscale"] > 2:
            params["upscale"] = 2
        if "scale" in params and params["scale"] > 2:
            params["scale"] = 2
        
        # Run the model
        if replicate_client:
            output = replicate_client.run(model_id, input=params)
        else:
            output = replicate.run(model_id, input=params)
        
        # Handle output
        if isinstance(output, str):
            response = requests.get(output)
            result_image = Image.open(BytesIO(response.content))
        elif isinstance(output, list):
            response = requests.get(output[0])
            result_image = Image.open(BytesIO(response.content))
        else:
            try:
                if hasattr(output, 'url'):
                    response = requests.get(output.url)
                    result_image = Image.open(BytesIO(response.content))
                else:
                    output_url = next(iter(output))
                    response = requests.get(output_url)
                    result_image = Image.open(BytesIO(response.content))
            except Exception as e:
                output_str = str(output)
                if output_str.startswith('http'):
                    response = requests.get(output_str)
                    result_image = Image.open(BytesIO(response.content))
                else:
                    raise e
        
        return result_image, None
    
    except Exception as e:
        error_msg = str(e)
        if "out of memory" in error_msg.lower() or "oom" in error_msg.lower():
            error_msg = "GPU out of memory. Image was too large. Try a smaller image or different model."
        elif "404" in error_msg or "not found" in error_msg.lower():
            error_msg = f"Model '{model_name}' temporarily unavailable."
        return None, error_msg

def process_image_smart(image, progress_callback=None, custom_model=None):
    """
    Process image with automatic resizing and error recovery
    custom_model: Optional tuple of (category, model_name, model_info) for manual model selection
    """
    results = []
    
    # Step 1: Smart resize to prevent memory issues
    if progress_callback:
        progress_callback(5, "📏 Checking image size...")
    
    processed_image, was_resized, original_size, new_size = smart_resize_image(image)
    
    if was_resized:
        resize_info = {
            "resized": True,
            "original": original_size,
            "new": new_size,
            "reason": "Prevented GPU memory issues"
        }
    else:
        resize_info = {"resized": False}
    
    # Step 2: Analyze
    if progress_callback:
        progress_callback(10, "🔍 Analyzing image conditions...")
    
    conditions = analyze_image_conditions(processed_image)
    
    # Step 3: Select models
    if progress_callback:
        progress_callback(20, "🎯 Selecting optimal models...")
    
    if custom_model:
        # Use the manually selected model
        selected_models = [custom_model]
    else:
        # Use auto-detection
        selected_models = select_best_models(conditions, was_resized)
    
    # Step 4: Apply models
    current_image = processed_image
    total_models = len(selected_models)
    
    for idx, (category, model_name, model_info) in enumerate(selected_models):
        progress = 30 + int((idx / total_models) * 60)
        
        if progress_callback:
            progress_callback(
                progress,
                f"🤖 Applying {model_name}... ({idx + 1}/{total_models})"
            )
        
        result_image, error = run_model(current_image, category, model_name, model_info)
        
        if error:
            results.append({
                "model": model_name,
                "category": category,
                "success": False,
                "error": error
            })
            # If memory error, try to continue with smaller image
            if "memory" in error.lower():
                # Resize even smaller and continue
                current_image, _, _, _ = smart_resize_image(current_image, max_dimension=1024, target_dimension=1024)
        else:
            results.append({
                "model": model_name,
                "category": category,
                "success": True,
                "image": result_image
            })
            current_image = result_image
    
    if progress_callback:
        progress_callback(100, "✨ Processing complete!")
    
    return current_image, results, conditions, resize_info

# Main app
def main():
    # Initialize session state
    if 'restored_image' not in st.session_state:
        st.session_state.restored_image = None
    if 'processing_results' not in st.session_state:
        st.session_state.processing_results = []
    if 'detected_conditions' not in st.session_state:
        st.session_state.detected_conditions = {}
    if 'resize_info' not in st.session_state:
        st.session_state.resize_info = {}

    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <h1>🖼️ Smart Photo Restoration</h1>
            <p style="font-size: 1.2rem;">AI Auto-Detect & Memory-Optimized Processing</p>
            <p>Upload any photo - automatic resizing prevents memory issues</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ System Info")
        
        if REPLICATE_API_KEY:
            st.success("✅ Replicate API: Connected")
        else:
            st.error("❌ Replicate API Key not found!")
            st.info("Add your API key to the .env file")
            st.stop()
        
        st.markdown("---")
        
        st.header("🛡️ Memory Protection")
        st.markdown(f"""
        **Auto-Resize Enabled:**
        - Max dimension: {MAX_IMAGE_DIMENSION}px
        - Target size: {TARGET_DIMENSION}px
        - Prevents GPU memory errors
        
        **Your images are automatically optimized!**
        """)
        
        st.markdown("---")
        
        st.header("🤖 AI Models")
        st.markdown(f"""
        **Total:** 15 specialized models
        
        - Damage Restoration: 6
        - Colorization: 3
        - Face Enhancement: 4
        - Night Enhancement: 1
        - Auto-detection: ✓
        """)
        
        st.markdown("---")
        
        st.header("ℹ️ How It Works")
        st.markdown("""
        1. 📤 **Upload** photo
        2. 📏 **Auto-resize** if needed
        3. 🔍 **AI analyzes** conditions
        4. 🎯 **Selects** best models
        5. 🤖 **Processes** automatically
        6. ✨ **Download** result
        """)

    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Upload Your Photo")
        uploaded_file = st.file_uploader(
            "Any size - will be optimized automatically",
            type=["jpg", "jpeg", "png", "webp"],
            help=f"Upload a photo (max {MAX_FILE_SIZE_MB}MB) - large images will be auto-resized"
        )
        
        if uploaded_file is not None:
            # Check file size
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > MAX_FILE_SIZE_MB:
                st.error(f"❌ File too large! Max size: {MAX_FILE_SIZE_MB}MB")
                st.stop()
            
            # Display original
            image = Image.open(uploaded_file)
            st.image(image, caption="Original Photo", use_column_width=True)
            
            # Show details and warnings
            width, height = image.size
            max_side = max(width, height)
            
            st.info(f"📏 {width} x {height} px | 💾 {file_size_mb:.2f} MB")
            
            # Warning if image is large
            if max_side > MAX_IMAGE_DIMENSION:
                st.markdown(f"""
                <div class="warning-box">
                    ⚠️ <strong>Large Image Detected</strong><br/>
                    This image will be automatically resized to ~{TARGET_DIMENSION}px to prevent memory issues.<br/>
                    This ensures smooth processing without errors!
                </div>
                """, unsafe_allow_html=True)
            
            # Clear previous results if new file
            if 'last_file' not in st.session_state or st.session_state.last_file != uploaded_file.name:
                st.session_state.restored_image = None
                st.session_state.processing_results = []
                st.session_state.detected_conditions = {}
                st.session_state.resize_info = {}
                st.session_state.last_file = uploaded_file.name
    
    with col2:
        st.subheader("✨ Enhanced Result")
        
        if uploaded_file is not None:
            # Model Selection (Optional)
            st.markdown("#### 🤖 Model Selection (Optional)")
            use_custom_model = st.checkbox("Override Auto-Detection", 
                                        help="Choose a specific model instead of letting AI choose automatically")
            
            custom_model_info = None
            if use_custom_model:
                # Create flattened list of models
                model_options = []
                for category, models in MODELS.items():
                    for model_name, model_info in models.items():
                        model_options.append({
                            "category": category,
                            "name": model_name,
                            "info": model_info,
                            "display": f"{model_name} ({model_info['description']})"
                        })
                
                selected_model = st.selectbox(
                    "Choose Model",
                    options=model_options,
                    format_func=lambda x: x["display"],
                    help="Select a specific model to use for enhancement"
                )
                
                if selected_model:
                    custom_model_info = (
                        selected_model["category"],
                        selected_model["name"],
                        selected_model["info"]
                    )
            
            # Process button
            if st.button("🚀 Auto-Enhance Photo", type="primary"):
                
                # Progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(value, text):
                    progress_bar.progress(value)
                    status_text.text(text)
                
                # Process image
                try:
                    # If custom model is selected, pass it to the function
                    final_image, results, conditions, resize_info = process_image_smart(
                        image,
                        progress_callback=update_progress,
                        custom_model=custom_model_info if use_custom_model else None
                    )
                    
                    # Save results
                    st.session_state.restored_image = final_image
                    st.session_state.processing_results = results
                    st.session_state.detected_conditions = conditions
                    st.session_state.resize_info = resize_info
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.success("✅ Enhancement complete!")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    progress_bar.empty()
                    status_text.empty()
            
            # Display results
            if st.session_state.restored_image is not None:
                st.image(
                    st.session_state.restored_image,
                    caption="Enhanced Photo",
                    use_column_width=True
                )
                
                # Show resize info if applicable
                if st.session_state.resize_info.get("resized"):
                    orig = st.session_state.resize_info["original"]
                    new = st.session_state.resize_info["new"]
                    st.info(f"📏 Resized: {orig[0]}x{orig[1]} → {new[0]}x{new[1]} (memory optimization)")
                
                # Download button
                buffered = BytesIO()
                st.session_state.restored_image.save(buffered, format="PNG", quality=95)
                
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.download_button(
                        "📥 Download Enhanced Photo",
                        buffered.getvalue(),
                        f"enhanced_{int(time.time())}.png",
                        "image/png"
                    )
                with col_b:
                    if st.button("🔄 New"):
                        st.session_state.restored_image = None
                        st.rerun()
        else:
            st.info("👈 Upload a photo to begin")
    
    # Analysis Results
    if st.session_state.detected_conditions:
        st.markdown("---")
        st.header("🔍 AI Analysis Results")
        
        conditions = st.session_state.detected_conditions
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="detection-card">
                <h4>📊 Detected Conditions</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if conditions["is_bw"]:
                st.write(f"🎨 Black & White ({conditions['confidence'].get('bw', 0):.0f}%)")
            if conditions["is_damaged"]:
                st.write(f"🔧 Damaged ({conditions['confidence'].get('damaged', 0):.0f}%)")
            if conditions["has_faces"]:
                st.write(f"👤 Faces ({conditions['confidence'].get('faces', 0):.0f}%)")
            if conditions["is_night"]:
                st.write(f"🌙 Low Light ({conditions['confidence'].get('night', 0):.0f}%)")
            if conditions["is_noisy"]:
                st.write(f"📡 Noisy ({conditions['confidence'].get('noisy', 0):.0f}%)")
            
            if not any([conditions["is_bw"], conditions["is_damaged"], 
                       conditions["has_faces"], conditions["is_night"], conditions["is_noisy"]]):
                st.write("✨ General enhancement applied")
        
        with col2:
            st.markdown("""
            <div class="detection-card">
                <h4>🤖 Models Applied</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for result in st.session_state.processing_results:
                status = "✅" if result["success"] else "❌"
                st.write(f"{status} {result['model']}")
        
        with col3:
            st.markdown("""
            <div class="detection-card">
                <h4>📈 Processing Stats</h4>
            </div>
            """, unsafe_allow_html=True)
            
            total = len(st.session_state.processing_results)
            success = sum(1 for r in st.session_state.processing_results if r["success"])
            st.write(f"Total Steps: {total}")
            st.write(f"Successful: {success}/{total}")
            
            if st.session_state.resize_info.get("resized"):
                st.write("✅ Auto-resized")
    
    # Comparison Section
    if uploaded_file is not None and st.session_state.restored_image is not None:
        st.markdown("---")
        st.header("🔍 Before & After")
        
        comp_col1, comp_col2 = st.columns(2)
        
        with comp_col1:
            st.image(image, caption="Before", use_column_width=True)
        
        with comp_col2:
            st.image(st.session_state.restored_image, caption="After", use_column_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Smart Photo Restoration | Memory-Optimized | 15 AI Models</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()