# 🤖 AI Models Guide - Choose the Right Model

This guide helps you understand which AI model to use for different types of photo restoration needs.

## 📊 Quick Comparison Table

| Model | Best For | Speed | Quality | Use Case |
|-------|----------|-------|---------|----------|
| **SwinIR** | General restoration | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ High | Blurry, compressed images |
| **GFPGAN** | Face restoration | ⚡⚡⚡ Very Fast | ⭐⭐⭐⭐⭐ Excellent | Portraits, family photos |
| **DDColor** | Colorization | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ High | B&W photos |
| **FLUX Kontext** | Complete restoration | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ Excellent | Severely damaged photos |
| **Real-ESRGAN** | Upscaling | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ High | Small/low-res images |
| **NAFNet** | Sharpness | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ High | Soft/unfocused images |

---

## 🎯 Model Details

### 1. General Restoration (SwinIR)

**Model**: `jingyunliang/swinir`

**When to Use**:
- 📸 Blurry or out-of-focus photos
- 🗜️ Images with compression artifacts
- 🔊 Photos with digital noise
- 📉 Low-quality scanned images
- 🌫️ Soft or hazy pictures

**Strengths**:
- ✅ Fast processing (30-45 seconds)
- ✅ Excellent at denoising
- ✅ Great for general image enhancement
- ✅ Handles multiple quality issues at once
- ✅ Good balance of speed and quality

**Example Use Cases**:
- Old scanned photos with scan lines
- Digital photos taken with low-quality cameras
- Screenshots that need sharpening
- JPEG images with compression artifacts
- Web images that were heavily compressed

**Settings**:
- Upscale Factor: 4x (default)
- Task: Real-world super-resolution
- Noise Level: 15 (adjustable)

---

### 2. Face Restoration (GFPGAN)

**Model**: `tencentarc/gfpgan`

**When to Use**:
- 👤 Old family portraits
- 👨‍👩‍👧‍👦 Group photos with people
- 📷 Vintage passport/ID photos
- 👰 Wedding photographs
- 🎓 School photos
- 👴 Ancestral photos

**Strengths**:
- ✅ **FASTEST** model (20-30 seconds)
- ✅ Specialized for facial features
- ✅ Reconstructs realistic faces even from heavily degraded photos
- ✅ Maintains facial identity
- ✅ Excellent for portraits

**Example Use Cases**:
- Grandparent's old wedding photos
- Faded family reunion pictures
- Damaged passport photos
- Blurry selfies
- Old driver's license photos
- Historical portrait photographs

**Settings**:
- Version: v1.4 (latest)
- Scale: 2x (default)
- Best for: Close-up faces and portraits

**Important Note**:
- Works best when faces are visible in the photo
- May not improve non-facial areas as much
- Perfect for family photo restoration projects

---

### 3. Colorize B&W Photos (DDColor)

**Model**: `piddnad/ddcolor`

**When to Use**:
- 🎞️ Black and white photographs
- 📰 Historical photos
- 🏛️ Vintage family pictures
- 🎨 Sepia-toned images
- 🌓 Grayscale photos that need color

**Strengths**:
- ✅ Fast colorization (30-40 seconds)
- ✅ Vibrant, realistic colors
- ✅ Better than older colorization models
- ✅ Understands context (sky = blue, grass = green)
- ✅ Natural skin tones

**Example Use Cases**:
- 1920s-1960s family photos
- Historical war photographs
- Vintage city/landscape photos
- Old newspaper images
- Black and white wedding photos
- Ancestral photographs

**Settings**:
- Model Size: Large (best quality)
- Automatic color palette detection
- Natural tone preservation

**Tips**:
- Works best with clear B&W photos
- May need manual touch-up for unusual colors
- Can be combined with other models (colorize first, then upscale)

---

### 4. Complete Restoration (FLUX Kontext)

**Model**: `flux-kontext-apps/restore-image`

**When to Use**:
- 💔 Torn or ripped photos
- 🗑️ Photos with missing pieces
- 🔨 Severely scratched images
- 💧 Water-damaged photographs
- 🔥 Fire-damaged pictures
- 📝 Photos with writing/marks on them

**Strengths**:
- ✅ Most **COMPREHENSIVE** restoration
- ✅ Handles multiple damage types simultaneously
- ✅ Can fill in missing areas
- ✅ Removes scratches and marks
- ✅ Best for challenging restorations

**Example Use Cases**:
- Photos torn in half
- Pictures with large scratches
- Water-stained photographs
- Photos with pieces missing
- Documents with coffee stains
- Heavily damaged vintage photos

**Settings**:
- Prompt-based restoration
- Automatic damage detection
- High-quality reconstruction

**Processing Time**:
- 45-90 seconds (depends on damage level)
- Worth the wait for severely damaged photos

**Important Note**:
- Best for photos where other models fail
- May take longer but produces excellent results
- Can handle photos that seem "beyond repair"

---

### 5. Advanced Upscale (Real-ESRGAN)

**Model**: `nightmareai/real-esrgan`

**When to Use**:
- 📱 Small smartphone photos
- 🖼️ Low-resolution images
- 📧 Email-sized pictures
- 🌐 Web images that need printing
- 📸 Photos from old digital cameras
- 🔍 Images that need enlargement

**Strengths**:
- ✅ Excellent upscaling quality
- ✅ Face enhancement included
- ✅ Can upscale 2x, 3x, or 4x
- ✅ Preserves details while enlarging
- ✅ Fast processing

