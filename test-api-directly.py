#!/usr/bin/env python3
"""
Test Nepal Law Assistant API directly without frontend
Perfect for when frontend setup fails
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_api_health():
    """Test if API is running"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data.get('message', 'OK')}")
            return True
        else:
            print(f"❌ API Health: Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API not running - start with start-backend.bat")
        return False
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False

def test_legal_analysis():
    """Test legal analysis endpoint"""
    print("\n🧪 Testing Legal Analysis...")
    
    payload = {
        "query_text": "I received a property tax notice with penalty from Kathmandu Municipality. What should I do?",
        "user_session": "test-session-123"
    }
    
    try:
        print("Sending request... (this may take 10-30 seconds)")
        response = requests.post(f"{BASE_URL}/analyze-legal-problem", json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            analysis = data.get('response', {}).get('response_text', '')
            laws = data.get('response', {}).get('relevant_laws', [])
            
            print(f"✅ Legal Analysis Success!")
            print(f"📄 Response Length: {len(analysis)} characters")
            print(f"⚖️  Laws Referenced: {len(laws)}")
            print(f"🏛️ Sample Response: {analysis[:200]}...")
            
            if laws:
                print(f"📚 Sample Laws: {laws[:3]}")
            
            return True
        else:
            print(f"❌ Legal Analysis Failed: Status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Legal Analysis Error: {e}")
        return False

def test_problem_solver():
    """Test problem solver endpoint"""
    print("\n🎯 Testing Problem Solver...")
    
    payload = {
        "problem_text": "My landlord is trying to evict me without proper notice. I have been paying rent regularly.",
        "document_type": "legal_notice",
        "user_session": "test-session-123"
    }
    
    try:
        print("Analyzing problem... (this may take 10-30 seconds)")
        response = requests.post(f"{BASE_URL}/solve-problem", json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            urgency = data.get('urgency_level', 'unknown')
            actions = data.get('immediate_actions', [])
            steps = data.get('step_by_step_solution', [])
            success_rate = data.get('success_probability', 0)
            
            print(f"✅ Problem Solver Success!")
            print(f"🚨 Urgency Level: {urgency}")
            print(f"⚡ Immediate Actions: {len(actions)}")
            print(f"📋 Solution Steps: {len(steps)}")
            print(f"📊 Success Probability: {success_rate}%")
            
            if actions:
                print(f"🎯 First Action: {actions[0]}")
            
            return True
        else:
            print(f"❌ Problem Solver Failed: Status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Problem Solver Error: {e}")
        return False

def test_legal_research():
    """Test legal research endpoint"""
    print("\n📚 Testing Legal Research...")
    
    payload = {
        "query_text": "What are the legal procedures for property inheritance in Nepal according to the new civil code?",
        "user_session": "test-session-123"
    }
    
    try:
        print("Conducting research... (this may take 15-45 seconds)")
        response = requests.post(f"{BASE_URL}/legal-research", json=payload, timeout=90)
        
        if response.status_code == 200:
            data = response.json()
            research = data.get('response', {}).get('response_text', '')
            laws = data.get('response', {}).get('relevant_laws', [])
            precedents = data.get('case_precedents', [])
            
            print(f"✅ Legal Research Success!")
            print(f"📖 Research Length: {len(research)} characters")
            print(f"⚖️  Laws Found: {len(laws)}")
            print(f"🏛️ Case Precedents: {len(precedents)}")
            print(f"📄 Sample Research: {research[:200]}...")
            
            return True
        else:
            print(f"❌ Legal Research Failed: Status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Legal Research Error: {e}")
        return False

def interactive_test():
    """Interactive testing mode"""
    print("\n🎮 Interactive Mode")
    print("=" * 30)
    
    while True:
        print("\nWhat would you like to test?")
        print("1. Ask a legal question")
        print("2. Solve a legal problem")
        print("3. Conduct legal research")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            question = input("\nEnter your legal question: ").strip()
            if question:
                payload = {"query_text": question, "user_session": "interactive-session"}
                try:
                    response = requests.post(f"{BASE_URL}/analyze-legal-problem", json=payload, timeout=60)
                    if response.status_code == 200:
                        data = response.json()
                        analysis = data.get('response', {}).get('response_text', '')
                        print(f"\n📄 Legal Analysis:\n{analysis}")
                    else:
                        print(f"❌ Error: {response.status_code}")
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        elif choice == "2":
            problem = input("\nDescribe your legal problem: ").strip()
            if problem:
                payload = {"problem_text": problem, "document_type": "general", "user_session": "interactive-session"}
                try:
                    response = requests.post(f"{BASE_URL}/solve-problem", json=payload, timeout=60)
                    if response.status_code == 200:
                        data = response.json()
                        print(f"\n🚨 Urgency: {data.get('urgency_level', 'unknown')}")
                        print(f"📊 Success Rate: {data.get('success_probability', 0)}%")
                        
                        actions = data.get('immediate_actions', [])
                        if actions:
                            print(f"\n⚡ Immediate Actions:")
                            for i, action in enumerate(actions, 1):
                                print(f"  {i}. {action}")
                        
                        steps = data.get('step_by_step_solution', [])
                        if steps:
                            print(f"\n📋 Solution Steps:")
                            for step in steps[:3]:  # Show first 3 steps
                                print(f"  • {step.get('description', 'N/A')}")
                    else:
                        print(f"❌ Error: {response.status_code}")
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        elif choice == "3":
            research_query = input("\nEnter your research query: ").strip()
            if research_query:
                payload = {"query_text": research_query, "user_session": "interactive-session"}
                try:
                    response = requests.post(f"{BASE_URL}/legal-research", json=payload, timeout=90)
                    if response.status_code == 200:
                        data = response.json()
                        research = data.get('response', {}).get('response_text', '')
                        print(f"\n📚 Legal Research:\n{research[:1000]}...")
                    else:
                        print(f"❌ Error: {response.status_code}")
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter 1-4.")

def main():
    """Main test function"""
    print("🏛️ Nepal Law Assistant - Direct API Testing")
    print("=" * 50)
    print("This tests the backend API directly without needing the frontend")
    print()
    
    # Test API health first
    if not test_api_health():
        print("\n❌ Backend is not running!")
        print("💡 Start the backend first with: start-backend.bat")
        return False
    
    print("\n🧪 Running automated tests...")
    
    tests = [
        ("Legal Analysis", test_legal_analysis),
        ("Problem Solver", test_problem_solver),
        ("Legal Research", test_legal_research)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
            time.sleep(2)  # Brief pause between tests
        except Exception as e:
            print(f"❌ {test_name}: Unexpected error - {e}")
            results.append((test_name, False))
    
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
        print("\n🎉 All tests passed! The API is working perfectly!")
        print("🌐 You can also test at: http://localhost:8000/docs")
        
        # Offer interactive mode
        choice = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_test()
    else:
        print(f"\n⚠️  {total-passed} test(s) failed. Check your AI provider configuration.")
    
    return passed == total

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")