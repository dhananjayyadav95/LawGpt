@echo off
echo 🧪 Testing Nepal Law Assistant Platform
echo ======================================

echo.
echo This will test your setup step by step
echo.

:: Test 1: Check directories
echo 📁 Test 1: Checking project structure...
if exist "backend" (
    echo ✅ Backend directory found
) else (
    echo ❌ Backend directory missing
    goto :error
)

if exist "frontend" (
    echo ✅ Frontend directory found
) else (
    echo ❌ Frontend directory missing
    goto :error
)

:: Test 2: Check Python
echo.
echo 🐍 Test 2: Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    goto :error
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python %PYTHON_VERSION%
)

:: Test 3: Check Node.js
echo.
echo 📦 Test 3: Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found
) else (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    echo ✅ Node.js %NODE_VERSION%
)

:: Test 4: Check backend setup
echo.
echo 🔧 Test 4: Checking backend setup...
cd backend

if exist "venv" (
    echo ✅ Virtual environment exists
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  No virtual environment (using system Python)
)

python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo ❌ FastAPI not installed
) else (
    echo ✅ FastAPI available
)

python -c "import openai" 2>nul
if errorlevel 1 (
    echo ❌ OpenAI package not installed
) else (
    echo ✅ OpenAI package available
)

if exist ".env" (
    echo ✅ Backend .env file exists
) else (
    echo ❌ Backend .env file missing
)

cd ..

:: Test 5: Check frontend setup
echo.
echo 🎨 Test 5: Checking frontend setup...
cd frontend

if exist "node_modules" (
    echo ✅ Frontend dependencies installed
) else (
    echo ❌ Frontend dependencies missing
)

if exist ".env" (
    echo ✅ Frontend .env file exists
) else (
    echo ❌ Frontend .env file missing
)

cd ..

:: Test 6: Test AI provider
echo.
echo 🤖 Test 6: Testing AI provider...
python test_ai_provider.py 2>nul
if errorlevel 1 (
    echo ❌ AI provider test failed
    echo 💡 Check your API key in backend\.env
) else (
    echo ✅ AI provider working
)

echo.
echo 📊 Test Summary:
echo ===============
echo.
echo ✅ = Working    ❌ = Needs fixing    ⚠️  = Optional issue
echo.
echo 🚀 Recommended next steps:
echo.
echo If most tests passed:
echo   1. Edit backend\.env with your API key
echo   2. Run: simple-backend-start.bat
echo   3. Test: python test-api-directly.py
echo.
echo If many tests failed:
echo   1. Run: manual-setup.bat
echo   2. Follow the setup instructions
echo.
goto :end

:error
echo.
echo ❌ Critical error found!
echo Please run manual-setup.bat to fix the issues
echo.

:end
echo.
echo Press any key to exit...
pause >nul