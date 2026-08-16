# model_config.py
# Model Configuration and Management

# Additional video generation models (constantly being updated)
EXTENDED_MODELS = {
    # Latest Replicate Models (check replicate.com for newest versions)
    "Minimax Video-01": {
        "id": "minimax/video-01",
        "description": "High-quality Chinese video generation model",
        "features": ["High Quality", "Long Duration", "Chinese Support"],
        "duration": "6 seconds",
        "best_for": "Professional content, Chinese language",
        "provider": "Minimax"
    },
    "Haiper v2": {
        "id": "haiper/haiper-video-v2",
        "description": "Fast and efficient video generation",
        "features": ["Fast", "Efficient", "Good Quality"],
        "duration": "4 seconds",
        "best_for": "Quick content creation",
        "provider": "Haiper"
    },
    "Luma Dream Machine": {
        "id": "lumalabs/luma-photon-flash",
        "description": "Ultra-fast dream-like video generation",
        "features": ["Ultra Fast", "Artistic", "Creative"],
        "duration": "5 seconds",
        "best_for": "Artistic and creative videos",
        "provider": "Luma Labs"
    },
    "Runway Gen-3": {
        "id": "runwayml/gen3-alpha-turbo",
        "description": "Professional video generation with Gen-3",
        "features": ["Professional", "Consistent", "High Quality"],
        "duration": "10 seconds",
        "best_for": "Professional video production",
        "provider": "Runway"
    },
    "Pika 2.0": {
        "id": "pika/pika-2-0",
        "description": "Next-gen video creation platform",
        "features": ["Innovative", "Style Control", "Effects"],
        "duration": "3 seconds",
        "best_for": "Creative effects and transitions",
        "provider": "Pika Labs"
    },
    "Genmo Mochi 1": {
        "id": "genmo/mochi-1-preview",
        "description": "Open source video generation",
        "features": ["Open Source", "Customizable", "Fast"],
        "duration": "5 seconds",
        "best_for": "Developers and customization",
        "provider": "Genmo"
    },
    "CogVideoX-5B": {
        "id": "lucataco/cogvideox-5b",
        "description": "Open source text-to-video model",
        "features": ["Open Source", "Research", "Customizable"],
        "duration": "6 seconds",
        "best_for": "Research and experimentation",
        "provider": "Tsinghua University"
    }
}

# Character consistency best practices
CHARACTER_TEMPLATES = {
    "Person - Detailed": """
A [AGE]-year-old [GENDER] with [HAIR_COLOR] [HAIR_LENGTH] hair [HAIR_STYLE], 
[EYE_COLOR] eyes, [SKIN_TONE] skin, [BUILD] build. 
Wearing [CLOTHING_TOP] and [CLOTHING_BOTTOM]. 
Notable features: [DISTINGUISHING_FEATURES].
[ACTION], [SETTING], [LIGHTING].
Photorealistic, cinematic, 4K quality.
""",
    
    "Animated Character": """
An animated [CHARACTER_TYPE] with [DISTINCTIVE_FEATURES], 
[PRIMARY_COLOR] and [SECONDARY_COLOR] color scheme.
[ANIMATION_STYLE] style (e.g., Pixar, anime, 2D).
[ACTION], [SETTING].
High quality animation, smooth motion.
""",
    
    "Professional/Occupation": """
A [AGE]-year-old [GENDER] [OCCUPATION] with [PHYSICAL_DESCRIPTION].
Wearing [PROFESSIONAL_ATTIRE].
[WORKING_ACTION] in [WORKPLACE_SETTING].
Professional lighting, 4K, cinematic.
""",
    
    "Fantasy/Sci-Fi Character": """
A [SPECIES/TYPE] [CHARACTER] with [UNIQUE_FEATURES].
Wearing [COSTUME/ARMOR].
[MAGICAL/TECH_ELEMENTS].
[ACTION] in [FANTASY/SCIFI_SETTING].
Epic, cinematic, high fantasy/sci-fi style.
"""
}

