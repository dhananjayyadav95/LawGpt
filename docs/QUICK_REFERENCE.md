# ⚡ Quick Reference Guide - Nepal Law Assistant

**One-page cheat sheet for common tasks**

---

## 🚀 Quick Start Commands

### Start Development

```bash
# Terminal 1 - Backend
cd backend
python server_working.py

# Terminal 2 - Frontend
cd frontend
npm start
```

### Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📁 Important Files

| File | Purpose | Edit When |
|------|---------|-----------|
| `backend/server_working.py` | Main server | Add features, fix bugs |
| `backend/legal_knowledge.py` | AI prompts | Change AI responses |
| `backend/ai_providers.py` | AI connection | Change AI provider |
| `backend/.env` | Secret keys | Update API keys |
| `frontend/src/App.js` | Website code | Change UI/features |
| `frontend/src/App.css` | Styling | Change colors/layout |

---

## 🔧 Common Tasks

### Change AI Response Style

**File:** `backend/legal_knowledge.py`

```python
# Find and edit:
SYSTEM_PROMPT = """
Your new instructions here...
"""
```

### Update API Key

**File:** `backend/.env`

```env
GOOGLE_API_KEY=your_new_key_here
```

### Change Website Colors

**File:** `frontend/src/App.css`

```css
/* Find and change: */
background-color: #1a1a2e;  /* Change this */
color: #ffffff;             /* And this */
```

### Add New Button

**File:** `frontend/src/App.js`

```javascript
<button onClick={handleClick}>
  Button Text
</button>
```

---

## 🌐 Deployment

### Push Changes to Production

```bash
# 1. Save all files
# 2. Commit changes
git add .
git commit -m "Description of changes"

# 3. Push to GitHub
git push origin dev.deploy

# 4. Wait 2-3 minutes for auto-deployment
```

### Check Deployment Status

**Railway (Backend):**
- Go to: https://railway.app
- Check deployment logs

**Vercel (Frontend):**
- Go to: https://vercel.com
- Check deployment status

---

## 🔑 Environment Variables

### Local Development

**File:** `backend/.env`

```env
GOOGLE_API_KEY=your_key_here
AI_PROVIDER=google
AI_MODEL=gemini-2.5-flash
ALLOWED_ORIGINS=http://localhost:3000
PORT=8000
```

### Production

**Railway Dashboard:**
- `GOOGLE_API_KEY` = your_production_key
- `ALLOWED_ORIGINS` = https://law-gpt.vercel.app

**Vercel Dashboard:**
- `REACT_APP_BACKEND_URL` = https://your-app.railway.app

---

## 🐛 Quick Fixes

### Backend Won't Start

```bash
cd backend
pip install -r requirements.txt
python server_working.py
```

### Frontend Won't Start

```bash
cd frontend
npm install
npm start
```

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <number> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### CORS Error

**File:** `backend/server_working.py`

```python
# Add your frontend URL:
allow_origins=[
    "http://localhost:3000",
    "https://law-gpt.vercel.app"
]
```

---

## 📊 Project Structure

```
LawGpt/
├── backend/
│   ├── server_working.py      ← Main server
│   ├── legal_knowledge.py    ← AI prompts
│   ├── ai_providers.py       ← AI connection
│   ├── requirements.txt      ← Python packages
│   └── .env                  ← Secret keys
├── frontend/
│   ├── src/
│   │   ├── App.js           ← Main code
│   │   └── App.css          ← Styling
│   └── package.json         ← JS packages
├── docs/                    ← Documentation
└── README.md               ← Project info
```

---

## 🔍 Where to Find Things

### Want to change...

**AI responses?**
→ `backend/legal_knowledge.py`

**Website look?**
→ `frontend/src/App.css`

**Website features?**
→ `frontend/src/App.js`

**API keys?**
→ `backend/.env`

**Deployment settings?**
→ Railway/Vercel dashboard

---

## 📞 Getting Help

### Error Messages

1. **Read the error** - it usually tells you what's wrong
2. **Google the error** - someone else probably had it
3. **Check docs** - look in `/docs` folder
4. **Ask AI** - ChatGPT, Claude, etc.

### Useful Links

- **Project Guide:** `docs/PROJECT_GUIDE.md`
- **Technical Docs:** `docs/TECHNICAL_ARCHITECTURE.md`
- **GitHub:** https://github.com/dhananjayyadav95/LawGpt
- **Live Site:** https://law-gpt.vercel.app

---

## ⚙️ Git Commands

```bash
# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin dev.deploy

# Pull latest changes
git pull origin dev.deploy

# See commit history
git log --oneline
```

---

## 🧪 Testing Locally

### Test Backend

```bash
# Start backend
cd backend
python server_working.py

# In browser, go to:
http://localhost:8000/docs

# Try the API endpoints
```

### Test Frontend

```bash
# Start frontend
cd frontend
npm start

# In browser, go to:
http://localhost:3000

# Ask a legal question
```

---

## 📝 Making Changes Checklist

- [ ] Edit the file
- [ ] Save the file
- [ ] Test locally
- [ ] If good, commit to git
- [ ] Push to GitHub
- [ ] Wait for deployment
- [ ] Test on live site

---

## 🎯 Common URLs

| Service | URL |
|---------|-----|
| Live Website | https://law-gpt.vercel.app |
| GitHub Repo | https://github.com/dhananjayyadav95/LawGpt |
| Railway Dashboard | https://railway.app |
| Vercel Dashboard | https://vercel.com |
| Google AI Studio | https://makersuite.google.com |

---

## 💡 Pro Tips

1. **Always test locally first** before pushing to production
2. **Save files before testing** - unsaved changes won't work
3. **Read error messages** - they're usually helpful
4. **Use meaningful commit messages** - helps track changes
5. **Keep API keys secret** - never share or upload them
6. **Restart servers after changes** - some changes need restart
7. **Check browser console** - shows frontend errors
8. **Check terminal** - shows backend errors

---

## 🆘 Emergency Contacts

**If something breaks:**

1. Check error message
2. Check recent changes (git log)
3. Revert last change if needed
4. Check deployment logs
5. Ask for help with error details

**Rollback to previous version:**

```bash
# See recent commits
git log --oneline

# Revert to previous commit
git revert HEAD

# Push the revert
git push origin dev.deploy
```

---

**Keep this guide handy for quick reference!** 📌

**Last Updated:** October 23, 2025
