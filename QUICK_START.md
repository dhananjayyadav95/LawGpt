# 🚀 Quick Start Guide - Nepal Law Assistant

## ⚡ **Super Quick Setup (5 Minutes)**

### **Option 1: OpenAI (Recommended)**
```bash
# 1. Setup
setup-windows.bat
# Choose option 1 (Minimal installation)

# 2. Get OpenAI API key from https://platform.openai.com/api-keys

# 3. Edit backend\.env:
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-openai-key-here

# 4. Start platform
start-backend.bat    # Terminal 1
start-frontend.bat   # Terminal 2

# 5. Open http://localhost:3000
```

### **Option 2: Google Gemini (Free Tier)**
```bash
# 1. Setup
setup-windows.bat
# Choose option 1 (Minimal installation)

# 2. Get free API key from https://makersuite.google.com/app/apikey

# 3. Edit backend\.env:
AI_PROVIDER=google
GOOGLE_API_KEY=your-google-api-key-here

# 4. Start platform
start-backend.bat    # Terminal 1
start-frontend.bat   # Terminal 2

# 5. Open http://localhost:3000
```

### **Option 3: Anthropic Claude**
```bash
# 1. Setup
setup-windows.bat
# Choose option 1 (Minimal installation)

# 2. Get API key from https://console.anthropic.com/

# 3. Edit backend\.env:
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# 4. Start platform
start-backend.bat    # Terminal 1
start-frontend.bat   # Terminal 2

# 5. Open http://localhost:3000
```

## 🎯 **What You DON'T Need**

### ❌ **No Emergent Integrations Required**
- The platform works perfectly without `emergentintegrations`
- Only install it if you specifically want to use Emergent LLM provider
- All other providers (OpenAI, Anthropic, Google) work out of the box

### ❌ **No Complex Setup**
- No Docker required
- No complex database setup (uses cloud MongoDB by default)
- No special configurations

## ✅ **What You DO Need**

### **Required:**
- Python 3.8+
- Node.js 16+
- API key from any supported provider

### **Optional:**
- MongoDB (uses cloud by default)
- Tesseract OCR (for image processing)

## 🧪 **Test Your Setup**

```bash
# Test everything works
python test_ai_provider.py
test-platform.bat
```

## 💰 **Cost Comparison**

| Provider | Free Tier | Cost/1000 queries | Quality |
|----------|-----------|-------------------|---------|
| **Google Gemini** | ✅ Yes | ~$10/month | ⭐⭐⭐⭐ |
| **OpenAI GPT-4** | ❌ No | ~$45/month | ⭐⭐⭐⭐⭐ |
| **Anthropic Claude** | ❌ No | ~$25/month | ⭐⭐⭐⭐⭐ |

*Estimates for typical legal assistant usage*

## 🎉 **You're Done!**

The platform now runs with:
- ✅ AI-powered legal analysis
- ✅ Document OCR and processing  
- ✅ Problem-solving with actionable steps
- ✅ Real case studies and examples
- ✅ Official forms and procedures

**No emergentintegrations needed!** 🎯