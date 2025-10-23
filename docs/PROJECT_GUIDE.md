# 📘 Complete Project Guide - Nepal Law Assistant

**For Non-Programmers & New Developers**

This guide explains everything about the Nepal Law Assistant project in simple terms. No technical jargon - just clear explanations!

---

## 🎯 What Does This Project Do?

**Nepal Law Assistant** is a website that helps people understand Nepal law using AI (Artificial Intelligence). Think of it like ChatGPT, but specialized for Nepal legal questions.

**Example:**
- User asks: "My neighbor built a wall on my property. What can I do?"
- AI responds: Explains Nepal property laws, next steps, costs, and procedures

---

## 🏗️ How Is The Project Organized?

Your project has 3 main parts:

```
LawGpt/
├── backend/          ← The "brain" (Python server that talks to AI)
├── frontend/         ← The "face" (Website users see and interact with)
└── docs/            ← Documentation (guides and instructions)
```

### 1. **Backend** (The Brain) 🧠
- **What it does:** Receives questions, sends them to Google AI, gets answers back
- **Language:** Python (a programming language)
- **Main file:** `backend/server_working.py`

### 2. **Frontend** (The Face) 👤
- **What it does:** The website users see - text box, buttons, chat interface
- **Language:** React (JavaScript for websites)
- **Main file:** `frontend/src/App.js`

### 3. **Docs** (The Manual) 📚
- **What it does:** Instructions and guides (like this one!)
- **Language:** Markdown (simple text formatting)

---

## 🔑 Key Files You Should Know

### Backend Files (Python)

| File | What It Does | When To Edit |
|------|-------------|--------------|
| `server_working.py` | Main server - handles all requests | Add new features, fix bugs |
| `legal_knowledge.py` | AI prompts for Nepal law | Improve AI responses, add legal knowledge |
| `ai_providers.py` | Connects to Google AI | Change AI provider, update API settings |
| `requirements.txt` | List of Python libraries needed | Add new Python packages |
| `.env` | Secret keys (API keys, passwords) | Update API keys, change settings |

### Frontend Files (React)

| File | What It Does | When To Edit |
|------|-------------|--------------|
| `src/App.js` | Main website code | Change website features, add buttons |
| `src/App.css` | Website styling (colors, fonts) | Change how website looks |
| `package.json` | List of JavaScript libraries | Add new JavaScript packages |
| `public/index.html` | Base HTML page | Change page title, add meta tags |

### Configuration Files

| File | What It Does | When To Edit |
|------|-------------|--------------|
| `.env.example` | Template for secret keys | Show what keys are needed |
| `.gitignore` | Files NOT to upload to GitHub | Add files to ignore |
| `README.md` | Project description | Update project info |

---

## 🔄 How Does Everything Work Together?

### Simple Flow:

```
1. User types question on website (Frontend)
   ↓
2. Frontend sends question to Backend
   ↓
3. Backend sends question to Google AI
   ↓
4. Google AI generates answer about Nepal law
   ↓
5. Backend receives answer
   ↓
6. Backend sends answer to Frontend
   ↓
7. User sees answer on website (Frontend)
```

### Technical Flow:

```
User Browser (localhost:3000)
    ↓ HTTP Request
Backend Server (localhost:8000)
    ↓ API Call
Google Gemini AI
    ↓ AI Response
Backend Server
    ↓ HTTP Response
User Browser (shows answer)
```

---

## 🚀 How To Run The Project

### Step 1: Start Backend (The Brain)

```bash
# Open terminal/command prompt
cd backend
python server_working.py
```

**What you'll see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**This means:** Backend is running! ✅

### Step 2: Start Frontend (The Face)

```bash
# Open NEW terminal/command prompt
cd frontend
npm start
```

**What you'll see:**
```
Compiled successfully!
Local: http://localhost:3000
```

**This means:** Website is running! ✅

### Step 3: Use The Website

Open browser and go to: `http://localhost:3000`

---

## 🔧 Common Tasks & Where To Look

### Task 1: Change AI Responses

**File to edit:** `backend/legal_knowledge.py`

**What to change:**
```python
# Find this section:
SYSTEM_PROMPT = """
You are a Nepal Law Assistant...
"""
```

