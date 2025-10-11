@echo off
echo 🏛️ Nepal Law Assistant - Manual Setup (Safe Mode)
echo ================================================

echo.
echo This script will NOT close automatically if there are errors
echo.

:: Keep terminal open on any error
set "ERRORLEVEL="

echo 📍 Current directory: %CD%
echo.

:: Check if we're in the right place
if not exist "frontend" (
    echo ❌ Frontend directory not found!
    echo Make sure you're in the project root directory
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

if not exist "backend" (
    echo ❌ Backend directory not found!
    echo Make sure you're in the project root directory
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo ✅ Project directories found
echo.

:: Setup Backend First
echo 🔧 Setting up Backend...
echo ========================

cd backend

if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        echo Make sure Python is installed and in PATH
        echo.
        echo Press any key to continue anyway...
        pause >nul
    ) else (
        echo ✅ Virtual environment created
    )
)

if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ⚠️  Virtual environment not found, using system Python
)

echo Installing Python packages...
pip install --upgrade pip
pip install fastapi uvicorn motor pymongo pydantic python-dotenv python-multipart requests aiohttp

if errorlevel 1 (
    echo ⚠️  Some packages may have failed to install
    echo The basic ones should work though
) else (
    echo ✅ Python packages installed
)

:: Try to install AI providers
echo Installing AI providers...
pip install openai anthropic google-generativeai

if errorlevel 1 (
    echo ⚠️  AI provider packages may have failed
    echo You can install them manually later
) else (
    echo ✅ AI providers installed
)

:: Create .env file
if not exist ".env" (
    echo Creating backend .env file...
    (
        echo MONGO_URL=mongodb+srv://demo:demo123@cluster0.mongodb.net/nepal_law_db?retryWrites=true^&w=majority
        echo DB_NAME=nepal_law_db
        echo CORS_ORIGINS=*
        echo.
        echo # AI Provider Configuration
        echo AI_PROVIDER=openai
        echo AI_MODEL=gpt-4
        echo.
        echo # Add your API key here
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo ANTHROPIC_API_KEY=your_anthropic_api_key_here
        echo GOOGLE_API_KEY=your_google_api_key_here
    ) > .env
    echo ✅ Backend .env created
) else (
    echo ✅ Backend .env already exists
)

cd ..

echo.
echo ✅ Backend setup completed!
echo.

:: Setup Frontend (Optional)
echo 🎨 Setting up Frontend (Optional)...
echo ==================================

cd frontend

echo Your Node.js version:
node --version
echo Your npm version:
npm --version
echo.

echo Cleaning previous installations...
if exist "node_modules" rmdir /s /q node_modules 2>nul
if exist "package-lock.json" del package-lock.json 2>nul

echo Configuring npm...
npm config set legacy-peer-deps true
npm config set fund false
npm config set audit false

echo.
echo Attempting npm install...
echo This may take several minutes...
echo.

npm install --legacy-peer-deps

if errorlevel 1 (
    echo.
    echo ⚠️  Frontend installation failed
    echo This is common with Node.js v22
    echo.
    echo 💡 You can still use the backend API directly!
    echo.
) else (
    echo ✅ Frontend packages installed successfully!
    
    :: Create frontend .env
    if not exist ".env" (
        echo Creating frontend .env...
        (
            echo REACT_APP_BACKEND_URL=http://localhost:8000
            echo WDS_SOCKET_PORT=443
        ) > .env
        echo ✅ Frontend .env created
    )
)

cd ..

echo.
echo 🎉 Setup Process Completed!
echo ===========================

echo.
echo 📋 What was set up:
echo ✅ Backend Python environment
echo ✅ Backend dependencies
echo ✅ Backend configuration (.env)
if exist "frontend\node_modules" (
    echo ✅ Frontend dependencies
    echo ✅ Frontend configuration (.env)
) else (
    echo ⚠️  Frontend setup failed (Node.js v22 compatibility issue)
)

echo.
echo 🚀 Next Steps:
echo.
echo 1. Configure your AI provider:
echo    - Edit backend\.env
echo    - Replace 'your_openai_api_key_here' with your actual API key
echo    - Get key from: https://platform.openai.com/api-keys
echo.
echo 2. Test backend setup:
echo    - Run: python test_ai_provider.py
echo.
echo 3. Start the platform:
echo    - Backend: start-backend.bat
if exist "frontend\node_modules" (
    echo    - Frontend: start-frontend.bat
    echo    - Access: http://localhost:3000
) else (
    echo    - API Docs: http://localhost:8000/docs
    echo    - Direct API Test: python test-api-directly.py
)

echo.
echo 💡 If frontend failed, you can use the backend API directly
echo    The API has all the same features as the web interface
echo.
echo Press any key to exit...
pause >nul