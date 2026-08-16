import replicate
import os
import requests
from pathlib import Path

# ============================================
# CONFIGURATION
# ============================================

# Your Replicate API token
REPLICATE_API_TOKEN = "r8_bdXUILyd8ZK3k0LyKeMwvQqJjuAXUdq1DoJKz"

# Your trained model
MODEL_NAME = "bod1411/aman-video"

# Trigger word (same as what you used during training)
TRIGGER_WORD = "AMANVID"

# ============================================
# SCRIPT START
# ============================================

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

def generate_video(prompt, num_frames=81, aspect_ratio="16:9", output_path="./generated_videos"):
    """
    Generate a video using your trained model
    
    Args:
        prompt: Your text prompt (must include trigger word)
        num_frames: Number of frames (81 = ~5 seconds, 161 = ~10 seconds)
        aspect_ratio: Video ratio ("16:9", "9:16", "1:1")
        output_path: Where to save generated videos
    """
    
    # Make sure trigger word is in prompt
    if TRIGGER_WORD not in prompt:
        print(f"⚠️  Warning: Trigger word '{TRIGGER_WORD}' not found in prompt!")
        print(f"   Adding it automatically...")
        prompt = f"{TRIGGER_WORD} {prompt}"
    
    print(f"🎬 Generating video...")
    print(f"   Model: {MODEL_NAME}")
    print(f"   Prompt: {prompt}")
    print(f"   Frames: {num_frames} (~{num_frames/16:.1f} seconds)")
    print(f"   Aspect ratio: {aspect_ratio}")
    print(f"\n⏳ This may take 2-5 minutes...")
    
    try:
        output = replicate.run(
            MODEL_NAME,
            input={
                "prompt": prompt,
                "num_frames": num_frames,
                "aspect_ratio": aspect_ratio,
                "num_inference_steps": 50,  # Higher = better quality, slower
            }
        )
        
        print(f"\n✅ Video generation complete!")
        
        # Output is a URL to the video file
        video_url = output
        print(f"   Video URL: {video_url}")
        
        # Download the video
        output_dir = Path(output_path)
        output_dir.mkdir(exist_ok=True)
        
        # Generate filename
        import time
        timestamp = int(time.time())
        filename = f"video_{timestamp}.mp4"
        filepath = output_dir / filename
        
        print(f"\n💾 Downloading video...")
        response = requests.get(video_url)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"   ✅ Saved to: {filepath}")
        else:
            print(f"   ❌ Failed to download video")
        
        return video_url, filepath
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   - Make sure your model training is complete")
        print(f"   - Check model exists at: https://replicate.com/{MODEL_NAME}")
        print("   - Verify your API token is correct")
        return None, None

# ============================================
# EXAMPLE PROMPTS
# ============================================

EXAMPLE_PROMPTS = [
    "playing in a park, sunny day, smiling and running",
    "close up portrait, looking at camera, natural lighting",
    "waving at camera, outdoor setting, happy expression",
    "playing with toys, indoor setting, energetic",
    "eating snack, kitchen background, casual",
]

def main():
    print("=" * 70)
    print("🎬 VIDEO GENERATION SCRIPT")
    print("=" * 70)
    print(f"\nModel: {MODEL_NAME}")
    print(f"Trigger word: {TRIGGER_WORD}")
    print()
    
    # Check if model exists
    try:
        model = replicate.models.get(MODEL_NAME)
        print(f"✅ Model found: https://replicate.com/{MODEL_NAME}")
    except:
        print(f"❌ Model not found: {MODEL_NAME}")
        print(f"\n💡 Make sure:")
        print(f"   1. Your training is complete")
        print(f"   2. The model name is correct")
        print(f"   3. The model is public or you have access")
        return
    
    print("\n" + "=" * 70)
    print("📝 EXAMPLE PROMPTS:")
    print("=" * 70)
    for i, example in enumerate(EXAMPLE_PROMPTS, 1):
        print(f"{i}. {TRIGGER_WORD} {example}")
    
    print("\n" + "=" * 70)
    print("🎥 GENERATING SAMPLE VIDEO")
    print("=" * 70)
    
    # Generate one sample video
    sample_prompt = EXAMPLE_PROMPTS[0]
    
    video_url, filepath = generate_video(
        prompt=sample_prompt,
        num_frames=81,  # ~5 seconds
        aspect_ratio="16:9"
    )
    
    if video_url:
        print("\n" + "=" * 70)
        print("💡 NEXT STEPS:")
        print("=" * 70)
        print("1. Check the generated video in ./generated_videos/")
        print("2. Try different prompts by modifying the script")
        print("3. Adjust num_frames for longer/shorter videos:")
        print("   • 81 frames = ~5 seconds")
        print("   • 161 frames = ~10 seconds")
        print("4. Try different aspect ratios:")
        print("   • '16:9' - Landscape (YouTube)")
        print("   • '9:16' - Portrait (TikTok, Instagram Stories)")
        print("   • '1:1' - Square (Instagram)")
        print("\n🎨 Custom Generation:")
        print("   Edit this script and change the prompt to generate")
        print("   your own custom videos!")

def generate_custom_videos():
    """
    Generate multiple videos with different prompts
    """
    custom_prompts = [
        ("playing soccer, outdoor field, action shot", 81, "16:9"),
        ("portrait, looking at camera, smiling", 81, "9:16"),
        ("running towards camera, slow motion effect", 161, "16:9"),
    ]
    
    print("\n🎬 Generating multiple custom videos...")
    
    for prompt, frames, ratio in custom_prompts:
        print(f"\n{'='*70}")
        video_url, filepath = generate_video(
            prompt=prompt,
            num_frames=frames,
            aspect_ratio=ratio
        )
        
        if not video_url:
            print(f"⚠️  Skipping to next video...")
            continue
    
    print(f"\n{'='*70}")
    print("✅ All videos generated!")
    print(f"   Check ./generated_videos/ folder")

if __name__ == "__main__":
    # Uncomment one of these options:
    
    # Option 1: Generate one sample video
    main()
    
    # Option 2: Generate multiple custom videos
    # generate_custom_videos()