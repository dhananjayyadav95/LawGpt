@echo off
echo 🎨 Starting Nepal Law Assistant Frontend...
echo =========================================

cd frontend

:: Check if .env exists
if not exist ".env" (
    echo ❌ Frontend .env file not found!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

:: Start the React development server
echo 🌐 Starting React development server...
npm start