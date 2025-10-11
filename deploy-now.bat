@echo off
echo 🏛️ Nepal Law Assistant - Quick Deploy to Free Cloud
echo.

echo 📋 What you'll need:
echo   1. GitHub account (free)
echo   2. Google account (for Gemini API - free)
echo   3. 10 minutes of your time
echo.

echo 🎯 We'll deploy to:
echo   ✅ Frontend: Vercel (free)
echo   ✅ Backend: Railway (free $5 credit)
echo   ✅ Database: MongoDB Atlas (free 512MB)
echo   ✅ AI: Google Gemini (free 60 req/min)
echo.

pause

echo.
echo 🔑 Step 1: Get Google Gemini API Key (FREE)
echo   1. Go to: https://makersuite.google.com/app/apikey
echo   2. Sign in with Google
echo   3. Click "Create API Key"
echo   4. Copy the key
echo.
set /p GEMINI_KEY="Paste your Gemini API key here: "

echo.
echo 💾 Step 2: Setup MongoDB Atlas (FREE)
echo   1. Go to: https://cloud.mongodb.com/
echo   2. Sign up for free
echo   3. Create M0 cluster (free)
echo   4. Create database user
echo   5. Get connection string
echo.
set /p MONGO_URL="Paste your MongoDB connection string: "

echo.
echo 📝 Creating production configuration...

REM Create backend production config
echo AI_PROVIDER=google > backend\.env.production
echo AI_MODEL=gemini-pro >> backend\.env.production
echo GOOGLE_API_KEY=%GEMINI_KEY% >> backend\.env.production
echo MONGO_URL=%MONGO_URL% >> backend\.env.production
echo CORS_ORIGINS=* >> backend\.env.production

REM Create Railway config
echo web: uvicorn server_working:app --host 0.0.0.0 --port $PORT > backend\Procfile

REM Create Vercel config for frontend
echo { > frontend\vercel.json
echo   "builds": [{"src": "package.json", "use": "@vercel/static-build"}], >> frontend\vercel.json
echo   "routes": [{"src": "/(.*)", "dest": "/index.html"}] >> frontend\vercel.json
echo } >> frontend\vercel.json

echo ✅ Configuration files created!
echo.

echo 🚀 Step 3: Deploy Backend to Railway
echo   1. Go to: https://railway.app/
echo   2. Sign up with GitHub
echo   3. Click "Deploy from GitHub repo"
echo   4. Select this repository
echo   5. Choose "backend" folder
echo   6. Add environment variables from backend\.env.production
echo   7. Deploy!
echo.
echo 📋 Copy these environment variables to Railway:
type backend\.env.production
echo.
pause

echo.
echo 🎨 Step 4: Deploy Frontend to Vercel
echo   1. Go to: https://vercel.com/
echo   2. Sign up with GitHub
echo   3. Import your project
echo   4. Set root directory to "frontend"
echo   5. Add environment variable: REACT_APP_BACKEND_URL=your-railway-url
echo   6. Deploy!
echo.
pause

echo.
echo 🎉 Deployment Complete!
echo.
echo 📱 Your Nepal Law Assistant is now live!
echo   Frontend: https://your-app.vercel.app
echo   Backend: https://your-app.railway.app
echo.
echo 💡 Next steps:
echo   1. Test your live application
echo   2. Share with friends for feedback
echo   3. Monitor usage in Railway/Vercel dashboards
echo   4. Upgrade if you need more resources
echo.
echo 🏛️ Welcome to the future of Nepal legal assistance!
pause