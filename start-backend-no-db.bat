@echo off
echo 🏛️ Starting Nepal Law Assistant Backend (No Database)
echo ===================================================

cd backend

:: Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ⚠️  Using system Python
)

:: Create a simple .env without MongoDB
echo Creating .env without MongoDB...
(
echo # Database Configuration ^(disabled^)
echo MONGO_URL=disabled
echo DB_NAME=disabled
echo CORS_ORIGINS=*
echo.
echo # AI Provider Configuration
echo AI_PROVIDER=openai
echo AI_MODEL=gpt-4
echo.
echo # API Keys
echo GOOGLE_API_KEY=your-google-gemini-api-key-here
) > .env

echo ✅ Configuration updated

:: Start server without database features
echo.
echo 🚀 Starting FastAPI server (API-only mode)...
echo.
echo 🌐 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🏥 Health Check: http://localhost:8000/api/
echo.
echo ℹ️  Running without database - some features limited
echo 🛑 Press Ctrl+C to stop
echo.

python -c "
import sys
sys.path.append('.')
from server_no_db import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
"

pause