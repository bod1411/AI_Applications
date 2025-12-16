import replicate
import os
import zipfile
from pathlib import Path
import sys
import tempfile
import shutil

# ============================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================

# Your Replicate API token (get it from https://replicate.com/account/api-tokens)
REPLICATE_API_TOKEN = "r8_bdXUILyd8ZK3k0LyKeMwvQqJjuAXUdq1DoJKz"

# Path to folder containing your training images
TRAINING_IMAGES_FOLDER = "./training_images"

# Your destination model name
DESTINATION_MODEL = "bod1411/quest-headshot"

# Trigger word for your model (use this in prompts later)
TRIGGER_WORD = "QSTSHOT"

# Training parameters
TRAINING_STEPS = 1000
LEARNING_RATE = 0.0004

# ============================================
# SCRIPT START
# ============================================

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

def create_training_zip(image_folder):
    """
    Create a zip file from your training images (using temp directory to avoid OneDrive issues)
    """
    print(f"📦 Creating zip file from {image_folder}...")
    
    # Get absolute path
    image_folder_path = Path(image_folder).resolve()
    print(f"   Full path: {image_folder_path}")
    
    if not image_folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {image_folder_path}")
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP']
    image_files = []
    
    for file_path in image_folder_path.iterdir():
        if file_path.is_file() and file_path.suffix in image_extensions:
            image_files.append(file_path)
    
    if len(image_files) == 0:
        raise ValueError(f"No images found in {image_folder_path}")
    
    print(f"✅ Found {len(image_files)} images")
    
    # Create zip in temp directory first (to avoid OneDrive sync issues)
    temp_dir = Path(tempfile.gettempdir())
    temp_zip = temp_dir / "replicate_training_data.zip"
    print(f"📦 Creating zip in temp location first...")
    print(f"   Temp path: {temp_zip}")
    
    # Remove old temp zip if exists
    if temp_zip.exists():
        temp_zip.unlink()
    
    try:
        # Create zip file
        with zipfile.ZipFile(str(temp_zip), 'w', zipfile.ZIP_DEFLATED) as zipf:
            for image_file in image_files:
                arcname = image_file.name
                zipf.write(str(image_file), arcname)
                print(f"   ✓ Added: {arcname}")
        
        # Verify temp zip was created
        if not temp_zip.exists():
            raise FileNotFoundError(f"Temp zip was not created at {temp_zip}")
        
        file_size_mb = temp_zip.stat().st_size / (1024 * 1024)
        print(f"✅ Zip created in temp directory!")
        print(f"   Size: {file_size_mb:.2f} MB")
        
        # Use C:\personel folder to avoid OneDrive issues
        safe_dir = Path("C:/personel")
        
        # Create the directory if it doesn't exist
        if not safe_dir.exists():
            print(f"\n📁 Creating directory: {safe_dir}")
            safe_dir.mkdir(parents=True, exist_ok=True)
        
        final_zip = safe_dir / "training_data.zip"
        print(f"\n📋 Copying to safe location (outside OneDrive)...")
        print(f"   Destination: {final_zip}")
        
        # Remove old final zip if exists
        if final_zip.exists():
            final_zip.unlink()
        
        shutil.copy2(str(temp_zip), str(final_zip))
        
        if not final_zip.exists():
            # If copy failed, just use temp file
            print(f"⚠️  Copy failed, will use temp file directly")
            return str(temp_zip)
        
        print(f"✅ Zip file ready!")
        print(f"   Location: {final_zip}")
        
        return str(final_zip)
        
    except Exception as e:
        print(f"❌ Error creating zip file: {e}")
        raise

