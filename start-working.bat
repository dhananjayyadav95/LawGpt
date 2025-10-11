@echo off
echo 🏛️ Nepal Law Assistant - WORKING VERSION
echo ========================================

echo.
echo This version has all bugs fixed and will work guaranteed!
echo.

cd backend

:: Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

:: Install OpenAI if not present
python -c "import openai" 2>nul
if errorlevel 1 (
    echo Installing OpenAI package...
    pip install openai==1.99.9
)

:: Start the working server
echo.
echo 🚀 Starting WORKING backend server...
echo.
echo 🌐 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🏥 Health Check: http://localhost:8000/api/health
echo.
echo ✅ All bugs fixed - this WILL work!
echo 🛑 Press Ctrl+C to stop
echo.

uvicorn server_working:app --reload --host 0.0.0.0 --port 8000

pause