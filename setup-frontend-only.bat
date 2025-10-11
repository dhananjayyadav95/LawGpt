@echo off
echo  Setting up Frontend Only...
echo ===============================

:: Check if we're in the right directory
if not exist "frontend" (
    echo  Frontend directory not found!
    echo Make sure you're running this from the project root directory
    pause
    exit /b 1
)

cd frontend

:: Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  Node.js not found!
    echo Please install Node.js from https://nodejs.org/
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    echo ✅ Node.js %NODE_VERSION% found
)

:: Check if npm is available
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  npm not found!
    echo Please reinstall Node.js from https://nodejs.org/
    pause
    exit /b 1
) else (
    for /f "tokens=1" %%i in ('npm --version 2^>^&1') do set NPM_VERSION=%%i
    echo ✅ npm %NPM_VERSION% found
)

:: Clean any existing node_modules and package-lock
echo.
echo  Cleaning previous installations...
if exist "node_modules" (
    echo Removing old node_modules...
    rmdir /s /q node_modules
)
if exist "package-lock.json" (
    echo Removing package-lock.json...
    del package-lock.json
)

:: Set npm to use a more reliable registry
echo.
echo  Configuring npm...
npm config set registry https://registry.npmjs.org/
npm config set fetch-retries 5
npm config set fetch-retry-mintimeout 20000
npm config set fetch-retry-maxtimeout 120000

:: Install dependencies with verbose output
echo.
echo  Installing Node.js packages...
echo This may take a few minutes, please wait...
echo.

npm install --verbose --no-optional

if %errorlevel% neq 0 (
    echo.
    echo  npm install failed!
    echo.
    echo  Trying alternative installation methods...
    echo.
    
    :: Try with --legacy-peer-deps
    echo Trying with --legacy-peer-deps...
    npm install --legacy-peer-deps --verbose
    
    if %errorlevel% neq 0 (
        echo.
        echo  Alternative installation also failed!
        echo.
        echo  Troubleshooting steps:
        echo 1. Check your internet connection
        echo 2. Try running as Administrator
        echo 3. Clear npm cache: npm cache clean --force
        echo 4. Update npm: npm install -g npm@latest
        echo.
        pause
        exit /b 1
    )
)

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo  Creating frontend .env file...
    echo REACT_APP_BACKEND_URL=http://localhost:8000 > .env
    echo WDS_SOCKET_PORT=443 >> .env
    echo  Frontend .env created
)

echo.
echo  Frontend setup completed successfully!
echo.
echo  Next steps:
echo 1. Start backend: start-backend.bat
echo 2. Start frontend: start-frontend.bat
echo 3. Open: http://localhost:3000
echo.
pause