**Example change:**
```python
# Make AI more friendly
SYSTEM_PROMPT = """
You are a friendly Nepal Law Assistant who explains laws in simple terms...
"""
```

### Task 2: Change Website Colors

**File to edit:** `frontend/src/App.css`

**What to change:**
```css
/* Find colors like this: */
background-color: #1a1a2e;

/* Change to new color: */
background-color: #2c3e50;
```

### Task 3: Add New Button

**File to edit:** `frontend/src/App.js`

**What to add:**
```javascript
<button onClick={handleNewFeature}>
  New Feature
</button>
```

### Task 4: Update API Key

**File to edit:** `backend/.env`

**What to change:**
```env
# Old key
GOOGLE_API_KEY=old_key_here

# New key
GOOGLE_API_KEY=new_key_here
```

---

## 🌐 How Is It Deployed Online?

Your project uses 2 services:

### 1. **Railway** (Backend Hosting)
- **What it does:** Runs your Python backend 24/7
- **URL:** `https://your-app.railway.app`
- **Cost:** Free tier available

**How it works:**
1. You push code to GitHub
2. Railway automatically detects changes
3. Railway rebuilds and deploys backend
4. Backend is live!

### 2. **Vercel** (Frontend Hosting)
- **What it does:** Hosts your website 24/7
- **URL:** `https://law-gpt.vercel.app`
- **Cost:** Free tier available

**How it works:**
1. You push code to GitHub
2. Vercel automatically detects changes
3. Vercel rebuilds and deploys website
4. Website is live!

---

## 🔐 Environment Variables (Secret Keys)

### What Are They?

Environment variables are like passwords - they're secret values your app needs to work.

### Where Are They?

**Local Development:**
- File: `backend/.env`
- Not uploaded to GitHub (kept secret)

**Production (Online):**
- Railway Dashboard → Environment Variables
- Vercel Dashboard → Environment Variables

### Important Variables:

| Variable | What It Does | Where To Get It |
|----------|-------------|-----------------|
| `GOOGLE_API_KEY` | Connects to Google AI | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| `ALLOWED_ORIGINS` | Which websites can use your API | Your frontend URL |
| `AI_MODEL` | Which AI model to use | `gemini-2.5-flash` |

---

## 🐛 Common Problems & Solutions

### Problem 1: Backend Won't Start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Problem 2: Frontend Won't Start

**Error:** `'react-scripts' is not recognized`

**Solution:**
```bash
cd frontend
npm install
```

### Problem 3: API Key Error

**Error:** `Invalid API key`

**Solution:**
1. Check `backend/.env` file
2. Make sure `GOOGLE_API_KEY` is set
3. Get new key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Problem 4: CORS Error

**Error:** `Access to fetch blocked by CORS policy`

**Solution:**
Edit `backend/server_working.py`:
```python
# Add your frontend URL
allow_origins=[
    "http://localhost:3000",
    "https://law-gpt.vercel.app"
]
```

### Problem 5: Port Already In Use

**Error:** `Address already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

---

## 👥 Working With A Developer

### What To Share With Them:

1. **GitHub Repository Link**
   - `https://github.com/dhananjayyadav95/LawGpt`

2. **This Documentation**
   - Share `docs/PROJECT_GUIDE.md`

3. **Access To Deployment Platforms**
   - Railway account access
   - Vercel account access

4. **Environment Variables**
   - Share API keys securely (not via email!)
   - Use password manager or secure sharing tool

### Questions They Might Ask:

**Q: What's the tech stack?**
A: Backend: Python + FastAPI, Frontend: React, AI: Google Gemini

**Q: Where is the database?**
A: Currently no database - uses local storage in browser

**Q: What's the deployment process?**
A: Automatic via GitHub - push to `dev.deploy` branch

**Q: Are there any tests?**
A: Not yet - this is an MVP (Minimum Viable Product)

**Q: What's the API documentation?**
A: See `docs/AI_PROVIDER_GUIDE.md` and `docs/QUICK_START.md`

---

## 📊 Project Structure Explained

### Backend Structure:

