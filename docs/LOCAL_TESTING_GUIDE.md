# 🏛️ Nepal Law Assistant - Local Testing Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Initial Setup
```bash
# Run the setup script
setup-windows.bat
```

### Step 2: Configure AI Provider
1. Open `backend/.env` file
2. Choose your AI provider:
   ```env
   AI_PROVIDER=openai  # or anthropic, google, emergent
   ```
3. Add your API key:
   ```env
   # For OpenAI
   OPENAI_API_KEY=sk-your-openai-key-here
   
   # For Anthropic
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
   
   # For Google Gemini
   GOOGLE_API_KEY=your-google-api-key-here
   
   # For Emergent LLM
   EMERGENT_LLM_KEY=sk-emergent-your-key-here
   ```
4. Save the file

### Step 2.5: Test AI Provider (Optional)
```bash
# Test your AI configuration
python test_ai_provider.py
```

### Step 3: Start Backend
```bash
# In first terminal
start-backend.bat
```
Wait for: `✅ Platform started successfully!`

### Step 4: Start Frontend
```bash
# In second terminal
start-frontend.bat
```
Wait for: `Local: http://localhost:3000`

### Step 5: Test the Platform
```bash
# In third terminal
test-platform.bat
```

## 📋 Detailed Setup Instructions

### Prerequisites

#### 1. Python 3.8+
- Download from: https://python.org/downloads/
- ✅ Check: `python --version`

#### 2. Node.js 16+
- Download from: https://nodejs.org/
- ✅ Check: `node --version`

#### 3. MongoDB (Optional)
- **Option A**: Install locally from https://mongodb.com/try/download/community
- **Option B**: Use MongoDB Atlas (cloud) - update `MONGO_URL` in backend/.env

#### 4. Tesseract OCR (For Image Processing)
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install with Nepali language support
- Add to PATH environment variable

### Environment Configuration

#### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=nepal_law_db
CORS_ORIGINS=http://localhost:3000
EMERGENT_LLM_KEY=sk-emergent-your-actual-key-here
```

#### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8000
WDS_SOCKET_PORT=443
```

## 🧪 Testing Scenarios

### 1. Text Query Test
1. Go to http://localhost:3000
2. Click "Query" tab
3. Enter: "I received a property tax notice with penalty. What should I do?"
4. Click "Get Legal Guidance"
5. ✅ Should get detailed legal analysis

### 2. Image Upload Test
1. Click "Photo" tab
2. Upload an image of any legal document (or create a test image with text)
3. Click "Solve Problem"
4. ✅ Should extract text and provide complete solution

### 3. Document Upload Test
1. Click "Document" tab
2. Upload a PDF, DOCX, or TXT file
3. Click "Analyze Document"
4. ✅ Should analyze document and provide recommendations

### 4. Legal Research Test
1. Click "Research" tab
2. Enter: "Property inheritance laws in Nepal with Supreme Court precedents"
3. Click "Conduct Legal Research"
4. ✅ Should provide comprehensive research with case precedents

## 🔧 Troubleshooting

### Backend Issues

#### "Module not found" Error
```bash
cd backend
venv\Scripts\activate.bat
pip install -r requirements.txt
```

#### "MongoDB connection failed"
- **Local MongoDB**: Start MongoDB service
- **Cloud MongoDB**: Update MONGO_URL in .env with your Atlas connection string

#### "LLM API key not configured"
- Edit `backend/.env`
- Add your Emergent LLM API key: `EMERGENT_LLM_KEY=sk-emergent-your-key`

#### "Tesseract not found"
- Install Tesseract OCR from official website
- Add Tesseract installation directory to Windows PATH
- Restart command prompt

### Frontend Issues

#### "npm install" fails
```bash
cd frontend
npm cache clean --force
npm install
```

#### "Backend connection failed"
- Ensure backend is running on http://localhost:8000
- Check `frontend/.env` has correct `REACT_APP_BACKEND_URL`

### OCR Issues

#### "Image processing failed"
- Install Tesseract with Nepali language support
- Ensure image is clear and readable
- Try different image formats (JPG, PNG)

## 📊 Test Results Interpretation

### Successful Test Output
```
🏛️ Nepal Law Assistant Platform - Comprehensive Testing
============================================================

API Health:
--------------------
✅ API health check successful - Message: Nepal Law Assistant API

Text Query:
--------------------
✅ Text query successful - Analysis length: 1250 chars

Problem Solver:
--------------------
✅ Problem solver successful - Urgency: high, Success rate: 85%
   Immediate actions: 3
   Solution steps: 5

📊 TEST SUMMARY
============================================================
API Health           ✅ PASS
Text Query           ✅ PASS
Problem Solver       ✅ PASS
Legal Research       ✅ PASS
Official Forms       ✅ PASS
Case Studies         ✅ PASS
Form Search          ✅ PASS
History              ✅ PASS

Overall: 8/8 tests passed (100.0%)

🎉 All tests passed! Platform is working correctly.
```

## 🎯 Manual Testing Checklist

### Core Features
- [ ] Text query analysis works
- [ ] Image upload and OCR works
- [ ] Document upload works
- [ ] Legal research provides precedents
- [ ] Problem solver gives actionable steps
- [ ] History shows previous queries
- [ ] Official forms are displayed
- [ ] Case studies are relevant

### UI/UX Testing
- [ ] All tabs switch correctly
- [ ] File upload shows progress
- [ ] Results display properly formatted
- [ ] Mobile responsive design works
- [ ] Error messages are clear
- [ ] Loading states work

### Performance Testing
- [ ] Page loads under 3 seconds
- [ ] API responses under 10 seconds
- [ ] Large file uploads work (up to 10MB)
- [ ] Multiple concurrent users supported

## 🚀 Production Deployment

### Environment Variables
```env
# Production Backend
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/nepal_law_prod
DB_NAME=nepal_law_production
CORS_ORIGINS=https://yourdomain.com
EMERGENT_LLM_KEY=sk-emergent-production-key

# Production Frontend
REACT_APP_BACKEND_URL=https://api.yourdomain.com
```

### Build Commands
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
npx serve -s build -l 3000
```

## 📞 Support

### Common Issues
1. **OCR not working**: Install Tesseract OCR with Nepali support
2. **API key errors**: Get valid Emergent LLM API key
3. **Database errors**: Ensure MongoDB is running
4. **CORS errors**: Check frontend/backend URL configuration

### Getting Help
- Check logs in terminal for detailed error messages
- Ensure all prerequisites are installed
- Verify environment variables are set correctly
- Test with simple queries first before complex documents

---

**🏛️ Nepal Law Assistant Platform - Empowering Legal Access Through Technology**