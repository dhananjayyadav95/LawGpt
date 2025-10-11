@echo off
echo 🏛️ Nepal Law Assistant - Step by Step Setup
echo ============================================

echo.
echo This will guide you through setting up the platform step by step
echo Press any key to continue, or Ctrl+C to exit
pause >nul

:: Step 1: Check Prerequisites
echo.
echo 📋 Step 1: Checking Prerequisites
echo ================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found
    echo Please install Python 3.8+ from https://python.org/downloads/
    echo After installation, restart this script
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python %PYTHON_VERSION%
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found
    echo Please install Node.js from https://nodejs.org/
    echo After installation, restart this script
    pause
    exit /b 1
) else (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    echo ✅ Node.js %NODE_VERSION%
)

echo.
echo ✅ Prerequisites check passed!
echo Press any key to continue to backend setup...
pause >nul

:: Step 2: Backend Setup
echo.
echo 🔧 Step 2: Backend Setup
echo =======================

cd backend

if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python packages...
pip install --upgrade pip
pip install -r requirements-minimal.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install Python packages
    echo.
    echo 💡 Try running as Administrator or check your internet connection
    pause
    exit /b 1
)

echo ✅ Python packages installed

:: Create .env file
if not exist ".env" (
    echo Creating backend .env file...
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
    echo ✅ Backend .env created
)

cd ..

echo.
echo ✅ Backend setup completed!
echo Press any key to continue to frontend setup...
pause >nul

:: Step 3: Frontend Setup
echo.
echo 🎨 Step 3: Frontend Setup
echo ========================

cd frontend

echo Checking npm configuration...
npm config set registry https://registry.npmjs.org/

echo Installing Node.js packages (this may take a few minutes)...
echo Please be patient and don't close this window...

npm install

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Standard installation failed, trying alternative method...
    npm install --legacy-peer-deps
    
    if %errorlevel% neq 0 (
        echo ❌ Frontend installation failed
        echo.
        echo 💡 Manual steps to try:
        echo 1. Open new Command Prompt as Administrator
        echo 2. Navigate to frontend folder: cd frontend
        echo 3. Run: npm cache clean --force
        echo 4. Run: npm install
        echo.
        pause
        exit /b 1
    )
)

:: Create frontend .env
if not exist ".env" (
    echo Creating frontend .env file...
    echo REACT_APP_BACKEND_URL=http://localhost:8000 > .env
    echo WDS_SOCKET_PORT=443 >> .env
    echo ✅ Frontend .env created
)

cd ..

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 IMPORTANT: Configure your AI provider
echo.
echo 1. Edit backend\.env file
echo 2. Replace 'your_openai_api_key_here' with your actual API key
echo 3. Get API key from: https://platform.openai.com/api-keys
echo.
echo 🚀 To start the platform:
echo 1. Run: start-backend.bat
echo 2. Run: start-frontend.bat (in new window)
echo 3. Open: http://localhost:3000
echo.
echo 🧪 To test: python test_ai_provider.py
echo.
pause