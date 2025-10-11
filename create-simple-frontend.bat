@echo off
echo 🎨 Creating Simple Frontend (No WebSocket Issues)
echo =================================================

cd frontend

echo.
echo 🧹 Cleaning previous setup...
if exist "node_modules" rmdir /s /q node_modules
if exist "package-lock.json" del package-lock.json
if exist ".env" del .env
if exist ".env.local" del .env.local

echo.
echo 📝 Creating minimal package.json...
(
echo {
echo   "name": "nepal-law-frontend",
echo   "version": "0.1.0",
echo   "private": true,
echo   "dependencies": {
echo     "react": "^18.2.0",
echo     "react-dom": "^18.2.0",
echo     "react-scripts": "5.0.1",
echo     "axios": "^1.6.0"
echo   },
echo   "scripts": {
echo     "start": "GENERATE_SOURCEMAP=false react-scripts start",
echo     "build": "GENERATE_SOURCEMAP=false react-scripts build",
echo     "test": "react-scripts test --watchAll=false",
echo     "eject": "react-scripts eject"
echo   },
echo   "eslintConfig": {
echo     "extends": ["react-app"]
echo   },
echo   "browserslist": {
echo     "production": [">0.2%%", "not dead", "not op_mini all"],
echo     "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
echo   }
echo }
) > package-simple.json

echo.
echo 📝 Creating simple .env...
(
echo REACT_APP_BACKEND_URL=http://localhost:8000
echo GENERATE_SOURCEMAP=false
echo BROWSER=none
echo WDS_SOCKET_PORT=0
echo FAST_REFRESH=false
) > .env

echo.
echo 📦 Installing minimal packages...
copy package-simple.json package.json
npm install --legacy-peer-deps

if errorlevel 1 (
    echo ❌ Installation failed
    pause
    exit /b 1
)

echo.
echo ✅ Simple frontend created successfully!
echo.
echo 🚀 Starting simple frontend...
set GENERATE_SOURCEMAP=false
set WDS_SOCKET_PORT=0
npm start

pause