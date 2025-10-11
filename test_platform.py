#!/usr/bin/env python3
"""
Nepal Law Assistant Platform Testing Script
Tests all major functionalities of the platform
"""

import requests
import json
import time
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000/api"
TEST_SESSION = "test-session-" + str(int(time.time()))

def test_text_query():
    """Test basic text query functionality"""
    print("🔍 Testing text query analysis...")
    
    payload = {
        "query_text": "I received a property tax notice with penalty. What should I do?",
        "user_session": TEST_SESSION
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze-legal-problem", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Text query successful - Analysis length: {len(result['response']['response_text'])} chars")
            return True
        else:
            print(f"❌ Text query failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Text query error: {e}")
        return False

def test_problem_solver():
    """Test advanced problem solver"""
    print("🎯 Testing problem solver...")
    
    payload = {
        "problem_text": "I was terminated from my job without proper notice. The company refuses to pay my salary.",
        "document_type": "employment_letter",
        "user_session": TEST_SESSION
    }
    
    try:
        response = requests.post(f"{BASE_URL}/solve-problem", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Problem solver successful - Urgency: {result['urgency_level']}, Success rate: {result['success_probability']}%")
            print(f"   Immediate actions: {len(result['immediate_actions'])}")
            print(f"   Solution steps: {len(result['step_by_step_solution'])}")
            return True
        else:
            print(f"❌ Problem solver failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Problem solver error: {e}")
        return False

def test_legal_research():
    """Test legal research functionality"""
    print("📚 Testing legal research...")
    
    payload = {
        "query_text": "What are the legal procedures for property inheritance in Nepal according to new civil code?",
        "user_session": TEST_SESSION
    }
    
    try:
        response = requests.post(f"{BASE_URL}/legal-research", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Legal research successful - Laws found: {len(result['response']['relevant_laws'])}")
            if 'case_precedents' in result:
                print(f"   Case precedents: {len(result['case_precedents'])}")
            return True
        else:
            print(f"❌ Legal research failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Legal research error: {e}")
        return False

def test_official_forms():
    """Test official forms retrieval"""
    print("📋 Testing official forms...")
    
    try:
        response = requests.get(f"{BASE_URL}/official-forms/tax_notice")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Official forms successful - Forms found: {len(result['forms'])}")
            print(f"   Procedures: {len(result['procedures'])}")
            print(f"   Offices: {len(result['offices'])}")
            return True
        else:
            print(f"❌ Official forms failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Official forms error: {e}")
        return False

def test_case_studies():
    """Test case studies retrieval"""
    print("📖 Testing case studies...")
    
    try:
        response = requests.get(f"{BASE_URL}/case-studies/employment_letter")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Case studies successful - Cases found: {len(result['case_studies'])}")
            return True
        else:
            print(f"❌ Case studies failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Case studies error: {e}")
        return False

def test_form_search():
    """Test form search functionality"""
    print("🔎 Testing form search...")
    
    try:
        response = requests.get(f"{BASE_URL}/search-forms?query=tax")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Form search successful - Results: {result['total_found']}")
            return True
        else:
            print(f"❌ Form search failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Form search error: {e}")
        return False

def test_history():
    """Test history retrieval"""
    print("📜 Testing history retrieval...")
    
    try:
        response = requests.get(f"{BASE_URL}/legal-history/{TEST_SESSION}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ History retrieval successful - Entries: {len(result)}")
            return True
        else:
            print(f"❌ History retrieval failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ History retrieval error: {e}")
        return False

def test_api_health():
    """Test API health"""
    print("🏥 Testing API health...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API health check successful - Message: {result['message']}")
            return True
        else:
            print(f"❌ API health check failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check error: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🏛️ Nepal Law Assistant Platform - Comprehensive Testing")
    print("=" * 60)
    
    tests = [
        ("API Health", test_api_health),
        ("Text Query", test_text_query),
        ("Problem Solver", test_problem_solver),
        ("Legal Research", test_legal_research),
        ("Official Forms", test_official_forms),
        ("Case Studies", test_case_studies),
        ("Form Search", test_form_search),
        ("History", test_history)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        success = test_func()
        results.append((test_name, success))
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Platform is working correctly.")
    else:
        print(f"\n⚠️  {total-passed} test(s) failed. Check the logs above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)