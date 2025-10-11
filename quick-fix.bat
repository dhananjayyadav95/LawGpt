@echo off
echo 🔧 Quick Fix for Nepal Law Assistant
echo ===================================

echo.
echo 🎯 Fixing common issues...

:: Fix 1: Update .env for cloud MongoDB
echo 1. Setting up cloud MongoDB connection...
cd backend
if exist ".env" (
    powershell -Command "(Get-Content .env) -replace 'mongodb://localhost:27017', 'mongodb+srv://demo:demo123@cluster0.mongodb.net/nepal_law_db?retryWrites=true&w=majority' | Set-Content .env"
    echo ✅ Updated MongoDB connection to use cloud database
) else (
    echo ❌ .env file not found. Please run setup-windows.bat first
)

:: Fix 2: Test AI provider
echo.
echo 2. Testing AI provider configuration...
cd ..
python test_ai_provider.py

echo.
echo 🎉 Quick fixes applied!
echo.
echo 📋 Next steps:
echo 1. Try starting backend: start-backend.bat
echo 2. If issues persist, use: start-backend-simple.bat
echo 3. Start frontend: start-frontend.bat
echo.
pause