@echo off
echo 🏛️ Starting Nepal Law Assistant Backend (Simple)
echo ===============================================

:: Navigate to backend directory
if not exist "backend" (
    echo ❌ Backend directory not found!
    echo Make sure you're in the project root directory
    echo.
    pause
    exit /b 1
)

cd backend

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python from https://python.org
    echo.
    pause
    exit /b 1
)

:: Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Using system Python (no virtual environment found)
)

:: Check if required packages are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    pip install fastapi uvicorn motor pymongo pydantic python-dotenv openai
)

:: Check if .env exists
if not exist ".env" (
    echo Creating basic .env file...
    (
        echo MONGO_URL=mongodb+srv://demo:demo123@cluster0.mongodb.net/nepal_law_db?retryWrites=true^&w=majority
        echo DB_NAME=nepal_law_db
        echo CORS_ORIGINS=*
        echo AI_PROVIDER=openai
        echo AI_MODEL=gpt-4
        echo OPENAI_API_KEY=your_openai_api_key_here
    ) > .env
    echo.
    echo ⚠️  IMPORTANT: Edit .env file and add your OpenAI API key!
    echo.
)

:: Start the server
echo 🚀 Starting FastAPI server...
echo.
echo 🌐 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🏥 Health Check: http://localhost:8000/api/
echo.
echo 🛑 Press Ctrl+C to stop
echo.

uvicorn server:app --reload --host 0.0.0.0 --port 8000

echo.
echo Server stopped.
pause