def start_training(zip_file_path):
    """
    Start the training process on Replicate
    """
    print(f"\n🚀 Starting training on Replicate...")
    print(f"   Model destination: {DESTINATION_MODEL}")
    print(f"   Trigger word: {TRIGGER_WORD}")
    print(f"   Steps: {TRAINING_STEPS}")
    
    # Verify zip file exists
    zip_path = Path(zip_file_path)
    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file not found at: {zip_path}")
    
    print(f"   Zip file: {zip_path}")
    print(f"   Uploading to Replicate (this may take a minute)...")
    
    try:
        with open(zip_path, "rb") as zip_file:
            training = replicate.trainings.create(
                version="replicate/fast-flux-trainer:8b10794665aed907bb98a1a5324cd1d3a8bea0e9b31e65210967fb9c9e2e08ed",
                input={
                    "input_images": zip_file,
                    "trigger_word": TRIGGER_WORD,
                    "steps": TRAINING_STEPS,
                    "learning_rate": LEARNING_RATE,
                    "lora_rank": 16,
                    "batch_size": 1,
                },
                destination=DESTINATION_MODEL
            )
        
        print(f"\n✅ Training started!")
        print(f"   Training ID: {training.id}")
        print(f"   Status: {training.status}")
        print(f"   View progress: https://replicate.com/p/{training.id}")
        
        return training
        
    except Exception as e:
        print(f"❌ Error starting training: {e}")
        raise

def check_training_status(training_id):
    """
    Check the status of your training
    """
    try:
        training = replicate.trainings.get(training_id)
        print(f"\n📊 Training Status: {training.status}")
        
        if training.status == "succeeded":
            print(f"✅ Training completed successfully!")
            print(f"   Model: {DESTINATION_MODEL}")
            print(f"\n🎨 Example prompt to test:")
            print(f'   "{TRIGGER_WORD} professional headshot, studio lighting, neutral background"')
            
        elif training.status == "failed":
            print(f"❌ Training failed")
            if training.error:
                print(f"   Error: {training.error}")
        
        elif training.status in ["starting", "processing"]:
            print(f"⏳ Training in progress... Check back in a few minutes")
        
        return training
        
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        raise

def main():
    """
    Main function to run the training pipeline
    """
    print("=" * 60)
    print("🎯 HEADSHOT FINE-TUNING SCRIPT (OneDrive Compatible)")
    print("=" * 60)
    print(f"📂 Working directory: {Path.cwd()}")
    print()
    
    # Verify configuration
    if REPLICATE_API_TOKEN == "your_api_token_here":
        print("❌ ERROR: You need to set your REPLICATE_API_TOKEN!")
        print("   Get it from: https://replicate.com/account/api-tokens")
        print("   Then update it in the script.")
        return
    
    try:
        # Step 1: Create zip file
        print("Step 1: Creating training data archive")
        print("-" * 60)
        zip_file = create_training_zip(TRAINING_IMAGES_FOLDER)
        
        # Step 2: Start training
        print("\nStep 2: Starting training on Replicate")
        print("-" * 60)
        training = start_training(zip_file)
        
        print("\n" + "=" * 60)
        print("📝 NEXT STEPS:")
        print("=" * 60)
        print("1. Wait for training to complete (10-30 minutes)")
        print("2. Check your email for completion notification")
        print(f"3. Or check status: python {Path(__file__).name} --check {training.id}")
        print(f"4. Use your model at: https://replicate.com/{DESTINATION_MODEL}")
        print(f"\n💡 Remember to use trigger word: {TRIGGER_WORD}")
        print("\n✅ Training initiated successfully!")
        
    except FileNotFoundError as e:
        print(f"\n❌ File/Folder Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   - Check that 'training_images' folder exists")
        print("   - Verify the folder contains image files (.jpg, .png)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   - Check your REPLICATE_API_TOKEN is correct")
        print("   - Ensure you have internet connection")
        print("   - Verify replicate package: pip install replicate")
        
        import traceback
        print("\n🐛 Full error details:")
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        if len(sys.argv) > 2:
            training_id = sys.argv[2]
            check_training_status(training_id)
        else:
            print("Usage: python script.py --check <training_id>")
    else:
        main()