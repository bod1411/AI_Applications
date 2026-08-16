# AI Professional Headshot Generator

A Streamlit application that generates professional headshots using state-of-the-art AI models from Hugging Face.

## Features

- **Multiple AI Models**: Choose from 5 top-tier headshot generation models
- **Style Selection**: Professional, Casual, Creative, or LinkedIn styles
- **Customizable**: Add specific details like clothing, accessories, or expressions
- **High Quality**: Generate 512x512 professional headshots
- **Easy Download**: Download your generated headshots instantly

## Available Models

1. **Realistic Vision V5.1** - High-quality realistic portraits with excellent detail
2. **Absolute Reality V1.8** - Photorealistic portraits with natural lighting
3. **Portrait+** - Specialized in professional portrait photography
4. **Epic Realism** - Ultra-realistic portraits with cinematic quality
5. **Deliberate V2** - Versatile model for professional headshots

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure your `.env` file contains your Hugging Face token:
```
HF_TOKEN=your_token_here
```

## Running the App

```bash
streamlit run headshot_generator.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

1. **Select Model**: Choose an AI model from the sidebar
2. **Upload Photo**: Upload a clear photo of yourself
3. **Choose Style**: Select your preferred headshot style (Professional, Casual, etc.)
4. **Add Details** (Optional): Specify additional details like "wearing glasses" or "short hair"
5. **Generate**: Click the "Generate Headshot" button
6. **Download**: Download your professional headshot

## Tips for Best Results

- Upload a clear, well-lit photo with your face clearly visible
- Choose the right style based on your intended use (LinkedIn, resume, etc.)
- Use additional descriptions to specify details like clothing or expressions
- Try different models to see which works best for your photo
- Face the camera directly for more professional results

## Requirements

- Python 3.8+
- Hugging Face account and API token
- Internet connection for model inference

## Tech Stack

- Streamlit
- Hugging Face Inference API
- Pillow (PIL)
- Python-dotenv
