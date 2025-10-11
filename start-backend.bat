@echo off
echo 🏛️ Starting Nepal Law Assistant Backend...
echo ==========================================

cd backend

:: Check if backend directory exists
if not exist "server.py" (
    echo ❌ Backend files not found! Make sure you're in the right directory.
    pause
    exit /b 1
)

:: Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ⚠️  Virtual environment not found, using system Python
)

:: Check if .env exists
if not exist ".env" (
    echo ❌ Backend .env file not found!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

:: Test AI provider configuration
echo 🤖 Testing AI provider...
python -c "
try:
    from ai_providers import get_ai_provider
    provider = get_ai_provider()
    print(f'✅ AI Provider: {provider.__class__.__name__} with model: {provider.model}')
except Exception as e:
    print(f'❌ AI Provider error: {e}')
    print('💡 Check your API key in .env file')
"

:: Seed database with case studies (optional)
echo.
echo 📚 Seeding case studies database...
python seed_case_studies.py

:: Start the backend server
echo.
echo 🔧 Starting FastAPI server...
echo 🌐 Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🏥 Health: http://localhost:8000/api/
echo.
echo 🛑 Press Ctrl+C to stop the server
echo.
uvicorn server:app --reload --host 0.0.0.0 --port 8000