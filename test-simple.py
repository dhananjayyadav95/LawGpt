#!/usr/bin/env python3
"""
Simple test script for Nepal Law Assistant
Tests core functionality without complex dependencies
"""

import sys
import os
import asyncio
import requests
import time

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get("http://localhost:8000/api/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Health: {data.get('message', 'OK')}")
            return True
        else:
            print(f"❌ Backend Health: Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running - start with start-backend.bat")
        return False
    except Exception as e:
        print(f"❌ Backend Health Error: {e}")
        return False

def test_frontend():
    """Test if frontend is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: Running")
            return True
        else:
            print(f"❌ Frontend: Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend not running - start with start-frontend.bat")
        return False
    except Exception as e:
        print(f"❌ Frontend Error: {e}")
        return False

def test_ai_provider():
    """Test AI provider configuration"""
    try:
        sys.path.append('backend')
        from ai_providers import get_ai_provider
        
        provider = get_ai_provider()
        print(f"✅ AI Provider: {provider.__class__.__name__}")
        print(f"✅ AI Model: {provider.model}")
        return True
    except Exception as e:
        print(f"❌ AI Provider: {e}")
        return False

def test_simple_api():
    """Test simple API endpoint"""
    try:
        response = requests.post(
            "http://localhost:8000/api/analyze-legal-problem",
            json={
                "query_text": "What is the process for property registration in Nepal?",
                "user_session": "test-session"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            analysis_length = len(data.get('response', {}).get('response_text', ''))
            print(f"✅ Legal Analysis API: Working ({analysis_length} chars)")
            return True
        else:
            print(f"❌ Legal Analysis API: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Legal Analysis API: {e}")
        return False

def main():
    """Run all tests"""
    print("🏛️ Nepal Law Assistant - Simple Test Suite")
    print("=" * 50)
    
    tests = [
        ("AI Provider Config", test_ai_provider),
        ("Backend Health", test_backend_health),
        ("Frontend Status", test_frontend),
        ("Legal Analysis API", test_simple_api)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name}: Unexpected error - {e}")
            results.append((test_name, False))
        
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Platform is working correctly.")
        print("🌐 Access your platform at: http://localhost:3000")
    elif passed >= total * 0.75:
        print("\n⚠️  Most tests passed. Platform should work with minor limitations.")
    else:
        print("\n❌ Multiple tests failed. Please check configuration.")
        print("📖 See setup instructions or run setup-final.bat")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        sys.exit(1)