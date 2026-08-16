import replicate
import os

# ============================================
# CONFIGURATION
# ============================================

REPLICATE_API_TOKEN = "r8_bdXUILyd8ZK3k0LyKeMwvQqJjuAXUdq1DoJKz"
DESTINATION_MODEL = "bod1411/quest-headshot"

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

print("=" * 60)
print("🔍 REPLICATE API DIAGNOSTICS")
print("=" * 60)
print()

# Test 1: Check API token
print("Test 1: Checking API token...")
try:
    # Try to list your models (this will fail if token is invalid)
    client = replicate.Client(api_token=REPLICATE_API_TOKEN)
    print("✅ API token appears valid")
except Exception as e:
    print(f"❌ API token error: {e}")
    print("\n🔧 Fix:")
    print("   1. Go to https://replicate.com/account/api-tokens")
    print("   2. Copy your API token")
    print("   3. Update it in the script")
    exit(1)

print()

# Test 2: Try to get your account info
print("Test 2: Getting account information...")
try:
    # Try to access the model
    model_owner, model_name = DESTINATION_MODEL.split("/")
    print(f"   Model owner: {model_owner}")
    print(f"   Model name: {model_name}")
    
    # Try to check if model exists
    try:
        model = replicate.models.get(DESTINATION_MODEL)
        print(f"✅ Model exists!")
        print(f"   URL: https://replicate.com/{DESTINATION_MODEL}")
        print(f"   Visibility: {model.visibility if hasattr(model, 'visibility') else 'unknown'}")
    except Exception as model_error:
        if "404" in str(model_error) or "not found" in str(model_error).lower():
            print(f"❌ Model NOT found: {DESTINATION_MODEL}")
            print(f"\n🔧 Fix:")
            print(f"   1. Go to https://replicate.com/create")
            print(f"   2. Create model with:")
            print(f"      Owner: {model_owner}")
            print(f"      Name: {model_name}")
            print(f"      Visibility: Public or Private")
            print(f"   3. Then run your training script again")
        else:
            print(f"❌ Error checking model: {model_error}")
            
except Exception as e:
    print(f"❌ Error: {e}")

print()

# Test 3: Check the trainer model exists
print("Test 3: Checking if fast-flux-trainer is accessible...")
try:
    trainer = replicate.models.get("replicate/fast-flux-trainer")
    print("✅ Trainer model is accessible")
except Exception as e:
    print(f"❌ Cannot access trainer: {e}")

print()
print("=" * 60)
print("DIAGNOSIS COMPLETE")
print("=" * 60)