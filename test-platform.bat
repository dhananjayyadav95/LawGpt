@echo off
echo 🧪 Testing Nepal Law Assistant Platform...
echo =========================================

:: Check if backend is running
curl -s http://localhost:8000/api/ >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Backend not running! Please start backend first with start-backend.bat
    pause
    exit /b 1
)

echo ✅ Backend is running, starting tests...
echo.

:: Run Python test script
cd backend
call venv\Scripts\activate.bat
cd ..
python test_platform.py

pause