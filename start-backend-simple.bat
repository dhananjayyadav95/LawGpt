@echo off
echo 🚀 Starting Nepal Law Assistant Backend (Simple Mode)...
echo =====================================================

cd backend

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Check if .env exists
if not exist ".env" (
    echo ❌ Backend .env file not found!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

:: Start the backend server without database seeding
echo 🔧 Starting FastAPI server (without database)...
echo 🌐 Backend will be available at: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo ℹ️  Running in simple mode - some features may be limited without database
echo.
uvicorn server:app --reload --host 0.0.0.0 --port 8000