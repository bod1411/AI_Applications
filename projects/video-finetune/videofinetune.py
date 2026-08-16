import replicate
import os
import zipfile
from pathlib import Path

# ============================================
# CONFIGURATION
# ============================================

REPLICATE_API_TOKEN = "r8_bdXUILyd8ZK3k0LyKeMwvQqJjuAXUdq1DoJKz"
TRAINING_VIDEOS_FOLDER = "./training_videos"
DESTINATION_MODEL = "bod1411/aman-video"
TRIGGER_WORD = "AMANVID"
TRAINING_EPOCHS = 2
BATCH_SIZE = 8
LEARNING_RATE = 0.0001

# ============================================
# SCRIPT START
# ============================================

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

print("=" * 70)
print("🎬 FOOLPROOF VIDEO TRAINING - FINAL FIX")
print("=" * 70)
print()

# Find videos
video_folder = Path(TRAINING_VIDEOS_FOLDER)
if not video_folder.exists():
    print(f"❌ Folder not found: {video_folder}")
    exit()

video_exts = ['.mp4', '.mov', '.avi', '.MP4', '.MOV', '.AVI']
videos = []
for ext in video_exts:
    videos.extend(list(video_folder.glob(f"*{ext}")))

if len(videos) == 0:
    print(f"❌ No videos found in {video_folder}")
    exit()

print(f"✅ Found {len(videos)} videos:")
total_size = 0
for v in videos:
    size = v.stat().st_size / (1024 * 1024)
    total_size += size
    print(f"   • {v.name} ({size:.2f} MB)")

print(f"\n   Total: {total_size:.2f} MB")
print()

# Create PERFECT zip structure
zip_path = Path("C:/personel/training_FINAL.zip")
zip_path.parent.mkdir(parents=True, exist_ok=True)

if zip_path.exists():
    zip_path.unlink()

print("📦 Creating PERFECT zip structure...")
print(f"   This will be a FLAT zip (no folders inside)")
print()

# Create zip with ONLY filenames (no paths!)
with zipfile.ZipFile(str(zip_path), 'w', zipfile.ZIP_DEFLATED) as zipf:
    for video in videos:
        # Read the file content
        with open(video, 'rb') as f:
            video_data = f.read()
        
        # Write ONLY with filename (NO PATH!)
        filename_only = video.name
        zipf.writestr(filename_only, video_data)
        print(f"   ✓ Added: {filename_only}")

print()
print("🔍 Verifying zip structure...")

# Verify
with zipfile.ZipFile(str(zip_path), 'r') as zipf:
    contents = zipf.namelist()
    print(f"   Files in zip: {contents}")
    
    # Check for ANY path separators
    has_paths = any(('/' in name or '\\' in name or ':' in name) for name in contents)
    
    if has_paths:
        print(f"   ❌ ERROR: Still has paths!")
        print(f"   Contents: {contents}")
        exit()
    
    print(f"   ✅ PERFECT! All files at root level")

zip_size = zip_path.stat().st_size / (1024 * 1024)
print(f"   Zip size: {zip_size:.2f} MB")
print()

if zip_size > 150:
    print(f"⚠️  WARNING: Zip is {zip_size:.2f} MB")
    print(f"   This might still be too large!")
    print(f"   Consider using only 4 videos instead of {len(videos)}")
    response = input(f"\n   Continue anyway? (y/n): ")
    if response.lower() != 'y':
        exit()

print("=" * 70)
print("🚀 UPLOADING TO REPLICATE")
print("=" * 70)
print()
print(f"Model: {DESTINATION_MODEL}")
print(f"Trigger word: {TRIGGER_WORD}")
print(f"Epochs: {TRAINING_EPOCHS}")
print()

try:
    with open(zip_path, "rb") as zip_file:
        print("⏳ Uploading... (this may take a few minutes)")
        
        training = replicate.trainings.create(
            version="zsxkib/hunyuan-video-lora:04279caf015c30a635cabc4077b5bd82c5c706262eb61797a48db139444bcca9",
            input={
                "input_videos": zip_file,
                "trigger_word": TRIGGER_WORD,
                "epochs": TRAINING_EPOCHS,
                "batch_size": BATCH_SIZE,
                "learning_rate": LEARNING_RATE,
                "lora_rank": 16,
            },
            destination=DESTINATION_MODEL
        )
    
    print()
    print("=" * 70)
    print("✅ SUCCESS! TRAINING STARTED!")
    print("=" * 70)
    print()
    print(f"Training ID: {training.id}")
    print(f"Status: {training.status}")
    print(f"Progress: https://replicate.com/p/{training.id}")
    print()
    print("⏰ Training will take 10-15 minutes")
    print("📧 You'll get an email when complete")
    print()
    print("=" * 70)
    print("🎨 AFTER TRAINING, TEST WITH:")
    print("=" * 70)
    print()
    print(f'"{TRIGGER_WORD} playing in a park, sunny day"')
    print(f'"{TRIGGER_WORD} close up portrait, smiling"')
    print(f'"{TRIGGER_WORD} running in playground"')
    print()
    print("✅ You should see Aman's face correctly!")
    print("=" * 70)
    
except Exception as e:
    print()
    print("=" * 70)
    print("❌ ERROR")
    print("=" * 70)
    print(f"Error: {e}")
    print()
    
    error_str = str(e)
    
    if "413" in error_str:
        print("💡 File too large!")
        print(f"   Your zip: {zip_size:.2f} MB")
        print(f"   Limit: ~100-150 MB")
        print()
        print("🔧 SOLUTION:")
        print(f"   Keep only 4 videos (delete 1)")
        print(f"   Or keep only 3 videos for sure success")
        
    elif "No video files" in error_str:
        print("💡 This should NOT happen with this script!")
        print("   The zip structure was verified as correct.")
        print()
        print("🔧 LAST RESORT:")
        print("   1. Check if videos are actually playable")
        print("   2. Make sure they're real MP4 files")
        print("   3. Try converting to MP4 with VLC/HandBrake")
        
    else:
        print("💡 Unexpected error")
        print("   Check internet connection")
        print("   Verify API token")
    
    import traceback
    traceback.print_exc()

print()
print("=" * 70)