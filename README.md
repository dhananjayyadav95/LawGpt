  # Nepal Law Assistant 🏛️

AI-powered legal assistance platform for Nepal law with streaming responses and comprehensive legal guidance.

## 🌟 Features

- **🤖 AI-Powered:** Google Gemini 2.5 Flash integration
- **🇳🇵 Nepal Law Expertise:** Specialized in Nepal legal system
- **⚡ Streaming Responses:** Real-time text like ChatGPT
- **📱 Mobile Responsive:** Works on all devices
- **💾 Query History:** Save and revisit previous queries
- **🔒 Secure:** Environment-based config, CORS protection, rate limiting
- **🆓 Free to Use:** No subscription required

## 🏗️ Tech Stack

- **Backend:** FastAPI (Python 3.9+)
- **Frontend:** React.js with Tailwind CSS
- **AI:** Google Gemini 2.5 Flash
- **Deployment:** Railway (Backend) + Vercel (Frontend)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/dhananjayyadav95/LawGpt.git
cd LawGpt
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
python server_working.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 4. Environment Variables
Create `backend/.env` with:
```env
GOOGLE_API_KEY=your_google_api_key_here
AI_PROVIDER=google
AI_MODEL=gemini-2.5-flash
ALLOWED_ORIGINS=http://localhost:3000
```

## �  Usage Examples

### Legal Query
```
"My neighbor built a wall on my property. What are my rights under Nepal law?"
```

### Legal Research
```
"Research property inheritance laws in Nepal including recent court decisions"
```

## 🚀 Production Deployment

### Backend (Railway)
1. Connect GitHub repository
2. Set environment variables:
   - `GOOGLE_API_KEY`
   - `ALLOWED_ORIGINS=https://your-frontend.vercel.app`
3. Deploy automatically

### Frontend (Vercel)
1. Import GitHub repository
2. Set environment variable:
   - `REACT_APP_BACKEND_URL=https://your-backend.railway.app`
3. Deploy automatically

## 📚 Documentation

Detailed documentation available in `/docs`:

- [Production Checklist](docs/PRODUCTION_CHECKLIST.md)
- [AI Provider Guide](docs/AI_PROVIDER_GUIDE.md)
- [Security Guide](docs/SECURITY_FIXES_APPLIED.md)
- [Quick Start Guide](docs/QUICK_START.md)
- [Streaming Features](docs/STREAMING_FEATURE.md)

## 🔧 Project Structure

```
├── backend/
│   ├── server_working.py      # Main FastAPI server
│   ├── legal_knowledge.py    # AI prompts and legal logic
│   ├── ai_providers.py       # AI provider integrations
│   ├── requirements.txt      # Python dependencies
│   └── .env.example         # Environment template
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   └── App.css          # Styles
│   ├── package.json         # Node dependencies
│   └── public/index.html    # HTML template
├── docs/                    # Documentation
├── .github/workflows/       # CI/CD
└── README.md               # This file
```

## 🎯 Key Features

### User Experience
- **Click logo** → Refresh page
- **Press Enter** → Submit query
- **Shift+Enter** → New line
- **Streaming responses** → Real-time feedback
- **Visual indicators** → Severity, cost, timeline

### AI Response Structure
1. **Quick Answer** (2-3 sentences)
2. **Immediate Next Step** (what to do now)
3. **Situation Assessment** (severity, cost, timeline)
4. **Your Options** (2-3 clear paths)
5. **Step-by-Step Plan** (weekly breakdown)
6. **Legal Basis** (specific laws and citations)
7. **Practical Details** (offices, contacts, costs)
8. **Warnings** (common mistakes to avoid)

## �L Security Features

- ✅ No hardcoded API keys
- ✅ CORS protection
- ✅ Rate limiting (10 requests/minute)
- ✅ Input validation
- ✅ Environment-based configuration

## � ePerformance

- **Streaming responses** for better perceived performance
- **Optimized prompts** for faster AI processing
- **Local storage** for query history
- **Mobile-first** responsive design

## 🎯 Roadmap

- [ ] User authentication (Google OAuth)
- [ ] Database integration (MongoDB)
- [ ] Document upload and analysis
- [ ] Lawyer marketplace
- [ ] Nepali language support
- [ ] Mobile app (React Native)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- 📖 Check documentation in `/docs`
- � Report tissues on GitHub
- 💬 Discussions welcome

---

**🌐 Live Demo:** [https://law-gpt.vercel.app](https://law-gpt.vercel.app)

**📊 Status:** ✅ Production Ready | 🔒 Secure | ⚡ Fast | 📱 Mobile-Friendly

**Made with ❤️ for Nepal's legal community**
