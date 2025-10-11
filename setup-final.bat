@echo off
echo 🏛️ Nepal Law Assistant - Final Setup
echo ====================================

echo.
echo 📋 This will set up the complete Nepal Law Assistant platform
echo.

:: Check prerequisites
echo 🔍 Checking prerequisites...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python %PYTHON_VERSION%
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js from https://nodejs.org
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    echo ✅ Node.js %NODE_VERSION%
)

echo.
echo 🔧 Setting up backend...
cd backend

:: Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install minimal requirements (works without OCR)
echo Installing core Python packages...
pip install --upgrade pip
pip install -r requirements-minimal.txt

:: Create .env file
if not exist ".env" (
    echo Creating backend .env file...
    copy .env.example .env 2>nul || (
        echo MONGO_URL=mongodb+srv://demo:demo123@cluster0.mongodb.net/nepal_law_db?retryWrites=true^&w=majority > .env
        echo DB_NAME=nepal_law_db >> .env
        echo CORS_ORIGINS=* >> .env
        echo. >> .env
        echo # AI Provider Configuration >> .env
        echo AI_PROVIDER=openai >> .env
        echo AI_MODEL=gpt-4 >> .env
        echo. >> .env
        echo # Add your API key here >> .env
        echo OPENAI_API_KEY=your_openai_api_key_here >> .env
        echo ANTHROPIC_API_KEY=your_anthropic_api_key_here >> .env
        echo GOOGLE_API_KEY=your_google_api_key_here >> .env
    )
)

cd ..

echo.
echo 🎨 Setting up frontend...
cd frontend

:: Install Node.js dependencies
echo Installing Node.js packages...
npm install

:: Create frontend .env
if not exist ".env" (
    echo Creating frontend .env file...
    echo REACT_APP_BACKEND_URL=http://localhost:8000 > .env
    echo WDS_SOCKET_PORT=443 >> .env
)

cd ..

echo.
echo ✅ Setup completed successfully!
echo.
echo 📋 IMPORTANT: Configure your AI provider
echo.
echo 1. Edit backend\.env file
echo 2. Choose AI provider (openai, anthropic, google)
echo 3. Add your API key
echo.
echo 🚀 Quick start:
echo   1. Get API key from:
echo      - OpenAI: https://platform.openai.com/api-keys
echo      - Google: https://makersuite.google.com/app/apikey
echo      - Anthropic: https://console.anthropic.com/
echo.
echo   2. Edit backend\.env:
echo      AI_PROVIDER=openai
echo      OPENAI_API_KEY=sk-your-actual-key-here
echo.
echo   3. Test configuration: python test_ai_provider.py
echo   4. Start backend: start-backend.bat
echo   5. Start frontend: start-frontend.bat
echo   6. Open: http://localhost:3000
echo.
pause