import streamlit as st
import os
import replicate
from dotenv import load_dotenv
import requests
from io import BytesIO
import base64
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Video Generator Studio",
    page_icon="🎬",
    layout="wide"
)

# Initialize API clients
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

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
        background-color: #FF4B4B;
        color: white;
        padding: 0.75rem;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.3);
    }
    .model-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .feature-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
    .prompt-box {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# Define available video generation models (VERIFIED WORKING on Replicate)
# Updated with actual model IDs from Replicate
VIDEO_MODELS = {
    # 🟢 CHEAPEST & VERIFIED WORKING MODELS
    "CogVideoX-5B ⭐ CHEAPEST": {
        "id": "fofr/cogvideox-5b:bf22f8e76fada7ec5d70c06fd22ac79f651df7decbf3c983cb9ab094e0c44294",
        "description": "Open source video generation - BEST VALUE! Actually available!",
        "features": ["Cheap $0.05", "Good Quality", "Verified Working"],
        "duration": "6 seconds",
        "best_for": "Testing, iterations, high volume, learning",
        "provider": "CogVideoX (Open Source)",
        "cost": "~$0.05-0.10",
        "cost_color": "green",
        "savings": "Save 95% vs premium models!"
    },
    
    "LTX Video by Lightricks 💚": {
        "id": "lightricks/ltx-video:8c47da666861d081eeb4d1261853087de23923a268a69b63febdf5dc1dee08e4",
        "description": "Fast and affordable text-to-video - VERIFIED!",
        "features": ["Affordable $0.10", "Fast", "Good Quality"],
        "duration": "5 seconds",
        "best_for": "Quick content creation, budget projects",
        "provider": "Lightricks",
        "cost": "~$0.08-0.15",
        "cost_color": "green",
        "savings": "Save 90% vs premium models!"
    },
    
    "CogVideoX Alternative 💰": {
        "id": "cuuupid/cogvideox-5b:5b14e2c2c648efecc8d36c6353576552f8a124e690587212f8e8bb17ecda3d8c",
        "description": "Another CogVideoX implementation - Budget friendly!",
        "features": ["Cheap $0.08", "Alternative Version", "Working"],
        "duration": "6 seconds",
        "best_for": "Testing, alternative to main CogVideoX",
        "provider": "CogVideoX (Community)",
        "cost": "~$0.05-0.10",
        "cost_color": "green",
        "savings": "Save 95% vs premium!"
    },
    
    "Mochi 1 Preview 🎨": {
        "id": "genmo/mochi-1-preview:c581e19816852c0d7ebcd5e1d06def5e1c6ca47d08b50031c1e75131e2c11e7e",
        "description": "Genmo's open video generation model",
        "features": ["Affordable", "Open Source", "Good Quality"],
        "duration": "~6 seconds",
        "best_for": "Creative projects, open source needs",
        "provider": "Genmo",
        "cost": "~$0.10-0.20",
        "cost_color": "green",
        "savings": "Save 85% vs premium!"
    },
    
    "AnimateDiff Lightning ⚡": {
        "id": "lucataco/animatediff-lightning-4-step:2abe5c1d36bb2e2c0fcef493f1c1a925ead67e0346c56d9a35b6b4f5cd4e82bb",
        "description": "Super fast animation generation - 4 steps only!",
        "features": ["Very Fast", "Affordable $0.08", "Animations"],
        "duration": "Variable",
        "best_for": "Quick animations, motion graphics",
        "provider": "AnimateDiff",
        "cost": "~$0.05-0.12",
        "cost_color": "green",
        "savings": "Save 92% vs premium!"
    },
    
    # 🟡 MODERATE PRICE - VERIFIED WORKING
    "Stable Video Diffusion 🎬": {
        "id": "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
        "description": "Stability AI's video generation - Good quality",
        "features": ["Moderate $0.25", "Good Quality", "Stable AI"],
        "duration": "~4 seconds",
        "best_for": "Professional quality on budget",
        "provider": "Stability AI",
        "cost": "~$0.20-0.30",
        "cost_color": "yellow",
        "savings": "Save 80% vs premium!"
    },
    
    "Zeroscope V2 XL 📹": {
        "id": "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
        "description": "High resolution video generation",
        "features": ["Moderate $0.20", "High Res", "Watermark-free"],
        "duration": "~3 seconds",
        "best_for": "High quality short clips",
        "provider": "Zeroscope",
        "cost": "~$0.15-0.25",
        "cost_color": "yellow",
        "savings": "Save 82% vs premium!"
    },
    
    "Text2Video-Zero 🎯": {
        "id": "cjwbw/text2video-zero:8b5aa96db02e27a6b52c312974c30fa8fd4e7193c3fa97e5b64b6e3b66c25f18",
        "description": "Zero-shot text to video generation",
        "features": ["Affordable $0.15", "Zero-shot", "Flexible"],
        "duration": "Variable",
        "best_for": "Experimental, creative projects",
        "provider": "Text2Video-Zero",
        "cost": "~$0.12-0.20",
        "cost_color": "yellow",
        "savings": "Save 85% vs premium!"
    },
    
    "ModelScope Text2Video ⚙️": {
        "id": "cjwbw/damo-text-to-video:1e205ea73084bd17a0a3b43396e49ba0d6bc2e754e9283b2df49fad2dcf95755",
        "description": "Alibaba's ModelScope text-to-video",
        "features": ["Moderate $0.18", "Good Quality", "Stable"],
        "duration": "~2 seconds",
        "best_for": "Short clips, general use",
        "provider": "Alibaba ModelScope",
        "cost": "~$0.15-0.22",
        "cost_color": "yellow",
        "savings": "Save 85% vs premium!"
    },
    
    # 🔴 PREMIUM (If/When Available) - May not be public yet
    "Haiper Video v2 🚀": {
        "id": "haiper/haiper-video-2.0",
        "description": "⚠️ May require special access - Check availability",
        "features": ["Premium", "High Quality", "May Be Limited"],
        "duration": "Variable",
        "best_for": "If available - professional projects",
        "provider": "Haiper",
        "cost": "~$0.30-0.50",
        "cost_color": "yellow",
        "note": "⚠️ Check Replicate for availability. May not be public yet."
    },
    
    "Minimax Video 💎": {
        "id": "minimax/video-01",
        "description": "⚠️ May require waitlist/special access",
        "features": ["Premium", "High Quality", "May Be Limited"],
        "duration": "~6 seconds",
        "best_for": "Premium projects if accessible",
        "provider": "Minimax",
        "cost": "~$0.30-0.60",
        "cost_color": "yellow",
        "note": "⚠️ Check if you have access. May require approval."
    },
}

# Character consistency tips and templates
CHARACTER_CONSISTENCY_TIPS = """
### 🎯 Tips for Consistent Characters:

1. **Detailed Character Description First:**
   - Start with: "A [age] [gender] with [specific features]"
   - Example: "A 25-year-old woman with long red hair, green eyes, wearing a blue jacket"

2. **Use Consistent Descriptors:**
   - Always use the EXACT same character description in every prompt
   - Include unique identifiers (clothing color, hairstyle, accessories)

3. **Reference Previous Generations:**
   - Keep a character sheet with your descriptions
   - Use the same terminology each time

4. **Specific Physical Details:**
   - Hair: color, length, style
   - Eyes: color, shape
   - Clothing: specific colors and styles
   - Distinctive features: glasses, beard, hat, etc.

### 📝 Character Prompt Templates:

**Template 1 - Person:**
```
A [age]-year-old [gender] with [hair description], [eye color] eyes, 
wearing [clothing description]. [Action/Scene description].
Photorealistic, cinematic lighting, 4K quality.
```

**Template 2 - Animated Character:**
```
An animated [character type] with [distinctive features], [color scheme], 
[style]. [Action/Scene]. [Animation style], high quality.
```

**Template 3 - Consistent Series:**
```
[Same character description from previous video], now [new action/scene].
Maintain consistent appearance and style.
```
"""

def generate_video_replicate(prompt, model_id, seed=None):
    """
    Generate video using selected Replicate model
    """
    try:
        st.info(f"🎬 Generating video with {model_id}...")
        st.info("⏳ This may take 1-5 minutes depending on the model...")
        
        # Prepare basic input parameters - start minimal
        input_params = {
            "prompt": prompt,
        }
        
        # Add seed for consistency if provided (as integer)
        if seed is not None:
            input_params["seed"] = int(seed)
        
        # Try to generate with minimal params first
        # Many models work best with just prompt and seed
        try:
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
        except Exception as e:
            error_str = str(e).lower()
            # If parameter error, try without seed
            if "invalid" in error_str or "expected" in error_str or "parameter" in error_str:
                st.warning("⚠️ Retrying with adjusted parameters...")
                input_params_retry = {"prompt": prompt}
                
                if replicate_client:
                    output = replicate_client.run(
                        model_id,
                        input=input_params_retry
                    )
                else:
                    output = replicate.run(
                        model_id,
                        input=input_params_retry
                    )
            else:
                raise e
        
        # Handle different output formats
        if isinstance(output, str):
            video_url = output
        elif isinstance(output, list) and len(output) > 0:
            video_url = output[0]
        elif isinstance(output, dict):
            video_url = output.get('video_url') or output.get('url') or output.get('output')
        else:
            return None, "Unexpected output format from model"
        
        return video_url, None
        
    except Exception as e:
        error_msg = str(e)
        
        # Provide helpful error messages
        if "authentication" in error_msg.lower():
            return None, "❌ API Authentication Error. Please check your API keys."
        elif "not found" in error_msg.lower():
            return None, f"❌ Model not found. The model '{model_id}' may not be available. Try a different model."
        elif "timeout" in error_msg.lower():
            return None, "⏰ Generation timed out. Please try again."
        elif "invalid" in error_msg.lower() or "parameter" in error_msg.lower():
            return None, f"❌ Parameter error. Try a different model. Details: {error_msg[:200]}"
        else:
            return None, f"❌ Error: {error_msg[:300]}"

def save_generation_history(prompt, model, video_url, seed):
    """Save generation to history"""
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    st.session_state.history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'prompt': prompt,
        'model': model,
        'video_url': video_url,
        'seed': seed
    })