# Prompt enhancement presets
ENHANCEMENT_PRESETS = {
    "cinematic": ", cinematic lighting, film grain, 24fps, professional camera work, shallow depth of field",
    "high_quality": ", 4K, ultra HD, highly detailed, professional quality, sharp focus",
    "artistic": ", artistic, creative composition, unique perspective, aesthetic, visually striking",
    "realistic": ", photorealistic, natural lighting, authentic, true to life, documentary style",
    "dramatic": ", dramatic lighting, intense atmosphere, high contrast, moody, powerful composition",
    "smooth": ", smooth motion, fluid animation, seamless transitions, professional editing"
}

# Aspect ratio settings
ASPECT_RATIOS = {
    "16:9": {"width": 1920, "height": 1080, "description": "Standard widescreen, best for YouTube/TV"},
    "9:16": {"width": 1080, "height": 1920, "description": "Vertical/Portrait, best for TikTok/Reels"},
    "1:1": {"width": 1080, "height": 1080, "description": "Square, best for Instagram posts"},
    "4:3": {"width": 1440, "height": 1080, "description": "Classic, best for presentations"},
    "21:9": {"width": 2560, "height": 1080, "description": "Ultra-wide cinematic"}
}

# Common video generation errors and solutions
ERROR_SOLUTIONS = {
    "authentication": {
        "message": "API Authentication Failed",
        "solutions": [
            "Check your .env file has the correct API key",
            "Verify the API key is active on Replicate",
            "Make sure there are no extra spaces in the .env file",
            "Try regenerating your API key on Replicate"
        ]
    },
    "model_not_found": {
        "message": "Model Not Available",
        "solutions": [
            "The model might be temporarily unavailable",
            "Check Replicate.com for model status",
            "Try a different model",
            "Some models are in beta and may not always be accessible"
        ]
    },
    "timeout": {
        "message": "Generation Timeout",
        "solutions": [
            "Complex prompts take longer to process",
            "Try a 'Fast' variant of the model",
            "Simplify your prompt",
            "Try again in a few minutes"
        ]
    },
    "content_policy": {
        "message": "Content Policy Violation",
        "solutions": [
            "Your prompt may contain restricted content",
            "Review Replicate's content policy",
            "Rephrase your prompt",
            "Avoid sensitive topics"
        ]
    }
}

# Usage tips by experience level
USAGE_TIPS = {
    "beginner": [
        "Start with simple, clear prompts",
        "Use the example prompts as templates",
        "Try 'Fast' models first for quicker results",
        "Save successful prompts for reuse",
        "Use the same seed for consistency"
    ],
    "intermediate": [
        "Experiment with different models for the same prompt",
        "Build a library of character descriptions",
        "Use specific camera angles and movements",
        "Combine quality tags for better results",
        "Study successful generations to understand patterns"
    ],
    "advanced": [
        "Fine-tune prompts with technical terms",
        "Use negative prompts (when supported)",
        "Experiment with seed variations",
        "Chain multiple videos for longer narratives",
        "Optimize prompts for specific model strengths"
    ]
}

# Recommended model combinations for projects
PROJECT_WORKFLOWS = {
    "character_series": {
        "description": "Creating a series with the same character",
        "recommended_model": "Google Veo 3.1",
        "workflow": [
            "1. Create detailed character description",
            "2. Generate first video with seed=42",
            "3. Save the exact prompt and seed",
            "4. Use same character description + new actions",
            "5. Always use the same seed and model"
        ]
    },
    "quick_prototyping": {
        "description": "Testing ideas quickly",
        "recommended_model": "Wan 2.5 Fast or Google Veo Fast",
        "workflow": [
            "1. Start with simple prompts",
            "2. Use fast models for iteration",
            "3. Refine successful prompts",
            "4. Switch to quality models for finals"
        ]
    },
    "professional_content": {
        "description": "High-quality final output",
        "recommended_model": "Google Veo 3.1 or Sora 2",
        "workflow": [
            "1. Test with fast models first",
            "2. Refine prompt based on tests",
            "3. Use quality models for final version",
            "4. Add cinematic enhancements"
        ]
    }
}
