#!/usr/bin/env python3
"""
Test the working version of Nepal Law Assistant
"""

import requests
import json
import time

def test_working_backend():
    """Test the working backend"""
    print("🧪 Testing WORKING Nepal Law Assistant Backend")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data.get('status', 'unknown')}")
            print(f"✅ AI Available: {data.get('ai_available', False)}")
            print(f"✅ OpenAI Configured: {data.get('openai_configured', 'unknown')}")
            print(f"📋 Full Response: {data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: API root
    print("\n2. Testing API root...")
    try:
        response = requests.get(f"{base_url}/api/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Root: {data['message']}")
        else:
            print(f"❌ API root failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API root error: {e}")
    
    # Test 3: Legal analysis (the main feature)
    print("\n3. Testing legal analysis...")
    try:
        payload = {
            "query_text": "I received a property tax notice with penalty from Kathmandu Municipality. What should I do?",
            "user_session": "test-session"
        }
        
        print("Sending legal analysis request...")
        response = requests.post(f"{base_url}/api/analyze-legal-problem", json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            analysis = data.get('response', {}).get('response_text', '')
            laws = data.get('response', {}).get('relevant_laws', [])
            
            print(f"✅ Legal Analysis SUCCESS!")
            print(f"📄 Response Length: {len(analysis)} characters")
            print(f"⚖️  Laws Referenced: {len(laws)}")
            print(f"🏛️ Sample Response: {analysis[:200]}...")
            
            if len(analysis) > 100:
                print("✅ Response quality: GOOD")
                return True
            else:
                print("⚠️  Response quality: Short")
                return False
        else:
            print(f"❌ Legal analysis failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Legal analysis error: {e}")
        return False

def main():
    """Main test function"""
    print("🏛️ Nepal Law Assistant - WORKING VERSION TEST")
    print("=" * 60)
    
    success = test_working_backend()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED! The working version is functioning correctly!")
        print("🌐 Your Nepal Law Assistant is ready at: http://localhost:3000")
        print("📚 API Documentation: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Check the backend logs for details.")
    
    return success

if __name__ == "__main__":
    main()