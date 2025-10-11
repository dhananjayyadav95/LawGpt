@echo off
echo 🎨 Starting Frontend with WebSocket Fix
echo ======================================

cd frontend

:: Fix the .env configuration
echo Fixing WebSocket configuration...
(
echo REACT_APP_BACKEND_URL=http://localhost:8000
echo WDS_SOCKET_PORT=0
echo FAST_REFRESH=false
echo CHOKIDAR_USEPOLLING=true
) > .env

:: Create additional config
(
echo GENERATE_SOURCEMAP=false
echo BROWSER=none
echo WDS_SOCKET_HOST=localhost
echo WDS_SOCKET_PORT=0
) > .env.local

echo ✅ Configuration updated

:: Set environment variables for this session
set WDS_SOCKET_PORT=0
set FAST_REFRESH=false
set CHOKIDAR_USEPOLLING=true

echo.
echo 🚀 Starting React development server...
echo.
echo 🌐 Frontend will be available at: http://localhost:3000
echo 🛑 Press Ctrl+C to stop
echo.

:: Try different start methods
npm start
if errorlevel 1 (
    echo.
    echo ⚠️  npm start failed, trying alternative method...
    npx react-scripts start
    if errorlevel 1 (
        echo.
        echo ❌ Both methods failed
        echo.
        echo 💡 Try these manual steps:
        echo 1. Delete node_modules: rmdir /s /q node_modules
        echo 2. Reinstall: npm install --legacy-peer-deps
        echo 3. Start: npm start
        echo.
        pause
    )
)