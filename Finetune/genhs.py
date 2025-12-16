import replicate
import os

# ============================================
# CONFIGURATION
# ============================================

# Your Replicate API token
REPLICATE_API_TOKEN = "your_api_token_here"

# Your trained model
MODEL_NAME = "bod1411/quest-headshot"

# Trigger word (same as what you used during training)
TRIGGER_WORD = "QSTSHOT"

# ============================================
# SCRIPT START
# ============================================

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

def generate_headshot(prompt, num_images=1, aspect_ratio="1:1", output_format="png"):
    """
    Generate headshots using your trained model
    
    Args:
        prompt: Your text prompt (must include trigger word)
        num_images: Number of images to generate (1-4)
        aspect_ratio: Image ratio ("1:1", "16:9", "9:16", "3:2", "2:3")
        output_format: "png" or "jpg"
    """
    
    # Make sure trigger word is in prompt
    if TRIGGER_WORD not in prompt:
        print(f"⚠️  Warning: Trigger word '{TRIGGER_WORD}' not found in prompt!")
        print(f"   Adding it automatically...")
        prompt = f"{TRIGGER_WORD} {prompt}"
    
    print(f"🎨 Generating {num_images} image(s)...")
    print(f"   Prompt: {prompt}")
    print(f"   Aspect ratio: {aspect_ratio}")
    
    try:
        output = replicate.run(
            MODEL_NAME,
            input={
                "prompt": prompt,
                "num_outputs": num_images,
                "aspect_ratio": aspect_ratio,
                "output_format": output_format,
                "output_quality": 100,
            }
        )
        
        print(f"\n✅ Generation complete!")
        print(f"   Generated {len(output)} image(s):")
        
        for i, image_url in enumerate(output, 1):
            print(f"   {i}. {image_url}")
        
        return output
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   - Make sure your model training is complete")
        print(f"   - Check model exists at: https://replicate.com/{MODEL_NAME}")
        print("   - Verify your API token is correct")
        return None

def save_images(image_urls, output_folder="./generated_images"):
    """
    Download and save generated images locally
    """
    import requests
    from pathlib import Path
    
    output_path = Path(output_folder)
    output_path.mkdir(exist_ok=True)
    
    print(f"\n💾 Saving images to {output_folder}...")
    
    for i, url in enumerate(image_urls, 1):
        response = requests.get(url)
        if response.status_code == 200:
            filename = output_path / f"headshot_{i}.png"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"   ✅ Saved: {filename}")
        else:
            print(f"   ❌ Failed to download image {i}")

# ============================================
# EXAMPLE PROMPTS
# ============================================

EXAMPLE_PROMPTS = [
    "professional headshot, studio lighting, corporate attire, neutral background",
    "casual outdoor portrait, natural lighting, smiling, park background",
    "creative portrait, dramatic lighting, artistic, dark background",
    "linkedin profile photo, business suit, confident expression",
    "headshot as a doctor, white medical coat, hospital background",
]

def main():
    print("=" * 50)
    print("🎨 HEADSHOT GENERATION SCRIPT")
    print("=" * 50)
    print(f"\nModel: {MODEL_NAME}")
    print(f"Trigger word: {TRIGGER_WORD}")
    
    # Example: Generate one professional headshot
    prompt = EXAMPLE_PROMPTS[0]
    
    images = generate_headshot(
        prompt=prompt,
        num_images=1,
        aspect_ratio="1:1"
    )
    
    if images:
        # Optionally save images locally
        save_images(images)
        
        print("\n" + "=" * 50)
        print("💡 TRY OTHER PROMPTS:")
        print("=" * 50)
        for i, example in enumerate(EXAMPLE_PROMPTS[1:], 2):
            print(f"{i}. {TRIGGER_WORD} {example}")
        
        print("\n📝 To generate with custom prompt, edit the script or use:")
        print(f"   generate_headshot('your custom prompt here')")

if __name__ == "__main__":
    main()