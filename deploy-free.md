# 🌐 Free Deployment Guide - Nepal Law Assistant

Deploy your Nepal Law Assistant platform completely FREE using modern cloud services.

## 🎯 **Recommended Stack (100% Free)**

- **Frontend**: Vercel (Free tier - 100GB bandwidth)
- **Backend**: Railway (Free tier - $5 credit monthly)
- **Database**: MongoDB Atlas (Free tier - 512MB)
- **AI**: Google Gemini (Free tier - 60 requests/minute)
- **Domain**: Free subdomain included

## 🚀 **Step-by-Step Deployment**

### **Phase 1: Prepare for Deployment**

#### 1. Create Production Environment Files
```bash
# Create production backend .env
echo MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/nepal_law_prod > backend/.env.production
echo AI_PROVIDER=google >> backend/.env.production
echo AI_MODEL=gemini-pro >> backend/.env.production
echo GOOGLE_API_KEY=your_google_api_key >> backend/.env.production
echo CORS_ORIGINS=https://your-frontend-domain.vercel.app >> backend/.env.production

# Create production frontend .env
echo REACT_APP_BACKEND_URL=https://your-backend-domain.railway.app > frontend/.env.production
```

#### 2. Create Deployment Configuration Files
```bash
# Railway deployment config
echo web: uvicorn server_working:app --host 0.0.0.0 --port $PORT > backend/Procfile

# Vercel deployment config
echo {
  "builds": [{"src": "package.json", "use": "@vercel/static-build"}],
  "routes": [{"src": "/(.*)", "dest": "/index.html"}]
} > frontend/vercel.json
```

### **Phase 2: Database Setup (MongoDB Atlas)**

#### 1. Create Free MongoDB Cluster
1. Go to https://cloud.mongodb.com/
2. Sign up for free account
3. Create new cluster (M0 Sandbox - FREE)
4. Create database user
5. Get connection string

#### 2. Configure Database
```javascript
// Connection string format:
mongodb+srv://username:password@cluster0.mongodb.net/nepal_law_prod?retryWrites=true&w=majority
```

### **Phase 3: Backend Deployment (Railway)**

#### 1. Setup Railway Account
1. Go to https://railway.app/
2. Sign up with GitHub account
3. Get $5 monthly free credit

#### 2. Deploy Backend
1. Connect your GitHub repository
2. Select backend folder
3. Add environment variables:
   ```
   MONGO_URL=your_mongodb_connection_string
   AI_PROVIDER=google
   AI_MODEL=gemini-pro
   GOOGLE_API_KEY=your_google_api_key
   CORS_ORIGINS=*
   ```
4. Deploy automatically

#### 3. Get Backend URL
Railway will provide a URL like: `https://nepal-law-backend.railway.app`

### **Phase 4: Frontend Deployment (Vercel)**

#### 1. Setup Vercel Account
1. Go to https://vercel.com/
2. Sign up with GitHub account
3. Import your project

#### 2. Configure Frontend
1. Set build command: `npm run build`
2. Set output directory: `build`
3. Add environment variable:
   ```
   REACT_APP_BACKEND_URL=https://your-railway-backend-url.railway.app
   ```

#### 3. Deploy
Vercel will provide a URL like: `https://nepal-law-assistant.vercel.app`

### **Phase 5: AI Service Setup (Google Gemini)**

#### 1. Get Free API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key (FREE)
4. Copy the key

#### 2. Free Tier Limits
- **60 requests per minute**
- **1,500 requests per day**
- **Perfect for prototype usage**

## 🛠️ **Deployment Scripts**

### Create Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Create Vercel Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
cd frontend
vercel --prod
```

## 📋 **Production Checklist**

### **Before Deployment**
- [ ] Get Google Gemini API key
- [ ] Create MongoDB Atlas cluster
- [ ] Test locally with production settings
- [ ] Remove sensitive data from code
- [ ] Add proper error handling
- [ ] Create user documentation

### **After Deployment**
- [ ] Test all features work online
- [ ] Monitor API usage limits
- [ ] Set up basic analytics
- [ ] Create feedback mechanism
- [ ] Document known limitations

## 💰 **Cost Breakdown (FREE)**

| Service | Free Tier | Limits | Upgrade Cost |
|---------|-----------|--------|--------------|
| **Vercel** | 100GB bandwidth | 100GB/month | $20/month |
| **Railway** | $5 credit | ~500 hours | $5/month |
| **MongoDB Atlas** | 512MB storage | 512MB | $9/month |
| **Google Gemini** | 60 req/min | 1,500/day | Pay per use |

**Total FREE usage**: Perfect for prototype with moderate traffic

## 🎯 **Alternative Free Options**

### **Option A: GitHub Pages + Netlify Functions**
- Frontend: GitHub Pages (FREE)
- Backend: Netlify Functions (FREE)
- Database: FaunaDB (FREE tier)

### **Option B: Firebase Hosting + Functions**
- Frontend: Firebase Hosting (FREE)
- Backend: Firebase Functions (FREE tier)
- Database: Firestore (FREE tier)
- AI: Google Gemini (FREE tier)

### **Option C: Heroku Alternatives**
- **Render**: Free tier available
- **Fly.io**: Free tier for small apps
- **PythonAnywhere**: Free tier for Python apps

## 🔒 **Security for Public Deployment**

### **Environment Variables**
```bash
# Never commit these to GitHub
GOOGLE_API_KEY=your_secret_key
MONGO_URL=your_database_connection
```

### **Rate Limiting**
```python
# Add to server_working.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/analyze-legal-problem")
@limiter.limit("10/minute")  # Limit to 10 requests per minute
async def analyze_legal_problem(request: Request, input: LegalQueryCreate):
    # ... existing code
```

## 📱 **Marketing Your Prototype**

### **Landing Page Content**
```markdown
# 🏛️ Nepal Law Assistant (FREE)

Get instant legal guidance for Nepal law questions:
- ✅ Property disputes and inheritance
- ✅ Employment and labor issues  
- ✅ Tax notices and penalties
- ✅ Court procedures and documentation
- ✅ Contract and agreement analysis

**100% Free • AI-Powered • Nepal Law Focused**
```

### **Social Media Strategy**
- **LinkedIn**: Target Nepal legal professionals
- **Facebook**: Nepal legal help groups
- **Reddit**: r/Nepal, legal advice communities
- **Twitter**: Nepal law hashtags

## 🎉 **Launch Strategy**

### **Soft Launch**
1. **Deploy to free services**
2. **Test with friends/family**
3. **Gather initial feedback**
4. **Fix any issues**

### **Public Launch**
1. **Create social media accounts**
2. **Post in Nepal legal communities**
3. **Share with law students/professionals**
4. **Monitor usage and feedback**

### **Growth Phase**
1. **Add more features based on feedback**
2. **Upgrade to paid tiers if needed**
3. **Consider monetization options**
4. **Scale infrastructure**

## 🔗 **Quick Deploy Commands**

```bash
# 1. Prepare production build
npm run build

# 2. Deploy frontend to Vercel
cd frontend
vercel --prod

# 3. Deploy backend to Railway
cd ../backend
railway up

# 4. Update CORS origins with your frontend URL
# 5. Test everything works
```

Would you like me to help you with any specific deployment platform? I can create the exact configuration files you need! 🏛️⚖️