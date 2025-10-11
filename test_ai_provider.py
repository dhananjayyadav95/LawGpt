#!/usr/bin/env python3
"""
Test AI Provider Configuration
Quick test to verify your AI provider is working correctly
"""

import sys
import os
import asyncio
from pathlib import Path

# Add backend to path
sys.path.append('backend')

async def test_ai_provider():
    """Test the configured AI provider"""
    print("🤖 Testing AI Provider Configuration")
    print("=" * 40)
    
    try:
        from ai_providers import get_ai_provider
        
        # Get configured provider
        provider = get_ai_provider()
        print(f"✅ Provider: {provider.__class__.__name__}")
        print(f"✅ Model: {provider.model}")
        
        # Test simple query
        print("\n🧪 Testing simple query...")
        system_msg = "You are a helpful assistant."
        user_msg = "Say 'Hello from Nepal Law Assistant!' in exactly one sentence."
        
        response = await provider.generate_response(system_msg, user_msg)
        print(f"✅ Response: {response[:100]}...")
        
        # Test legal query
        print("\n⚖️ Testing legal query...")
        legal_system = """You are an expert Nepal legal assistant. Provide brief, practical legal guidance for Nepal."""
        legal_query = "What should someone do if they receive a property tax notice with penalty in Nepal?"
        
        legal_response = await provider.generate_response(legal_system, legal_query)
        print(f"✅ Legal Response Length: {len(legal_response)} characters")
        print(f"✅ Contains 'Nepal': {'Nepal' in legal_response}")
        print(f"✅ Contains legal terms: {any(term in legal_response.lower() for term in ['tax', 'penalty', 'municipality', 'payment'])}")
        
        # Test response quality
        if len(legal_response) > 100 and 'Nepal' in legal_response:
            print("✅ Response quality: Good")
        else:
            print("⚠️  Response quality: May need improvement")
        
        print("\n🎉 AI Provider is working correctly!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you've installed all requirements: pip install -r backend/requirements.txt")
        return False
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("💡 Check your backend/.env file configuration")
        print("📖 See AI_PROVIDER_GUIDE.md for setup instructions")
        return False
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        print("💡 Check your API key and internet connection")
        print("📖 See AI_PROVIDER_GUIDE.md for troubleshooting")
        return False

def check_env_config():
    """Check environment configuration"""
    print("🔧 Checking Environment Configuration")
    print("=" * 40)
    
    env_file = Path("backend/.env")
    if not env_file.exists():
        print("❌ backend/.env file not found")
        print("💡 Run setup-windows.bat to create it")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Check AI provider
    if 'AI_PROVIDER=' in content:
        provider = [line.split('=')[1].strip() for line in content.split('\n') if line.startswith('AI_PROVIDER=')][0]
        print(f"✅ AI Provider: {provider}")
    else:
        print("⚠️  AI_PROVIDER not set, will default to openai")
        provider = "openai"
    
    # Check API keys
    api_keys = {
        'openai': 'OPENAI_API_KEY',
        'anthropic': 'ANTHROPIC_API_KEY', 
        'google': 'GOOGLE_API_KEY',
        'gemini': 'GOOGLE_API_KEY',
        'emergent': 'EMERGENT_LLM_KEY'
    }
    
    key_var = api_keys.get(provider.lower(), 'AI_API_KEY')
    
    if key_var + '=' in content:
        key_line = [line for line in content.split('\n') if line.startswith(key_var + '=')][0]
        key_value = key_line.split('=')[1].strip()
        
        if key_value and 'your_' not in key_value.lower():
            print(f"✅ API Key: {key_var} configured")
            return True
        else:
            print(f"❌ API Key: {key_var} not properly configured")
            print(f"💡 Edit backend/.env and set {key_var}=your_actual_api_key")
            return False
    else:
        print(f"❌ API Key: {key_var} not found")
        print(f"💡 Add {key_var}=your_actual_api_key to backend/.env")
        return False

async def main():
    """Main test function"""
    print("🏛️ Nepal Law Assistant - AI Provider Test")
    print("=" * 50)
    
    # Check environment first
    if not check_env_config():
        print("\n❌ Environment configuration issues found")
        print("📖 See AI_PROVIDER_GUIDE.md for setup help")
        return False
    
    print("\n" + "=" * 50)
    
    # Test AI provider
    success = await test_ai_provider()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Your AI provider is ready.")
        print("🚀 You can now start the platform with start-backend.bat")
    else:
        print("❌ Tests failed. Please fix the issues above.")
        print("📖 Check AI_PROVIDER_GUIDE.md for detailed setup instructions")
    
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)