@echo off
echo 🔧 Fixing Frontend Installation Issues
echo =====================================

cd frontend

echo.
echo 🧹 Cleaning npm cache and previous installations...
npm cache clean --force
if exist "node_modules" rmdir /s /q node_modules
if exist "package-lock.json" del package-lock.json

echo.
echo 🔧 Configuring npm for better reliability...
npm config set registry https://registry.npmjs.org/
npm config set fetch-retries 5
npm config set fetch-retry-mintimeout 20000
npm config set fetch-retry-maxtimeout 120000

echo.
echo 📦 Installing packages with alternative method...
npm install --legacy-peer-deps --verbose

if %errorlevel% neq 0 (
    echo.
    echo ❌ Installation still failing. Trying yarn instead...
    
    :: Check if yarn is available
    yarn --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Installing yarn...
        npm install -g yarn
    )
    
    echo Using yarn to install packages...
    yarn install
    
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Both npm and yarn failed
        echo.
        echo 💡 Manual troubleshooting steps:
        echo 1. Run Command Prompt as Administrator
        echo 2. Update Node.js to latest version
        echo 3. Update npm: npm install -g npm@latest
        echo 4. Try again: npm install --force
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ✅ Frontend packages installed successfully!
echo.
pause