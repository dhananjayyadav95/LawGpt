@echo off
echo 🏛️ Nepal Law Assistant - Windows Setup Script
echo ================================================

echo.
echo 📋 Checking Prerequisites...

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
) else (
    echo ✅ Python found
)

:: Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js from https://nodejs.org
    pause
    exit /b 1
) else (
    echo ✅ Node.js found
)

:: Check MongoDB (optional - will use cloud if not available)
mongod --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  MongoDB not found locally. You can use cloud MongoDB or install from https://mongodb.com
) else (
    echo ✅ MongoDB found
)

echo.
echo 🔧 Setting up Backend...
cd backend

:: Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install Python dependencies
echo Installing Python packages...
echo Choose installation option:
echo 1. Minimal (OpenAI, Anthropic, Google) - Recommended
echo 2. Full (includes Emergent LLM)
choice /c 12 /m "Select option"
if %errorlevel%==1 (
    pip install -r requirements-minimal.txt
) else (
    pip install -r requirements.txt
)

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating backend .env file...
    echo MONGO_URL=mongodb://localhost:27017 > .env
    echo DB_NAME=nepal_law_db >> .env
    echo CORS_ORIGINS=http://localhost:3000 >> .env
    echo. >> .env
    echo # AI Provider Configuration >> .env
    echo # Choose one: openai, anthropic, google, emergent >> .env
    echo AI_PROVIDER=openai >> .env
    echo AI_MODEL=gpt-4 >> .env
    echo. >> .env
    echo # API Keys ^(set the one you're using^) >> .env
    echo OPENAI_API_KEY=your_openai_api_key_here >> .env
    echo ANTHROPIC_API_KEY=your_anthropic_api_key_here >> .env
    echo GOOGLE_API_KEY=your_google_api_key_here >> .env
    echo EMERGENT_LLM_KEY=your_emergent_api_key_here >> .env
    echo. >> .env
    echo # Generic API key ^(fallback^) >> .env
    echo AI_API_KEY=your_api_key_here >> .env
    echo.
    echo ⚠️  IMPORTANT: Edit backend\.env and configure your AI provider and API key
)

cd ..

echo.
echo 🎨 Setting up Frontend...
cd frontend

:: Install Node.js dependencies
echo Installing Node.js packages...
npm install

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating frontend .env file...
    echo REACT_APP_BACKEND_URL=http://localhost:8000 > .env
    echo WDS_SOCKET_PORT=443 >> .env
)

cd ..

echo.
echo 📚 Installing OCR Dependencies...
echo.
echo For OCR functionality, you need to install Tesseract:
echo 1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
echo 2. Install Tesseract OCR for Windows
echo 3. Add Tesseract to your PATH environment variable
echo.

echo ✅ Setup completed!
echo.
echo 📋 Next Steps:
echo 1. Edit backend\.env and configure your AI provider:
echo    - Set AI_PROVIDER to: openai, anthropic, google, or emergent
echo    - Add your API key for the chosen provider
echo 2. Start MongoDB (or use cloud MongoDB)
echo 3. Run: start-backend.bat
echo 4. Run: start-frontend.bat (in new terminal)
echo 5. Open: http://localhost:3000
echo.
pause