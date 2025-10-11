@echo off
echo 🏛️ Nepal Law Assistant - Backend Only Setup
echo ===========================================

echo.
echo This will set up only the backend (API server)
echo You can test it directly without the frontend
echo.

cd backend

echo 🔧 Setting up Python environment...

:: Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        echo Make sure Python 3.8+ is installed
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing Python packages...
pip install --upgrade pip
pip install -r requirements-minimal.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install Python packages
    pause
    exit /b 1
)

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env configuration...
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

echo.
echo ✅ Backend setup completed!
echo.
echo 📋 IMPORTANT: Configure your AI provider
echo.
echo 1. Edit backend\.env file
echo 2. Replace 'your_openai_api_key_here' with your actual API key
echo 3. Get API key from: https://platform.openai.com/api-keys
echo.
echo 🧪 Test your configuration:
echo   python test_ai_provider.py
echo.
echo 🚀 Start the backend:
echo   start-backend.bat
echo.
echo 🌐 Access points:
echo   - API: http://localhost:8000/api/
echo   - Docs: http://localhost:8000/docs
echo   - Health: http://localhost:8000/api/
echo.
echo 📱 You can test the API directly using the documentation interface
echo    or use tools like Postman to send requests
echo.
pause