# 🤖 AI Provider Configuration Guide

The Nepal Law Assistant platform supports multiple AI providers. You can choose the one that best fits your needs and budget.

## 🎯 Supported AI Providers

### 1. **OpenAI GPT-4** (Recommended)
- **Model**: GPT-4, GPT-4 Turbo, GPT-3.5 Turbo
- **Strengths**: Excellent reasoning, reliable, well-documented
- **Cost**: Moderate ($0.03/1K tokens for GPT-4)
- **Setup**: Easy, widely available

### 2. **Anthropic Claude**
- **Model**: Claude-3 Sonnet, Claude-3 Haiku, Claude-3 Opus
- **Strengths**: Great for analysis, safety-focused, long context
- **Cost**: Competitive ($0.015/1K tokens for Sonnet)
- **Setup**: Easy, good API

### 3. **Google Gemini**
- **Model**: Gemini Pro, Gemini Pro Vision
- **Strengths**: Free tier available, good performance
- **Cost**: Free tier + paid options
- **Setup**: Google AI Studio account needed

### 4. **Emergent LLM** (Optional)
- **Model**: Various models through Emergent platform
- **Strengths**: Specialized for legal use cases
- **Cost**: Varies by model
- **Setup**: Emergent platform account + `pip install emergentintegrations`
- **Note**: Not required - other providers work great!

## ⚙️ Configuration Steps

### Step 1: Choose Your Provider

Edit `backend/.env` file and set:
```env
AI_PROVIDER=openai  # or anthropic, google, emergent
```

### Step 2: Configure API Key

#### For OpenAI:
```env
AI_PROVIDER=openai
AI_MODEL=gpt-4
OPENAI_API_KEY=sk-your-openai-api-key-here
```

#### For Anthropic:
```env
AI_PROVIDER=anthropic
AI_MODEL=claude-3-sonnet-20240229
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

#### For Google Gemini:
```env
AI_PROVIDER=google
AI_MODEL=gemini-pro
GOOGLE_API_KEY=your-google-api-key-here
```

#### For Emergent LLM:
```env
AI_PROVIDER=emergent
AI_MODEL=gemini-2.5-pro
EMERGENT_LLM_KEY=sk-emergent-your-key-here
```

## 🔑 Getting API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create new secret key
5. Copy the key (starts with `sk-`)

**Cost**: Pay-per-use, ~$0.03 per 1K tokens for GPT-4

### Anthropic API Key
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create new key
5. Copy the key (starts with `sk-ant-`)

**Cost**: Pay-per-use, ~$0.015 per 1K tokens for Claude-3 Sonnet

### Google Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Copy the key

**Cost**: Free tier available (60 requests/minute), then pay-per-use

### Emergent LLM API Key
1. Contact Emergent platform for access
2. Get your API key from dashboard
3. Copy the key (starts with `sk-emergent-`)

**Cost**: Varies by model and usage

## 🎛️ Model Selection

### Recommended Models by Use Case

#### **General Legal Analysis** (Balanced cost/performance)
```env
# OpenAI
AI_PROVIDER=openai
AI_MODEL=gpt-4

# Anthropic
AI_PROVIDER=anthropic
AI_MODEL=claude-3-sonnet-20240229

# Google
AI_PROVIDER=google
AI_MODEL=gemini-pro
```

#### **Budget-Conscious** (Lower cost)
```env
# OpenAI
AI_PROVIDER=openai
AI_MODEL=gpt-3.5-turbo

# Anthropic
AI_PROVIDER=anthropic
AI_MODEL=claude-3-haiku-20240307

# Google (Free tier)
AI_PROVIDER=google
AI_MODEL=gemini-pro
```

#### **High-Performance** (Best quality)
```env
# OpenAI
AI_PROVIDER=openai
AI_MODEL=gpt-4-turbo

# Anthropic
AI_PROVIDER=anthropic
AI_MODEL=claude-3-opus-20240229
```

## 🧪 Testing Your Configuration

### 1. Check Configuration
```bash
python health_check.py
```

### 2. Test API Connection
```bash
python -c "
from backend.ai_providers import get_ai_provider
import asyncio

async def test():
    provider = get_ai_provider()
    response = await provider.generate_response(
        'You are a helpful assistant.',
        'Say hello in one sentence.'
    )
    print(f'✅ AI Provider working: {response}')

asyncio.run(test())
"
```

### 3. Run Platform Tests
```bash
test-platform.bat
```

## 💰 Cost Comparison

### Typical Usage (1000 legal queries/month)

| Provider | Model | Cost/Month | Quality | Speed |
|----------|-------|------------|---------|-------|
| OpenAI | GPT-4 | ~$45 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| OpenAI | GPT-3.5 Turbo | ~$15 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Anthropic | Claude-3 Sonnet | ~$25 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Anthropic | Claude-3 Haiku | ~$8 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Google | Gemini Pro | ~$10 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

*Estimates based on average 1500 tokens per query*

## 🔄 Switching Providers

You can easily switch between providers:

1. **Update `.env` file**:
   ```env
   AI_PROVIDER=anthropic  # Change from openai to anthropic
   ANTHROPIC_API_KEY=your-key-here
   ```

2. **Restart backend**:
   ```bash
   # Stop current backend (Ctrl+C)
   start-backend.bat
   ```

3. **Test new provider**:
   ```bash
   test-platform.bat
   ```

## 🛠️ Troubleshooting

### "No API key found" Error
- Check `.env` file has correct API key variable
- Ensure no extra spaces or quotes around the key
- Verify the key is valid and active

### "Provider not supported" Error
- Check `AI_PROVIDER` value is one of: openai, anthropic, google, emergent
- Ensure correct spelling and lowercase

### "Model not found" Error
- Verify model name is correct for your provider
- Check if you have access to the specified model
- Try default models if custom ones fail

### Rate Limit Errors
- Check your API usage limits
- Consider upgrading your API plan
- Switch to a provider with higher limits

## 📊 Performance Comparison

### Response Quality for Nepal Legal Queries

| Provider | Legal Accuracy | Nepal Law Knowledge | Practical Solutions | Overall |
|----------|----------------|-------------------|-------------------|---------|
| GPT-4 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Claude-3 Sonnet | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Gemini Pro | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| GPT-3.5 Turbo | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🎯 Recommendations

### **For Production Use**
- **Primary**: OpenAI GPT-4 (best balance of quality and reliability)
- **Backup**: Anthropic Claude-3 Sonnet (excellent analysis capabilities)

### **For Development/Testing**
- **Budget**: Google Gemini Pro (free tier available)
- **Performance**: OpenAI GPT-3.5 Turbo (fast and cost-effective)

### **For Specialized Legal Use**
- **Expert**: Emergent LLM (if available, specialized for legal)
- **Analysis**: Anthropic Claude-3 Opus (best for complex reasoning)

## 🔐 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate keys regularly** (monthly recommended)
4. **Monitor usage** to detect unauthorized access
5. **Set usage limits** to prevent unexpected charges
6. **Use separate keys** for development and production

---

**🏛️ Choose the AI provider that best fits your needs and budget. All providers work seamlessly with the Nepal Law Assistant platform!**