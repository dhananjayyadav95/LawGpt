@echo off
echo 🔧 Fixing WebSocket Configuration Issue
echo ======================================

cd frontend

echo Current .env content:
if exist ".env" (
    type .env
) else (
    echo No .env file found
)

echo.
echo Creating new .env file with correct WebSocket configuration...

(
echo REACT_APP_BACKEND_URL=http://localhost:8000
echo WDS_SOCKET_PORT=0
echo FAST_REFRESH=false
echo CHOKIDAR_USEPOLLING=true
) > .env

echo.
echo ✅ New .env file created with:
type .env

echo.
echo 🔧 Also creating .env.local for additional config...

(
echo GENERATE_SOURCEMAP=false
echo BROWSER=none
echo WDS_SOCKET_HOST=localhost
echo WDS_SOCKET_PORT=0
) > .env.local

echo.
echo ✅ Configuration files updated!
echo.
echo 🚀 Now try starting the frontend:
echo   npm start
echo.
pause