```
backend/
├── server_working.py       ← Main server (START HERE)
├── legal_knowledge.py     ← AI prompts for Nepal law
├── ai_providers.py        ← Google AI connection
├── requirements.txt       ← Python packages needed
├── .env                   ← Secret keys (DON'T SHARE)
├── .env.example          ← Template for .env
├── Procfile              ← Railway deployment config
└── railway.toml          ← Railway settings
```

### Frontend Structure:

```
frontend/
├── src/
│   ├── App.js            ← Main website code (START HERE)
│   └── App.css           ← Website styling
├── public/
│   └── index.html        ← Base HTML page
├── package.json          ← JavaScript packages needed
└── .env.template         ← Template for environment variables
```

---

## 🎓 Learning Resources

### If You Want To Learn More:

**Python (Backend):**
- [Python for Beginners](https://www.python.org/about/gettingstarted/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

**React (Frontend):**
- [React Official Tutorial](https://react.dev/learn)
- [React for Beginners](https://www.youtube.com/watch?v=SqcY0GlETPk)

**Git & GitHub:**
- [GitHub Guides](https://guides.github.com/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)

**AI Integration:**
- [Google Gemini API Docs](https://ai.google.dev/docs)

---

## 🔄 Making Changes - Step by Step

### Scenario: You Want To Change AI Response Style

**Step 1:** Open the file
```bash
# Open in any text editor
backend/legal_knowledge.py
```

**Step 2:** Find the prompt
```python
# Look for SYSTEM_PROMPT variable
SYSTEM_PROMPT = """..."""
```

**Step 3:** Make changes
```python
# Change the text inside the quotes
SYSTEM_PROMPT = """
You are a friendly Nepal Law Assistant...
"""
```

**Step 4:** Save the file

**Step 5:** Restart backend
```bash
# Stop backend (Ctrl+C)
# Start again
python server_working.py
```

**Step 6:** Test on website
- Go to `http://localhost:3000`
- Ask a question
- See if response changed

**Step 7:** If good, upload to GitHub
```bash
git add backend/legal_knowledge.py
git commit -m "Updated AI response style"
git push origin dev.deploy
```

**Step 8:** Wait 2-3 minutes
- Railway automatically deploys
- Check live website

---

## 📝 Important Notes

### DO's ✅

- ✅ Keep `.env` file secret (never share or upload)
- ✅ Test changes locally before deploying
- ✅ Read error messages carefully
- ✅ Ask for help when stuck
- ✅ Keep documentation updated
- ✅ Use meaningful commit messages

### DON'Ts ❌

- ❌ Never share API keys publicly
- ❌ Don't edit files directly on GitHub
- ❌ Don't delete files you don't understand
- ❌ Don't push untested code to production
- ❌ Don't ignore error messages
- ❌ Don't forget to save files before testing

---

## 🆘 Getting Help

### If You're Stuck:

1. **Check Error Message**
   - Read what it says
   - Google the error message

2. **Check Documentation**
   - Look in `/docs` folder
   - Read `README.md`

3. **Check GitHub Issues**
   - See if others had same problem
   - Search closed issues too

4. **Ask AI Assistant**
   - Use ChatGPT or Claude
   - Share error message and context

5. **Ask Developer Community**
   - Stack Overflow
   - Reddit r/learnprogramming
   - Discord programming servers

---

## 🎯 Next Steps For Your Project

### Short Term (1-2 weeks):
- [ ] Add user authentication (login system)
- [ ] Save chat history in database
- [ ] Add document upload feature
- [ ] Improve mobile responsiveness

### Medium Term (1-2 months):
- [ ] Add Nepali language support
- [ ] Create lawyer directory
- [ ] Add legal document templates
- [ ] Implement payment system

### Long Term (3-6 months):
- [ ] Build mobile app
- [ ] Add voice input/output
- [ ] Create admin dashboard
- [ ] Add analytics and reporting

---

## 📞 Contact & Support

**Project Owner:** Dhananjay Yadav
**GitHub:** https://github.com/dhananjayyadav95/LawGpt
**Live Demo:** https://law-gpt.vercel.app

---

**Remember:** Every developer was a beginner once. Don't be afraid to experiment, make mistakes, and learn! 🚀

**Last Updated:** October 23, 2025
