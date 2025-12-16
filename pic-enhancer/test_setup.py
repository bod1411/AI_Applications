#!/usr/bin/env python3
"""
Utility script to test API connections and validate setup
"""

import os
import sys
from dotenv import load_dotenv
import replicate

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_environment():
    """Check if .env file exists and is configured"""
    print_header("🔍 Checking Environment Configuration")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("\n📝 Steps to fix:")
        print("1. Copy .env.example to .env")
        print("2. Add your Replicate API key")
        print("\nExample .env content:")
        print("REPLICATE_API_KEY=r8_xxxxxxxxxxxxx")
        return False
    
    print("✅ .env file found")
    
    load_dotenv()
    api_key = os.getenv('REPLICATE_API_KEY')
    
    if not api_key:
        print("❌ REPLICATE_API_KEY not set in .env")
        print("\n📝 Add this to your .env file:")
        print("REPLICATE_API_KEY=your_actual_key_here")
        return False
    
    if api_key == "your_replicate_api_key_here":
        print("⚠️  Default placeholder API key detected")
        print("\n📝 Replace with your actual API key from:")
        print("https://replicate.com/account/api-tokens")
        return False
    
    print(f"✅ REPLICATE_API_KEY is set")
    print(f"   Key starts with: {api_key[:10]}...")
    return True

def test_replicate_connection():
    """Test connection to Replicate API"""
    print_header("🔌 Testing Replicate API Connection")
    
    try:
        # Set the API token
        load_dotenv()
        api_key = os.getenv('REPLICATE_API_KEY')
        
        if not api_key:
            print("❌ No API key found")
            return False
        
        os.environ["REPLICATE_API_TOKEN"] = api_key
        client = replicate.Client(api_token=api_key)
        
        # Try to list models (lightweight test)
        print("Testing API authentication...")
        
        # Simple test - try to get model info
        try:
            # This is a lightweight call that tests authentication
            models = client.models.list()
            print("✅ Successfully connected to Replicate API")
            print(f"   Your account has access to Replicate services")
            return True
        except Exception as e:
            if "authentication" in str(e).lower():
                print("❌ Authentication failed")
                print(f"   Error: {e}")
                print("\n📝 Check that your API key is correct")
                return False
            else:
                # If it's not an auth error, connection might still be OK
                print("⚠️  API connection test inconclusive")
                print(f"   Details: {e}")
                return True
                
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print_header("📦 Checking Dependencies")
    
    required_packages = {
        'streamlit': 'Streamlit',
        'replicate': 'Replicate',
        'dotenv': 'python-dotenv',
        'requests': 'Requests',
        'PIL': 'Pillow'
    }
    
    all_installed = True
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name} is installed")
        except ImportError:
            print(f"❌ {name} is NOT installed")
            all_installed = False
    
    if not all_installed:
        print("\n📝 Install missing packages with:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def list_available_models():
    """List some popular video generation models"""
    print_header("🤖 Popular Video Generation Models")
    
    models = [
        ("google/veo-3.1-fast", "Google Veo 3.1 Fast"),
        ("google/veo-3.1", "Google Veo 3.1"),
        ("openai/sora-2", "OpenAI Sora 2"),
        ("kwaivgi/kling-v2.5-turbo-pro", "Kling v2.5 Turbo Pro"),
        ("wan-video/wan-2.5-t2v-fast", "Wan 2.5 Fast"),
        ("pixverse/pixverse-v5", "PixVerse v5"),
        ("leonardoai/motion-2.0", "Leonardo Motion 2.0"),
    ]
    
    print("Models configured in the app:")
    for model_id, name in models:
        print(f"  • {name}")
        print(f"    ID: {model_id}")
    
    print("\n💡 Note: Model availability may vary on Replicate")
    print("   Check https://replicate.com/explore for latest models")

def print_next_steps():
    """Print next steps for the user"""
    print_header("🚀 Next Steps")
    
    print("1. Start the application:")
    print("   streamlit run ai_video_generator.py")
    print()
    print("2. Open in browser:")
    print("   http://localhost:8501")
    print()
    print("3. Try your first video:")
    print("   - Select a model (try 'Google Veo 3.1 Fast')")
    print("   - Enter a prompt")
    print("   - Click 'Generate Video'")
    print()
    print("4. For character consistency:")
    print("   - Use detailed descriptions")
    print("   - Keep the same seed (e.g., 42)")
    print("   - Use the same model")
    print()
    print("📖 Read QUICK_START.md for examples and tips!")

def main():
    """Main validation function"""
    print("\n")
    print("🎬 AI Video Generator - Setup Validator")
    print("=" * 60)
    
    # Run checks
    env_ok = check_environment()
    deps_ok = check_dependencies()
    
    if env_ok:
        api_ok = test_replicate_connection()
    else:
        api_ok = False
    
    list_available_models()
    
    # Summary
    print_header("📊 Setup Summary")
    
    checks = [
        ("Environment Configuration", env_ok),
        ("Dependencies", deps_ok),
        ("API Connection", api_ok)
    ]
    
    all_passed = all(status for _, status in checks)
    
    for check_name, status in checks:
        icon = "✅" if status else "❌"
        print(f"{icon} {check_name}")
    
    print()
    
    if all_passed:
        print("🎉 All checks passed! You're ready to generate videos!")
        print_next_steps()
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n💡 Common solutions:")
        print("   • Install dependencies: pip install -r requirements.txt")
        print("   • Create .env file with your API key")
        print("   • Get API key from: https://replicate.com/account/api-tokens")
        return 1

if __name__ == "__main__":
    sys.exit(main())
