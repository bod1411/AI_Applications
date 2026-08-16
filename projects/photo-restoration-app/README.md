# 🖼️ Photo Restoration Pro

AI-Powered Photo Repair & Enhancement Application - Restore damaged photos, colorize B&W images, and enhance quality using cutting-edge AI models.

![Photo Restoration](https://img.shields.io/badge/AI-Photo%20Restoration-blue)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)
![Replicate](https://img.shields.io/badge/Powered%20by-Replicate%20AI-green)

## ✨ Features

### 🔧 Photo Restoration Capabilities
- **Fix Physical Damage**: Repair tears, scratches, water stains, and missing pieces
- **Enhance Quality**: Sharpen blurry images, brighten dark photos, remove noise
- **Colorize B&W Photos**: Add realistic colors to black and white photographs
- **Face Restoration**: Specialized restoration for portraits and family photos
- **Upscale Images**: Enhance resolution up to 4K quality
- **Remove Artifacts**: Clean up compression artifacts and degradation

### 🤖 AI Models Included

1. **General Restoration (SwinIR)**
   - Best for: Denoising, deblurring, sharpening
   - Speed: Fast
   - Use case: Blurry or compressed images

2. **Face Restoration (GFPGAN)**
   - Best for: Portraits and family photos
   - Speed: Very Fast
   - Use case: Old photos with faces

3. **Colorize B&W Photos (DDColor)**
   - Best for: Black and white photos
   - Speed: Fast
   - Use case: Vintage photos needing colorization

4. **Complete Restoration (FLUX Kontext)**
   - Best for: Severe damage and scratches
   - Speed: Medium
   - Use case: Heavily damaged photos

5. **Advanced Upscale (Real-ESRGAN)**
   - Best for: Small or low-resolution images
   - Speed: Fast
   - Use case: Image upscaling with face enhancement

6. **Sharpness Restoration (NAFNet)**
   - Best for: Slightly blurry images
   - Speed: Fast
   - Use case: Soft or unfocused photos

### 🎯 Smart Features
- **Auto-Detection**: Automatically selects the best restoration method
- **Before/After Comparison**: Side-by-side view of original and restored photos
- **Batch Processing Ready**: Easy to extend for multiple photos
- **High-Quality Output**: PNG format with maximum quality
- **User-Friendly Interface**: Beautiful, intuitive design

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Replicate API key (get it free at [replicate.com](https://replicate.com/account/api-tokens))

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd photo-restoration-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - The `.env` file is already created with your API key
   - If needed, edit `.env` and add your Replicate API key:
     ```
     REPLICATE_API_KEY=your_api_key_here
     ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

## 📖 How to Use

### Basic Usage

1. **Upload a Photo**
   - Click "Choose a photo to restore"
   - Select JPG, PNG, or WEBP (max 100MB)

2. **Choose Restoration Method**
   - **Auto-Detect (Recommended)**: Let AI choose the best method
   - **Manual Selection**: Choose a specific restoration type

3. **Restore Photo**
   - Click "🚀 Restore Photo"
   - Wait 30-60 seconds for processing

4. **Download Result**
   - View before/after comparison
   - Click "📥 Download Restored Photo"

### Advanced Settings

Access advanced options in the sidebar:

- **Upscale Factor**: Choose 2x, 3x, or 4x enlargement
- **Quality Preset**: Balance between speed and quality
- **Manual Model Selection**: Try different AI models

## 🎨 Use Cases

### Perfect For:
- ✅ Old family photos with damage
- ✅ Faded wedding photographs
- ✅ Blurry childhood memories
- ✅ Black and white photos needing color
- ✅ Low-resolution scanned images
- ✅ Water-damaged photographs
- ✅ Scratched or torn pictures

### Restoration Examples:
- **Torn Photos**: Reconstructs missing pieces
- **Faded Colors**: Restores vibrant colors
- **Blurry Faces**: Sharpens facial features
- **Dark Photos**: Brightens underexposed images
- **Scratched Photos**: Removes scratches and marks
- **B&W Photos**: Adds realistic colorization

## 🛠️ Technical Details

### Tech Stack
- **Frontend**: Streamlit
- **AI Models**: Replicate API
- **Image Processing**: Pillow (PIL)
- **Language**: Python 3.8+

### Supported Formats
- **Input**: JPG, JPEG, PNG, WEBP
- **Output**: High-quality PNG
- **Max File Size**: 100MB (configurable in .env)

### AI Models Used
All models are hosted on Replicate:
- `jingyunliang/swinir` - General restoration
- `tencentarc/gfpgan` - Face restoration
- `piddnad/ddcolor` - Colorization
- `flux-kontext-apps/restore-image` - Complete restoration
- `nightmareai/real-esrgan` - Upscaling
- `megvii-research/nafnet` - Sharpness restoration

## ⚙️ Configuration

Edit `.env` file for custom settings:

```env
# Replicate API Key (Required)
REPLICATE_API_KEY=your_key_here

# Application Settings
MAX_FILE_SIZE_MB=100
OUTPUT_FORMAT=PNG
```

## 🐛 Troubleshooting

### Common Issues

**1. API Key Error**
```
❌ Replicate API Key not found!
```
**Solution**: Add your API key to the `.env` file

**2. GPU Memory Error**
```
🚨 GPU Memory Error Detected!
```
**Solutions**:
- Reduce upscale factor to 2x
- Try a different model
- Resize image before uploading

**3. Slow Processing**
```
Taking longer than 60 seconds
```
**Solutions**:
- Large images take longer to process
- Try "Fast Processing" quality preset
- Check your internet connection

**4. Import Errors**
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

## 📊 Performance Tips

- **Small Images (<2MP)**: All models work well, try 4x upscale
- **Medium Images (2-5MP)**: Use 2x-3x upscale for best results
- **Large Images (>5MP)**: Stick to 2x upscale or use Fast preset
- **B&W Photos**: Auto-detect will automatically choose colorization
- **Portraits**: Auto-detect will prioritize face restoration

## 🔒 Privacy & Security

- All processing happens on Replicate's secure servers
- Images are not stored permanently
- API communication is encrypted
- Your photos are only used for restoration processing

## 📝 Future Enhancements

Planned features:
- [ ] Batch processing for multiple photos
- [ ] Custom restoration presets
- [ ] Photo animation (like BringBack.pro)
- [ ] Add custom frames and captions
- [ ] Historical restoration styles
- [ ] Video frame restoration
- [ ] Integration with more AI models

## 🤝 Contributing

Feel free to fork this project and add your own improvements!

Suggestions for contributions:
- Add new AI models from Replicate
- Improve auto-detection algorithm
- Add more quality presets
- Create batch processing feature
- Improve UI/UX design

## 📄 License

This project is open source and available for personal and educational use.

## 🙏 Acknowledgments

- **Replicate AI** for providing access to state-of-the-art models
- **Streamlit** for the amazing web framework
- **AI Model Creators**: SwinIR, GFPGAN, DDColor, FLUX, Real-ESRGAN, NAFNet

## 📞 Support

If you encounter any issues:
1. Check the Troubleshooting section above
2. Ensure your API key is valid
3. Verify your internet connection
4. Try a different restoration model

## 🌟 Credits

Built with ❤️ using Streamlit and Replicate AI

Inspired by [BringBack.pro](https://bringback.pro/) and similar photo restoration services.

---

**Enjoy restoring your precious memories! 📸✨**