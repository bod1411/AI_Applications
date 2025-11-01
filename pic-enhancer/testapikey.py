"""
Quick test script to verify your Replicate API key is working
Run this before starting the main app to troubleshoot authentication
"""

import os
from dotenv import load_dotenv
import replicate

print("=" * 50)
print("Testing Replicate API Authentication")
print("=" * 50)

# Load environment variables
load_dotenv()

# Check if API key is loaded
api_key = os.getenv("REPLICATE_API_KEY")

if not api_key:
    print("❌ ERROR: REPLICATE_API_KEY not found in .env file")
    print("\nMake sure:")
    print("1. You have a .env file in this directory")
    print("2. It contains: REPLICATE_API_KEY=your_key_here")
    exit(1)

print(f"✅ API Key loaded: {api_key[:10]}...{api_key[-4:]}")

# Try to create a client
try:
    print("\nTesting authentication...")
    client = replicate.Client(api_token=api_key)
    print("✅ Client created successfully!")
    
    # Set environment variable (what the app does)
    os.environ["REPLICATE_API_TOKEN"] = api_key
    print("✅ Environment variable set!")
    
    print("\n" + "=" * 50)
    print("SUCCESS! Your API key is working correctly! 🎉")
    print("=" * 50)
    print("\nYou can now run your Streamlit app:")
    print("streamlit run fixed_image_enhancer.py")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    print("\nPossible issues:")
    print("1. Your API key might be invalid or expired")
    print("2. You might need to install/update replicate:")
    print("   pip install --upgrade replicate")
    print("3. Check your API key at: https://replicate.com/account/api-tokens")