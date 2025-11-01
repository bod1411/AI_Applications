# 🖼️ 4K Image Enhancer

A Streamlit-powered web application that uses AI to enhance images to 4K quality.

## Features

- **4x Image Upscaling**: Enhance images to 4K resolution
- **AI-Powered Enhancement**: Uses Real-ESRGAN model for superior quality
- **Face Enhancement**: Specialized enhancement for portraits
- **Easy to Use**: Simple drag-and-drop interface
- **Multiple Methods**: AI enhancement or fast local processing
- **Download Support**: Save enhanced images instantly

## Recommended Model

**Real-ESRGAN** (via Replicate API) - This is the best option for 4K enhancement:
- Specifically designed for image super-resolution
- Produces high-quality, realistic results
- Handles various image types (photos, artwork, etc.)
- Built-in face enhancement feature
- No need for local GPU resources

**Alternative**: The app also includes a local enhancement fallback using Lanczos resampling if you don't want to use an API.

## Setup Instructions

### 1. Install Dependencies

```bash
cd pic-enhancer
pip install -r requirements.txt
```

### 2. Get API Key (Recommended)

For best results, get a free Replicate API key:

1. Visit https://replicate.com/account/api-tokens
2. Sign up for a free account
3. Copy your API token
4. Add it to the `.env` file:

```env
REPLICATE_API_KEY=your_actual_api_key_here
```

**Note**: You already have an OpenAI API key in the `.env` file, but for image enhancement, Replicate's Real-ESRGAN model is more suitable and cost-effective.

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## How to Use

1. **Upload an Image**: Click "Browse files" or drag and drop an image
2. **Choose Enhancement Method**:
   - **Real-ESRGAN (AI)**: Best quality, requires API key
   - **Local Enhancement**: Fast, works offline
3. **Click "Enhance to 4K"**: Wait for processing (30-60 seconds)
4. **Download**: Save your enhanced 4K image

## Supported Image Formats

- JPG/JPEG
- PNG
- WebP

## API Comparison

| Feature | Real-ESRGAN (Replicate) | OpenAI DALL-E |
|---------|------------------------|---------------|
| Purpose | Image Upscaling | Image Generation |
| Quality | Excellent for enhancement | Not designed for upscaling |
| Cost | ~$0.01 per image | Higher cost |
| Speed | 30-60 seconds | Faster but different use case |
| Best For | **4K Enhancement** ✅ | Creating new images |

## Cost Estimate

- **Replicate (Real-ESRGAN)**: ~$0.01 per image enhancement
- Free tier available for testing

## Troubleshooting

**No API Key**: The app will automatically fall back to local enhancement mode.

**Slow Processing**: AI enhancement takes 30-60 seconds. Use local enhancement for faster results.

**Large Files**: For best results, start with images between 500x500 and 2000x2000 pixels.

## Tech Stack

- **Streamlit**: Web framework
- **Replicate**: AI model hosting
- **Real-ESRGAN**: AI upscaling model
- **Pillow**: Image processing
- **Python-dotenv**: Environment management

## License

MIT License - Feel free to use and modify!
