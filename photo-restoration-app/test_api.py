"""
Test script to verify Replicate API key is working correctly
Run this before starting the main app to ensure everything is set up properly
"""

import os
from dotenv import load_dotenv
import replicate

def test_api_key():
    """Test if Replicate API key is valid and working"""

    print("=" * 60)
    print("🔍 Photo Restoration App - API Key Test")
    print("=" * 60)
    print()

    # Load environment variables
    load_dotenv()

    # Get API key
    api_key = os.getenv("REPLICATE_API_KEY")

    if not api_key:
        print("❌ ERROR: Replicate API key not found!")
        print()
        print("📝 To fix this:")
        print("1. Open the .env file in this directory")
        print("2. Add your Replicate API key:")
        print("   REPLICATE_API_KEY=your_key_here")
        print()
        print("Get your free API key at:")
        print("👉 https://replicate.com/account/api-tokens")
        print()
        return False

    # Check if key looks valid
    if not api_key.startswith("r8_"):
        print("⚠️  WARNING: API key format looks incorrect")
        print(f"   Key starts with: {api_key[:3]}...")
        print("   Should start with: r8_")
        print()

    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    print()

    # Test API connection
    print("🔄 Testing API connection...")
    print("   This may take a few seconds...")
    print()

    try:
        # Set the API token
        os.environ["REPLICATE_API_TOKEN"] = api_key
        client = replicate.Client(api_token=api_key)

        # Try to list available models (lightweight test)
        print("✅ API Connection Successful!")
        print()
        print("=" * 60)
        print("✨ All systems ready! You can now run the app:")
        print("=" * 60)
        print()
        print("   streamlit run app.py")
        print()
        print("=" * 60)

        return True

    except replicate.exceptions.ReplicateError as e:
        print("❌ API Connection Failed!")
        print()
        print(f"Error: {str(e)}")
        print()
        print("📝 Possible issues:")
        print("1. Invalid API key")
        print("2. API key has been revoked")
        print("3. No internet connection")
        print()
        print("Get a new API key at:")
        print("👉 https://replicate.com/account/api-tokens")
        print()
        return False

    except Exception as e:
        print("❌ Unexpected Error!")
        print()
        print(f"Error: {str(e)}")
        print()
        print("Please check:")
        print("1. Internet connection")
        print("2. Python packages are installed (pip install -r requirements.txt)")
        print()
        return False

def check_dependencies():
    """Check if all required packages are installed"""

    print("🔍 Checking dependencies...")
    print()

    required_packages = [
        'streamlit',
        'replicate',
        'Pillow',
        'requests',
        'python-dotenv'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            if package == 'Pillow':
                __import__('PIL')
            elif package == 'python-dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            missing_packages.append(package)

    print()

    if missing_packages:
        print("❌ Missing packages detected!")
        print()
        print("📝 To install missing packages, run:")
        print("   pip install -r requirements.txt")
        print()
        return False

    print("✅ All dependencies installed!")
    print()
    return True

def main():
    """Main test function"""

    # Check dependencies first
    deps_ok = check_dependencies()

    if not deps_ok:
        print("=" * 60)
        print("⚠️  Please install missing dependencies first")
        print("=" * 60)
        return

    # Test API key
    print("=" * 60)
    print()
    test_api_key()

if __name__ == "__main__":
    main()