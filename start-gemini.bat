@echo off
echo 🏛️ Nepal Law Assistant - Google Gemini Version
echo =============================================

echo.
echo Using Google Gemini API (Free tier available!)
echo.

cd backend

:: Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ❌ Virtual environment not found!
    pause
    exit /b 1
)

:: Install Google Generative AI if not present
python -c "import google.generativeai" 2>nul
if errorlevel 1 (
    echo Installing Google Generative AI package...
    pip install google-generativeai
)

:: Start the Gemini-powered server
echo.
echo 🚀 Starting backend with Google Gemini...
echo.
echo 🌐 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🏥 Health Check: http://localhost:8000/api/health
echo.
echo 💡 Make sure to add your Google API key to server_working.py
echo    Get free key from: https://makersuite.google.com/app/apikey
echo.
echo 🛑 Press Ctrl+C to stop
echo.

uvicorn server_working:app --reload --host 0.0.0.0 --port 8000

pause