**Example Use Cases**:
- Small profile pictures for printing
- Thumbnails that need to be poster-sized
- Low-res product photos
- Old digital camera photos (1-2MP)
- Social media images for printing
- Screenshots that need higher resolution

**Settings**:
- Scale: 2x, 3x, or 4x (choose based on needs)
- Face Enhance: Enabled (default)
- Quality: Maximum

**Upscale Guide**:
- **2x**: Most reliable, works with larger images
- **3x**: Good balance of size and quality
- **4x**: Maximum enlargement, may fail on large files

---

### 6. Sharpness Restoration (NAFNet)

**Model**: `megvii-research/nafnet`

**When to Use**:
- 🌫️ Slightly unfocused photos
- 📷 Motion blur (camera shake)
- 🎯 Photos that need sharpening
- 📸 Images with soft focus
- 🎨 Photos that lack definition

**Strengths**:
- ✅ Fast processing
- ✅ Doesn't over-sharpen (natural look)
- ✅ Preserves image structure
- ✅ Good for subtle improvements
- ✅ Maintains realistic appearance

**Example Use Cases**:
- Photos with slight camera shake
- Slightly out-of-focus shots
- Images that look "soft"
- Photos that need crispness
- Action shots with minor blur

**Settings**:
- Automatic sharpness detection
- Structure preservation
- Natural enhancement

**Best For**:
- Photos that are "almost perfect" but need a boost
- Images where aggressive restoration isn't needed

---

## 🎓 Decision Tree: Which Model to Choose?

### Start Here: What's wrong with your photo?

```
Is your photo BLACK & WHITE?
├─ YES → Use DDColor (Colorization)
└─ NO  → Continue below

Does your photo have FACES prominently?
├─ YES → Use GFPGAN (Face Restoration)
└─ NO  → Continue below

Is your photo SEVERELY DAMAGED (tears, missing pieces)?
├─ YES → Use FLUX Kontext (Complete Restoration)
└─ NO  → Continue below

Is your photo VERY SMALL or LOW RESOLUTION?
├─ YES → Use Real-ESRGAN (Upscaling)
└─ NO  → Continue below

Is your photo BLURRY or COMPRESSED?
├─ YES → Use SwinIR (General Restoration)
└─ NO  → Use NAFNet (Sharpness)
```

---

## 💡 Pro Tips

### Combining Models
For best results, you can run photos through multiple models:

1. **B&W Old Photo**:
   - First: DDColor (add color)
   - Then: GFPGAN (if has faces) or Real-ESRGAN (upscale)

2. **Small Damaged Photo with Faces**:
   - First: FLUX Kontext (fix damage)
   - Then: GFPGAN (restore faces)
   - Finally: Real-ESRGAN (enlarge)

3. **Blurry Low-Res Photo**:
   - First: SwinIR (sharpen and denoise)
   - Then: Real-ESRGAN (upscale)

### Auto-Detect Feature
The app includes **Auto-Detect** which:
- ✅ Analyzes your photo automatically
- ✅ Chooses the best model for your needs
- ✅ Recommended for beginners
- ✅ Saves time and guesswork

### When to Use Manual Selection
Choose manual model selection when:
- You know exactly what's wrong with the photo
- Auto-detect didn't give the result you wanted
- You want to try different models to compare
- You're working with a specific type of damage

---

## 📈 Performance Comparison

### Processing Speed
| Model | Typical Time | Large Image Time |
|-------|--------------|------------------|
| GFPGAN | 20-30s | 30-45s |
| SwinIR | 30-45s | 45-60s |
| DDColor | 30-40s | 40-55s |
| Real-ESRGAN | 30-50s | 50-75s |
| NAFNet | 25-40s | 40-60s |
| FLUX Kontext | 45-90s | 60-120s |

### Quality Ratings (User Feedback)
- **GFPGAN**: ⭐⭐⭐⭐⭐ (5/5) - Best for faces
- **FLUX Kontext**: ⭐⭐⭐⭐⭐ (5/5) - Best for damage
- **SwinIR**: ⭐⭐⭐⭐ (4/5) - Excellent all-rounder
- **Real-ESRGAN**: ⭐⭐⭐⭐ (4/5) - Great upscaling
- **DDColor**: ⭐⭐⭐⭐ (4/5) - Natural colors
- **NAFNet**: ⭐⭐⭐⭐ (4/5) - Natural sharpening

---

## 🔧 Troubleshooting Model Issues

### Model Takes Too Long
- **Solution**: Try a faster model (GFPGAN or NAFNet)
- Reduce upscale factor to 2x
- Check internet connection

### Result Not Good Enough
- **Solution**: Try a different model
- Combine multiple models
- Adjust upscale factor

### GPU Memory Error
- **Solution**: Reduce upscale factor
- Resize image before uploading
- Wait a moment and try again

### Model Unavailable Error
- **Solution**: Replicate might be updating
- Try a different model temporarily
- Check API key is valid

---

## 🎯 Summary: Quick Reference

**Need it FAST?** → GFPGAN or NAFNet
**Best QUALITY?** → FLUX Kontext or GFPGAN
**Has FACES?** → GFPGAN
**BLACK & WHITE?** → DDColor
**Severely DAMAGED?** → FLUX Kontext
**TOO SMALL?** → Real-ESRGAN
**BLURRY?** → SwinIR or NAFNet
**NOT SURE?** → Use Auto-Detect ✨

---

**Happy Restoring! 📸✨**