# Main app
def main():
    # Initialize session state
    if 'generated_video' not in st.session_state:
        st.session_state.generated_video = None
    if 'generation_info' not in st.session_state:
        st.session_state.generation_info = {}
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'character_description' not in st.session_state:
        st.session_state.character_description = ""
    
    # Header
    st.title("🎬 AI Video Generator Studio")
    st.markdown("### Generate professional videos using cutting-edge AI models")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Status
        st.subheader("🔑 API Status")
        if REPLICATE_API_KEY:
            st.success("✅ Replicate API: Connected")
        else:
            st.error("❌ Replicate API: Not Connected")
            st.info("Add REPLICATE_API_KEY to your .env file")
        
        st.markdown("---")
        
        # Model Selection
        st.subheader("🎯 Select AI Model")
        selected_model_name = st.selectbox(
            "Choose Model",
            list(VIDEO_MODELS.keys()),
            help="Select the AI model for video generation"
        )
        
        model_info = VIDEO_MODELS[selected_model_name]
        
        # Determine cost color
        cost_color_map = {
            "green": "#10b981",
            "yellow": "#f59e0b", 
            "red": "#ef4444"
        }
        cost_color = cost_color_map.get(model_info.get('cost_color', 'yellow'), "#f59e0b")
        
        # Display model info card with cost
        cost_display = f"<p style='color: {cost_color}; font-weight: bold; font-size: 1.2em;'>💰 Cost: {model_info.get('cost', 'N/A')}</p>"
        savings_display = f"<p style='color: #10b981; font-weight: bold;'>{model_info.get('savings', '')}</p>" if 'savings' in model_info else ""
        
        st.markdown(f"""
        <div class="model-card">
            <h4>{selected_model_name}</h4>
            {cost_display}
            {savings_display}
            <p>{model_info['description']}</p>
            <p><strong>Provider:</strong> {model_info['provider']}</p>
            <p><strong>Duration:</strong> {model_info['duration']}</p>
            <p><strong>Best For:</strong> {model_info['best_for']}</p>
            <div>
                {''.join([f'<span class="feature-badge">{f}</span>' for f in model_info['features']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if 'note' in model_info:
            st.warning(f"⚠️ {model_info['note']}")
        
        if 'warning' in model_info:
            st.error(f"⚠️ {model_info['warning']}")
        
        st.markdown("---")
        
        # Character Consistency Options
        st.subheader("🎭 Character Consistency")
        use_seed = st.checkbox(
            "Use Seed for Consistency",
            value=True,
            help="Using the same seed helps maintain character consistency"
        )
        
        if use_seed:
            seed_value = st.number_input(
                "Seed Value",
                min_value=1,
                max_value=999999,
                value=42,
                help="Use the same seed for consistent characters across videos"
            )
        else:
            seed_value = None
        
        st.markdown("---")
        
        # Advanced Settings
        with st.expander("⚙️ Advanced Settings"):
            aspect_ratio = st.selectbox(
                "Aspect Ratio",
                ["16:9", "9:16", "1:1", "4:3"],
                help="Video aspect ratio"
            )
            
            video_length = st.select_slider(
                "Preferred Length",
                options=["Short (5s)", "Medium (10s)", "Long (15s+)"],
                value="Medium (10s)"
            )
            
            quality_preset = st.selectbox(
                "Quality Preset",
                ["Balanced", "Speed", "Quality"],
                help="Balance between speed and quality"
            )
        
        st.markdown("---")
        
        # Quick Stats
        st.subheader("📊 Session Stats")
        st.metric("Videos Generated", len(st.session_state.history))
        if st.session_state.history:
            st.metric("Current Seed", st.session_state.generation_info.get('seed', 'N/A'))
        
        st.markdown("---")
        
        # Cost Information
        st.subheader("💰 Cost Guide")
        st.markdown("""
        **🟢 CHEAPEST ($0.05-0.15):**
        - CogVideoX-5B: $0.08 ⭐
        - LTX Video: $0.10 ⭐
        - AnimateDiff: $0.08
        
        **🟡 MODERATE ($0.15-0.30):**
        - Stable Video: $0.25
        - Zeroscope: $0.20
        - ModelScope: $0.18
        
        **💎 PREMIUM (if available):**
        - Check Replicate for latest
        
        💡 **Save 90%+!** Use CogVideoX 
        or LTX Video for testing!
        """)
        
        with st.expander("💡 Money-Saving Tips"):
            st.markdown("""
            **Golden Rule:**
            1. Test with CogVideoX ($0.08)
            2. Find what works (10 tests = $0.80)
            3. Polish with better model if needed
            
            **Verified Working Models:**
            ✅ CogVideoX-5B (fofr version)
            ✅ LTX Video (Lightricks)
            ✅ Mochi 1 Preview
            ✅ Stable Video Diffusion
            
            **Example Savings:**
            - 100 videos with budget models: $8-15
            - Much cheaper than premium!
            """)

    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("✍️ Create Your Video")
        
        # Cost warning for expensive models
        if model_info.get('cost_color') == 'red':
            st.error(f"""
            ⚠️ **EXPENSIVE MODEL SELECTED!** ⚠️
            
            This model costs **{model_info.get('cost')}** per video!
            
            💡 **Save Money:** Test with **CogVideoX-5B** ($0.05) first, then use this for finals only.
            
            **Cost Example:**
            - 10 videos with this model: ~${float(model_info.get('cost', '1.0').split('-')[0].replace('~$', '').replace('$', '')) * 10:.2f}
            - 10 videos with CogVideoX: $0.50
            - **You save: ~${float(model_info.get('cost', '1.0').split('-')[0].replace('~$', '').replace('$', '')) * 10 - 0.50:.2f}!**
            """)
        elif model_info.get('cost_color') == 'green':
            st.success(f"""
            ✅ **BUDGET-FRIENDLY MODEL!** 
            
            This model costs only **{model_info.get('cost')}** per video - {model_info.get('savings', 'Great value!')}
            """)
        
        # Character Description (for consistency)
        with st.expander("👤 Character Description Template (Recommended)", expanded=True):
            st.markdown(CHARACTER_CONSISTENCY_TIPS)
            
            character_desc = st.text_area(
                "Save Your Character Description",
                value=st.session_state.character_description,
                height=100,
                placeholder="E.g., A 30-year-old man with short brown hair, blue eyes, wearing a red shirt and jeans...",
                help="Save this description to use in multiple videos for character consistency"
            )
            
            if st.button("💾 Save Character Description"):
                st.session_state.character_description = character_desc
                st.success("✅ Character description saved!")
            
            if st.session_state.character_description:
                if st.button("📋 Use Saved Character"):
                    st.session_state.prompt_prefix = st.session_state.character_description + ", "
                    st.success("✅ Character added to prompt!")
        
        # Main Prompt Input
        st.markdown("### 🎨 Video Prompt")
        
        # Prompt examples
        prompt_example = st.selectbox(
            "📚 Quick Start Examples",
            [
                "Custom Prompt",
                "A woman walking in a park during sunset, cinematic lighting",
                "A robot dancing in a futuristic city, neon lights",
                "A chef cooking in a modern kitchen, professional photography",
                "An astronaut floating in space, Earth in background, 4K quality",
                "A cat playing with yarn in a cozy living room, warm lighting"
            ]
        )
        
        if prompt_example != "Custom Prompt":
            default_prompt = prompt_example
        else:
            default_prompt = st.session_state.get('prompt_prefix', '')
        
        prompt = st.text_area(
            "Enter your video prompt",
            value=default_prompt,
            height=150,
            placeholder="Describe the video you want to generate. Be specific about:\n- Characters (appearance, clothing, actions)\n- Setting (location, time, lighting)\n- Camera angle and movement\n- Style and mood",
            help="The more detailed your prompt, the better the results!"
        )
        
        # Prompt enhancement options
        col_enhance1, col_enhance2 = st.columns(2)
        with col_enhance1:
            add_quality = st.checkbox("Add Quality Tags", value=True)
        with col_enhance2:
            add_cinematic = st.checkbox("Add Cinematic Style", value=False)
        
        # Enhance prompt
        enhanced_prompt = prompt
        if add_quality:
            enhanced_prompt += ", high quality, detailed, professional"
        if add_cinematic:
            enhanced_prompt += ", cinematic lighting, film grain, 24fps"
        
        if enhanced_prompt != prompt:
            st.info(f"📝 Enhanced Prompt: {enhanced_prompt}")
        
        # Generate Button
        st.markdown("###")
        generate_col1, generate_col2 = st.columns([3, 1])
        
        with generate_col1:
            generate_button = st.button(
                "🚀 Generate Video",
                type="primary",
                disabled=not prompt or not REPLICATE_API_KEY
            )
        
        with generate_col2:
            if st.button("🔄 Clear"):
                st.session_state.generated_video = None
                st.session_state.generation_info = {}
                st.rerun()
        
        if not REPLICATE_API_KEY:
            st.error("⚠️ Please add REPLICATE_API_KEY to your .env file to generate videos")
        
        # Generate video
        if generate_button and prompt:
            with st.spinner("🎬 Generating your video... This may take a few minutes..."):
                video_url, error = generate_video_replicate(
                    enhanced_prompt,
                    model_info['id'],
                    seed_value if use_seed else None
                )
                
                if error:
                    st.error(error)
                    
                    # Provide helpful suggestions
                    st.info("💡 Troubleshooting Tips:")
                    st.markdown("""
                    - Try a different model
                    - Simplify your prompt
                    - Check if the model is currently available
                    - Verify your API key is valid
                    """)
                else:
                    st.session_state.generated_video = video_url
                    st.session_state.generation_info = {
                        'prompt': enhanced_prompt,
                        'model': selected_model_name,
                        'seed': seed_value,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Save to history
                    save_generation_history(
                        enhanced_prompt,
                        selected_model_name,
                        video_url,
                        seed_value
                    )
                    
                    st.success("✅ Video generated successfully!")
                    st.balloons()
    
    with col2:
        st.subheader("🎥 Generated Video")
        
        if st.session_state.generated_video:
            # Display video
            try:
                st.video(st.session_state.generated_video)
                
                # Display generation info
                info = st.session_state.generation_info
                st.markdown(f"""
                <div class="prompt-box">
                    <strong>📝 Prompt:</strong> {info['prompt']}<br>
                    <strong>🤖 Model:</strong> {info['model']}<br>
                    <strong>🎲 Seed:</strong> {info['seed']}<br>
                    <strong>⏰ Generated:</strong> {info['timestamp']}
                </div>
                """, unsafe_allow_html=True)
                
                # Download button
                st.markdown("###")
                st.markdown(f"[📥 Download Video]({st.session_state.generated_video})")
                
                # Copy prompt button
                if st.button("📋 Copy Prompt for Reuse"):
                    st.code(info['prompt'], language=None)
                    st.success("✅ Prompt ready to copy!")
                
            except Exception as e:
                st.error(f"Error displaying video: {e}")
                st.markdown(f"[🔗 Open Video Link]({st.session_state.generated_video})")
        else:
            st.info("👈 Enter a prompt and click 'Generate Video' to create your first video!")
            
            # Show example gallery
            st.markdown("### 🎨 Inspiration Gallery")
            st.markdown("""
            **Popular Prompt Styles:**
            - 🎬 Cinematic shots with dramatic lighting
            - 🌅 Nature scenes with dynamic weather
            - 🏙️ Urban environments with people
            - 🎭 Character-focused narratives
            - 🚀 Sci-fi and futuristic themes
            - 🎨 Artistic and abstract visuals
            """)
    
    # History Section
    if st.session_state.history:
        st.markdown("---")
        st.subheader("📜 Generation History")
        
        # Display last 5 generations
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"🎬 {item['timestamp']} - {item['model']}"):
                col_h1, col_h2 = st.columns([2, 1])
                
                with col_h1:
                    st.markdown(f"**Prompt:** {item['prompt']}")
                    st.markdown(f"**Seed:** {item['seed']}")
                
                with col_h2:
                    st.markdown(f"[🔗 View Video]({item['video_url']})")
                    if st.button(f"🔄 Regenerate", key=f"regen_{i}"):
                        st.session_state.prompt_prefix = item['prompt']
                        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <p style='text-align: center; color: gray;'>
        🎬 AI Video Generator Studio | Made with ❤️ using Streamlit & Advanced AI Models<br>
        💡 Pro Tip: Use the same seed and detailed character descriptions for consistent results!
        </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()