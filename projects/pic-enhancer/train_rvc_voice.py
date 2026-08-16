"""
RVC Voice Model Training - Replicate API - FINAL WORKING VERSION
"""

import os
import time
from dotenv import load_dotenv
import replicate

# Load environment
load_dotenv()
api_token = os.getenv("REPLICATE_API_KEY")

if not api_token:
    raise RuntimeError("REPLICATE_API_KEY not found in .env file")

# Configuration
DATASET_FILE = "my_voice_dataset.zip"
DESTINATION_MODEL = "bod1411/my-rvc-voice"
# Full reference with owner/name:version format
TRAINING_MODEL_REF = "replicate/train-rvc-model:cf360587a27f67500c30fc31de1e0f0f9aa26dcd7b866e6ac937a07bd104bad9"

print("=" * 70)
print("RVC Voice Model Training - Replicate API")
print("=" * 70)

# Verify dataset exists
if not os.path.exists(DATASET_FILE):
    raise FileNotFoundError(f"Dataset file not found: {DATASET_FILE}")

file_size_mb = os.path.getsize(DATASET_FILE) / (1024 * 1024)
print(f"\n✓ Dataset file: {DATASET_FILE}")
print(f"✓ File size: {file_size_mb:.1f} MB")
print(f"✓ Destination model: {DESTINATION_MODEL}")

# Initialize client
print(f"\nInitializing Replicate client...")
client = replicate.Client(api_token=api_token)

# Read dataset as bytes
print(f"\nReading dataset into memory...")
with open(DATASET_FILE, "rb") as f:
    dataset_bytes = f.read()

print(f"✓ Dataset loaded: {len(dataset_bytes)} bytes")

# Submit training job
print(f"\n{'=' * 70}")
print("Submitting training job to Replicate...")
print(f"{'=' * 70}\n")

try:
    # Use the full model reference in the model parameter
    training = client.trainings.create(
        destination=DESTINATION_MODEL,
        model=TRAINING_MODEL_REF,  # Full reference: owner/name:version
        input={
            "dataset_zip": dataset_bytes,
            "sample_rate": "48k",
            "version": "v2",
            "f0method": "rmvpe_gpu",
            "epoch": 80,
            "batch_size": 7
        }
    )
    
    print(f"✅ Training job submitted successfully!")
    print(f"   Training ID: {training.id}")
    print(f"   Current Status: {training.status}")
    print(f"\n📊 View progress at:")
    print(f"   https://replicate.com/p/{training.id}")
    
except Exception as e:
    print(f"\n❌ Error submitting training: {e}")
    import traceback
    traceback.print_exc()
    raise

# Poll for completion
print(f"\n{'=' * 70}")
print("Monitoring training progress...")
print(f"{'=' * 70}\n")

start_time = time.time()
poll_count = 0

try:
    while training.status not in ["succeeded", "failed", "canceled"]:
        time.sleep(15)
        poll_count += 1
        
        training = client.trainings.get(training.id)
        elapsed = time.time() - start_time
        
        status_symbol = "⏳" if training.status == "processing" else "✓"
        print(f"[{poll_count:2d}] {status_symbol} Status: {training.status:12s} | Elapsed: {elapsed/60:5.1f} min")
    
    elapsed = time.time() - start_time
    
    print(f"\n{'=' * 70}")
    print(f"✅ TRAINING COMPLETE!")
    print(f"{'=' * 70}")
    print(f"\nFinal Status: {training.status}")
    print(f"Total Time: {elapsed/60:.1f} minutes")
    
    if training.status == "succeeded":
        print(f"\n✓ Model trained successfully!")
        print(f"\nTrained Model Output URL:")
        print(f"{training.output}")
        
        print(f"\n{'=' * 70}")
        print("✨ NEXT STEPS: Use trained model for voice cloning")
        print(f"{'=' * 70}")
        print(f"\n1. Go to: https://replicate.com/zsxkib/realistic-voice-cloning")
        print(f"\n2. Fill in the parameters:")
        print(f"   - rvc_model: CUSTOM")
        print(f"   - custom_rvc_model_download_url: {training.output}")
        print(f"   - input_audio: [upload your audio file]")
        print(f"\n3. Click 'Run' to clone your voice!")
        
    elif training.status == "failed":
        print(f"\n❌ Training failed!")
        if hasattr(training, 'error'):
            print(f"Error: {training.error}")
        
    else:
        print(f"\n⚠️  Training was {training.status}")

except KeyboardInterrupt:
    print(f"\n\n⚠️  Training interrupted by user")
    print(f"Training is still running on Replicate at:")
    print(f"https://replicate.com/p/{training.id}")
    
except Exception as e:
    print(f"\n❌ Error during monitoring: {e}")
    import traceback
    traceback.print_exc()
