# 🚂 Railway Deployment Guide - Nepal Law Assistant

## 🎯 **Step-by-Step Railway Deployment**

### **Step 1: Prepare Your Repository**
✅ Your repository is already configured with:
- `backend/Procfile` - Railway startup command
- `backend/railway.toml` - Railway configuration
- `backend/nixpacks.toml` - Build configuration
- `backend/start.sh` - Startup script
- `backend/runtime.txt` - Python version
- `backend/requirements-minimal.txt` - Dependencies

### **Step 2: Deploy to Railway**

1. **Go to Railway**
   - Visit: https://railway.app/
   - Click "Start a New Project"
   - Sign up with GitHub account

2. **Connect Repository**
   - Click "Deploy from GitHub repo"
   - Select your repository: `lawGpt`
   - Choose branch: `clean-deploy` or `dev.deploy`

3. **Configure Root Directory**
   - In Railway dashboard, go to Settings
   - Set "Root Directory" to: `backend`
   - This tells Railway to look in the backend folder

4. **Add Environment Variables**
   Go to Variables tab and add:
   ```
   AI_PROVIDER=google
   AI_MODEL=gemini-2.5-flash
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   CORS_ORIGINS=*
   PORT=8000
   ```

5. **Deploy**
   - Railway will automatically detect Python
   - It will install dependencies from `requirements-minimal.txt`
   - Start the server using the Procfile command

### **Step 3: Get Your API Key**

1. **Google Gemini API (FREE)**
   - Go to: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy the key and paste in Railway environment variables

### **Step 4: Test Deployment**

Once deployed, Railway will give you a URL like:
`https://your-app-name.railway.app`

Test these endpoints:
- Health check: `https://your-app.railway.app/api/health`
- API docs: `https://your-app.railway.app/docs`

### **Step 5: Common Issues & Solutions**

#### **Issue: "Script start.sh not found"**
✅ **Fixed**: We added `start.sh` and proper configuration files

#### **Issue: "Could not determine how to build"**
✅ **Fixed**: Added `nixpacks.toml` and `runtime.txt`

#### **Issue: "Module not found"**
- Check that Root Directory is set to `backend`
- Verify `requirements-minimal.txt` is in backend folder

#### **Issue: "Port binding failed"**
- Railway automatically sets `$PORT` environment variable
- Our Procfile uses: `--port $PORT`

### **Step 6: Frontend Connection**

After backend is deployed:

1. **Copy your Railway URL**
   - Example: `https://nepal-law-backend.railway.app`

2. **Deploy Frontend to Vercel**
   - Go to: https://vercel.com/
   - Import your repository
   - Set root directory to: `frontend`
   - Add environment variable:
     ```
     REACT_APP_BACKEND_URL=https://your-railway-url.railway.app
     ```

## 🎉 **Success!**

Your Nepal Law Assistant will be live at:
- **Backend**: `https://your-app.railway.app`
- **Frontend**: `https://your-app.vercel.app`

## 💰 **Railway Free Tier**

- **$5 credit monthly** (resets each month)
- **~500 hours** of runtime
- **Perfect for prototype usage**
- **No credit card required**

## 🔧 **Monitoring**

Railway Dashboard shows:
- **Deployment logs**
- **Runtime metrics**
- **Environment variables**
- **Custom domains**

## 🚀 **Next Steps**

1. Test all features work online
2. Share your live app with users
3. Monitor usage in Railway dashboard
4. Upgrade if you need more resources

Your Nepal Law Assistant is now helping people worldwide! 🏛️⚖️