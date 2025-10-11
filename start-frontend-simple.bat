@echo off
echo 🎨 Starting Nepal Law Assistant Frontend (Simple Mode)
echo ====================================================

cd frontend

:: Check if node_modules exists
if not exist "node_modules" (
    echo ❌ Node modules not installed!
    echo.
    echo 💡 Please run one of these first:
    echo   - setup-frontend-only.bat
    echo   - fix-frontend.bat
    echo   - npm install (in frontend directory)
    echo.
    pause
    exit /b 1
)

:: Check if .env exists
if not exist ".env" (
    echo Creating frontend .env file...
    echo REACT_APP_BACKEND_URL=http://localhost:8000 > .env
    echo WDS_SOCKET_PORT=443 >> .env
)

:: Start the development server
echo 🌐 Starting React development server...
echo.
echo Frontend will be available at: http://localhost:3000
echo.
echo 🛑 Press Ctrl+C to stop the server
echo.

:: Try different start methods
npm start
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  npm start failed, trying alternative...
    yarn start
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Both npm and yarn failed to start the frontend
        echo.
        echo 💡 Try these steps:
        echo 1. Delete node_modules folder
        echo 2. Run: npm install
        echo 3. Run: npm start
        echo.
        pause
    )
)