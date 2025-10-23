# Quick Production Fixes (Do These Now!)

## 🔥 Critical Fixes (30 minutes total)

### 1. Remove Hardcoded API Key (5 min)

**Current Problem:**
```python
os.environ['GOOGLE_API_KEY'] = 'your_hardcoded_api_key_here'
```

**Fix:**
Remove this line and use environment variable only:
```python
# In server_working.py, remove the hardcoded key
# Just use: os.environ.get('GOOGLE_API_KEY')
```

**On deployment platform:**
- Set environment variable: `GOOGLE_API_KEY=your_key_here`

---

### 2. Fix CORS Security (5 min)

**Current Problem:**
```python
allow_origins=["*"]  # Allows ANY website to call your API
```

**Fix:**
```python
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com",
    "http://localhost:3000"  # for development only
]
```

---

### 3. Add Rate Limiting (20 min)

**Install:**
```bash
pip install slowapi
```

**Add to server_working.py:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add to endpoints:
@app.post("/api/analyze-legal-problem")
@limiter.limit("10/minute")  # 10 requests per minute
async def analyze_legal_problem(request: Request, input: LegalQueryCreate):
    # ... existing code
```

---

## 📊 Recommended Deployment Setup

### Option 1: Railway (Easiest)

**Backend:**
1. Connect GitHub repo
2. Select `backend` folder
3. Add environment variables:
   - `GOOGLE_API_KEY`
   - `PORT=8000`
4. Deploy automatically

**Frontend:**
1. Use Vercel (connects to GitHub)
2. Set build command: `npm run build`
3. Set environment variable:
   - `REACT_APP_BACKEND_URL=https://your-backend.railway.app`

### Option 2: All-in-One (Render)

**Backend + Frontend together:**
1. Create new Web Service
2. Connect GitHub
3. Set environment variables
4. Deploy

---

## 🗄️ Database Setup (Choose One)

### Option A: MongoDB Atlas (Recommended)
- Free tier: 512MB storage
- Easy setup
- Good for flexible data

**Steps:**
1. Create account at mongodb.com/atlas
2. Create free cluster
3. Get connection string
4. Add to environment: `MONGODB_URI=mongodb+srv://...`

### Option B: Supabase (If you want auth too)
- Free tier: 500MB database
- Built-in authentication
- PostgreSQL

**Steps:**
1. Create account at supabase.com
2. Create project
3. Get connection string
4. Includes user auth out of the box

---

## 🚀 Deployment Commands

### Build Frontend:
```bash
cd frontend
npm run build
```

### Test Backend Locally:
```bash
cd backend
python server_working.py
```

### Environment Variables Needed:

**Backend (.env):**
```
GOOGLE_API_KEY=your_actual_key_here
AI_PROVIDER=google
AI_MODEL=gemini-2.5-flash
FRONTEND_URL=https://yourdomain.com
PORT=8000
```

**Frontend (.env):**
```
REACT_APP_BACKEND_URL=https://your-backend-url.com
```

---

## ✅ Pre-Deploy Checklist

- [ ] API key moved to environment variable
- [ ] CORS restricted to your domain
- [ ] Rate limiting added
- [ ] .env files not in git
- [ ] Frontend built successfully
- [ ] Backend tested locally
- [ ] Environment variables set on platform
- [ ] Database connected (if using)

---

## 🆘 If Something Goes Wrong

### Backend won't start:
1. Check logs on deployment platform
2. Verify environment variables are set
3. Check Python version (3.9+)
4. Verify all dependencies in requirements.txt

### Frontend can't connect to backend:
1. Check CORS settings
2. Verify REACT_APP_BACKEND_URL is correct
3. Check browser console for errors
4. Verify backend is running

### API key errors:
1. Verify key is set in environment
2. Check key is valid in Google Cloud Console
3. Ensure API is enabled (Gemini API)

---

## 📞 Next Steps

1. **Fix the 3 critical issues above**
2. **Choose deployment platform**
3. **Set up database (optional for MVP)**
4. **Deploy and test**
5. **Monitor for issues**

**Want me to help you implement any of these fixes?**
