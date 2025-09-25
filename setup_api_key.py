"""
Setup OpenAI API Key
This script helps you set up your OpenAI API key
"""
import os

def setup_api_key():
    """Setup OpenAI API key"""
    print("🔑 OpenAI API Key Setup")
    print("=" * 50)
    
    # Check if key is already set
    existing_key = os.getenv('OPENAI_API_KEY')
    if existing_key:
        print(f"✅ OpenAI API key already set: {existing_key[:10]}...")
        return True
    
    print("Please enter your OpenAI API key:")
    print("(You can get it from: https://platform.openai.com/api-keys)")
    print()
    
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ No API key entered")
        return False
    
    if not api_key.startswith('sk-'):
        print("⚠️  Warning: OpenAI API keys usually start with 'sk-'")
        confirm = input("Are you sure this is correct? (y/n): ").lower()
        if confirm != 'y':
            print("❌ Setup cancelled")
            return False
    
    # Create .env file
    try:
        with open('.env', 'w') as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print("✅ API key saved to .env file")
    except Exception as e:
        print(f"❌ Could not create .env file: {e}")
        return False
    
    # Set environment variable for current session
    os.environ['OPENAI_API_KEY'] = api_key
    print("✅ API key set for current session")
    
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("=" * 50)
    print("Your OpenAI API key is now configured.")
    print("You can now use AI generation features!")
    print("\nTo test it, run: python quick_ai_fix.py")
    
    return True

def test_api_key():
    """Test if the API key works"""
    print("\n🧪 Testing API Key...")
    
    try:
        from quick_ai_fix import quick_ai
        
        # Test text generation
        success, result = quick_ai.generate_text("Write a short test message")
        if success:
            print("✅ API key is working!")
            print(f"   Test result: {result['output_text'][:50]}...")
            return True
        else:
            print(f"❌ API key test failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False

if __name__ == "__main__":
    if setup_api_key():
        test_api_key()
