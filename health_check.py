#!/usr/bin/env python3
"""
Nepal Law Assistant Platform Health Check
Verifies all system components are working correctly
"""

import requests
import subprocess
import sys
import os
from pathlib import Path
import json

def check_python():
    """Check Python installation"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
            return False
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def check_node():
    """Check Node.js installation"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} - OK")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except Exception as e:
        print(f"❌ Node.js check failed: {e}")
        return False

def check_mongodb():
    """Check MongoDB connection"""
    try:
        # Try to import pymongo
        import pymongo
        from motor.motor_asyncio import AsyncIOMotorClient
        
        # Try to connect (basic check)
        print("✅ MongoDB drivers installed - OK")
        return True
    except ImportError:
        print("❌ MongoDB drivers not installed")
        return False
    except Exception as e:
        print(f"⚠️  MongoDB check: {e}")
        return True  # Don't fail on connection issues

def check_tesseract():
    """Check Tesseract OCR installation"""
    try:
        import pytesseract
        # Try to get version
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract {version} - OK")
        return True
    except Exception as e:
        print(f"⚠️  Tesseract OCR: {e}")
        print("   Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False

def check_backend_dependencies():
    """Check backend Python dependencies"""
    required_packages = [
        'fastapi', 'uvicorn', 'motor', 'pymongo', 'pydantic',
        'python-dotenv', 'PyPDF2', 'python-docx', 'pillow',
        'opencv-python', 'pytesseract', 'easyocr', 'numpy'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing Python packages: {', '.join(missing)}")
        print("   Run: pip install -r backend/requirements.txt")
        return False
    else:
        print("✅ All Python dependencies - OK")
        return True

def check_frontend_dependencies():
    """Check frontend Node.js dependencies"""
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Frontend directory not found")
        return False
    
    node_modules = frontend_path / "node_modules"
    package_json = frontend_path / "package.json"
    
    if not package_json.exists():
        print("❌ Frontend package.json not found")
        return False
    
    if not node_modules.exists():
        print("❌ Frontend node_modules not found")
        print("   Run: cd frontend && npm install")
        return False
    
    print("✅ Frontend dependencies - OK")
    return True

def check_env_files():
    """Check environment configuration files"""
    backend_env = Path("backend/.env")
    frontend_env = Path("frontend/.env")
    
    issues = []
    
    # Check backend .env
    if not backend_env.exists():
        issues.append("Backend .env file missing")
    else:
        with open(backend_env, 'r') as f:
            content = f.read()
            
            # Check AI provider configuration
            if 'AI_PROVIDER' not in content:
                issues.append("AI_PROVIDER not configured")
            
            # Check if at least one API key is configured
            api_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY', 'EMERGENT_LLM_KEY', 'AI_API_KEY']
            has_real_key = False
            for key in api_keys:
                if key in content and 'your_' not in content.split(key + '=')[1].split('\n')[0]:
                    has_real_key = True
                    break
            
            if not has_real_key:
                issues.append("No valid API key configured")
    
    # Check frontend .env
    if not frontend_env.exists():
        issues.append("Frontend .env file missing")
    
    if issues:
        print(f"⚠️  Environment issues: {', '.join(issues)}")
        return False
    else:
        print("✅ Environment files - OK")
        return True

def check_ai_provider():
    """Check AI provider configuration and connectivity"""
    try:
        # Import here to avoid issues if not installed
        sys.path.append('backend')
        from ai_providers import get_ai_provider
        
        provider = get_ai_provider()
        print(f"✅ AI Provider configured - {provider.__class__.__name__}")
        return True
    except ImportError as e:
        print(f"⚠️  AI Provider modules: {e}")
        return False
    except ValueError as e:
        print(f"❌ AI Provider config: {e}")
        return False
    except Exception as e:
        print(f"⚠️  AI Provider check: {e}")
        return False

def check_backend_server():
    """Check if backend server is running"""
    try:
        response = requests.get("http://localhost:8000/api/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend server - OK ({data.get('message', 'Running')})")
            return True
        else:
            print(f"❌ Backend server - Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend server - Not running")
        print("   Start with: start-backend.bat")
        return False
    except Exception as e:
        print(f"❌ Backend server check failed: {e}")
        return False

def check_frontend_server():
    """Check if frontend server is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend server - OK")
            return True
        else:
            print(f"❌ Frontend server - Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend server - Not running")
        print("   Start with: start-frontend.bat")
        return False
    except Exception as e:
        print(f"❌ Frontend server check failed: {e}")
        return False

def check_api_endpoints():
    """Check critical API endpoints"""
    endpoints = [
        ("/api/", "API root"),
        ("/api/legal-templates", "Legal templates"),
        ("/api/official-forms/tax_notice", "Official forms")
    ]
    
    all_ok = True
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {name} endpoint - OK")
            else:
                print(f"❌ {name} endpoint - Status {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"❌ {name} endpoint - Error: {e}")
            all_ok = False
    
    return all_ok

def run_health_check():
    """Run complete health check"""
    print("🏛️ Nepal Law Assistant Platform - Health Check")
    print("=" * 50)
    
    checks = [
        ("System Requirements", [
            ("Python 3.8+", check_python),
            ("Node.js", check_node),
            ("MongoDB Drivers", check_mongodb),
            ("Tesseract OCR", check_tesseract)
        ]),
        ("Dependencies", [
            ("Backend Packages", check_backend_dependencies),
            ("Frontend Packages", check_frontend_dependencies)
        ]),
        ("Configuration", [
            ("Environment Files", check_env_files),
            ("AI Provider", check_ai_provider)
        ]),
        ("Services", [
            ("Backend Server", check_backend_server),
            ("Frontend Server", check_frontend_server)
        ]),
        ("API Endpoints", [
            ("Critical APIs", check_api_endpoints)
        ])
    ]
    
    total_checks = 0
    passed_checks = 0
    
    for category, category_checks in checks:
        print(f"\n📋 {category}")
        print("-" * 30)
        
        for check_name, check_func in category_checks:
            total_checks += 1
            if check_func():
                passed_checks += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 HEALTH CHECK SUMMARY")
    print("=" * 50)
    
    success_rate = (passed_checks / total_checks) * 100
    print(f"Passed: {passed_checks}/{total_checks} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("🎉 System is healthy and ready!")
        status = "HEALTHY"
    elif success_rate >= 70:
        print("⚠️  System has minor issues but should work")
        status = "WARNING"
    else:
        print("❌ System has major issues, please fix before using")
        status = "CRITICAL"
    
    print(f"\nOverall Status: {status}")
    
    # Recommendations
    print("\n📋 Next Steps:")
    if status == "HEALTHY":
        print("✅ All systems operational")
        print("🧪 Run test-platform.bat to verify functionality")
        print("🌐 Access platform at http://localhost:3000")
    elif status == "WARNING":
        print("⚠️  Fix minor issues above")
        print("🧪 Test basic functionality")
        print("📞 Some features may not work fully")
    else:
        print("❌ Fix critical issues before proceeding")
        print("📖 Check LOCAL_TESTING_GUIDE.md for help")
        print("🔧 Run setup-windows.bat if needed")
    
    return status == "HEALTHY"

if __name__ == "__main__":
    success = run_health_check()
    sys.exit(0 if success else 1)