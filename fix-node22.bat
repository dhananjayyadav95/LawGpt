@echo off
echo 🔧 Fix for Node.js v22.13.1 Compatibility Issues
echo ===============================================

echo.
echo Your Node.js version: v22.13.1
echo Your npm version: v10.9.2
echo.
echo The issue is likely compatibility with newer Node.js versions.
echo Let's fix this step by step...

cd frontend

echo.
echo 🧹 Step 1: Complete cleanup...
if exist "node_modules" (
    echo Removing node_modules...
    rmdir /s /q node_modules
)
if exist "package-lock.json" (
    echo Removing package-lock.json...
    del package-lock.json
)
if exist "yarn.lock" (
    echo Removing yarn.lock...
    del yarn.lock
)

echo.
echo 🔧 Step 2: Configure npm for Node.js v22...
npm config set legacy-peer-deps true
npm config set fund false
npm config set audit false
npm config set registry https://registry.npmjs.org/

echo.
echo 📝 Step 3: Update package.json for Node.js v22 compatibility...

:: Create a Node.js v22 compatible package.json
echo Creating Node.js v22 compatible package.json...
(
echo {
echo   "name": "frontend",
echo   "version": "0.1.0",
echo   "private": true,
echo   "dependencies": {
echo     "react": "^18.2.0",
echo     "react-dom": "^18.2.0",
echo     "react-scripts": "5.0.1",
echo     "axios": "^1.6.0",
echo     "lucide-react": "^0.400.0"
echo   },
echo   "scripts": {
echo     "start": "react-scripts start",
echo     "build": "react-scripts build",
echo     "test": "react-scripts test",
echo     "eject": "react-scripts eject"
echo   },
echo   "eslintConfig": {
echo     "extends": [
echo       "react-app"
echo     ]
echo   },
echo   "browserslist": {
echo     "production": [
echo       ">0.2%%",
echo       "not dead",
echo       "not op_mini all"
echo     ],
echo     "development": [
echo       "last 1 chrome version",
echo       "last 1 firefox version",
echo       "last 1 safari version"
echo     ]
echo   },
echo   "overrides": {
echo     "react-scripts": {
echo       "typescript": "^4.9.5"
echo     }
echo   }
echo }
) > package-simple.json

echo.
echo 📦 Step 4: Installing with Node.js v22 compatibility...
echo This may take 2-3 minutes, please wait...

:: Try installation with the simplified package.json
npm install --package-lock-only --package-lock=false
npm install --legacy-peer-deps --no-audit --no-fund

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Standard method failed, trying alternative approach...
    
    :: Use the simplified package.json
    copy package-simple.json package.json
    npm install --legacy-peer-deps --force
    
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Installation failed with Node.js v22
        echo.
        echo 💡 Node.js v22 is very new and may have compatibility issues
        echo.
        echo 🔄 Recommended solutions:
        echo 1. Downgrade to Node.js LTS v20: https://nodejs.org/
        echo 2. Use Node Version Manager ^(nvm^) to switch versions
        echo 3. Try the backend-only version for now
        echo.
        echo 🚀 Backend-only setup:
        echo   cd backend
        echo   python -m venv venv
        echo   venv\Scripts\activate.bat
        echo   pip install -r requirements-minimal.txt
        echo   start-backend.bat
        echo   ^(Access API at http://localhost:8000/docs^)
        echo.
        pause
        @REM exit /b 1
    )
)

:: Create .env file
if not exist ".env" (
    echo.
    echo 📝 Creating .env file...
    echo REACT_APP_BACKEND_URL=http://localhost:8000 > .env
    echo WDS_SOCKET_PORT=443 >> .env
)

echo.
echo ✅ Frontend setup completed for Node.js v22!
echo.
echo 🚀 Next steps:
echo 1. Start backend: start-backend.bat
echo 2. Start frontend: start-frontend-simple.bat
echo 3. Open: http://localhost:3000
echo.
pause