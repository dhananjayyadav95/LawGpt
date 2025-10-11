@echo off
echo Starting Nepal Law Assistant Backend (Simple)
echo ============================================

cd backend

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Using system Python
)

echo.
echo Creating simple .env file...
echo MONGO_URL=disabled > .env
echo DB_NAME=disabled >> .env
echo CORS_ORIGINS=* >> .env
echo AI_PROVIDER=google >> .env
echo AI_MODEL=gemini-pro >> .env
echo GOOGLE_API_KEY=your-google-gemini-api-key-here >> .env

echo.
echo Starting server...
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.

uvicorn server_no_db:app --reload --host 0.0.0.0 --port 8000

pause