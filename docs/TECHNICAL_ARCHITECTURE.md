# 🏗️ Technical Architecture - Nepal Law Assistant

**For Developers & Technical Team**

This document provides a detailed technical overview of the Nepal Law Assistant architecture, design decisions, and implementation details.

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Technology Stack](#technology-stack)
4. [Backend Architecture](#backend-architecture)
5. [Frontend Architecture](#frontend-architecture)
6. [API Documentation](#api-documentation)
7. [Data Flow](#data-flow)
8. [Security Implementation](#security-implementation)
9. [Deployment Architecture](#deployment-architecture)
10. [Performance Considerations](#performance-considerations)

---

## 🎯 System Overview

### Purpose
AI-powered legal assistance platform specialized for Nepal law, providing real-time legal guidance through streaming responses.

### Key Features
- Real-time streaming AI responses
- Nepal law specialization
- Query history (local storage)
- Mobile-responsive design
- Rate limiting and security
- Multi-AI provider support (currently Google Gemini)

### Architecture Pattern
**Microservices-style separation:**
- Backend: RESTful API server
- Frontend: Single Page Application (SPA)
- AI: External service (Google Gemini)

---

## 🏛️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Browser    │  │    Mobile    │  │    Tablet    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND LAYER                         │
│                    (Vercel Hosting)                         │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              React SPA (App.js)                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │ │
│  │  │  UI Layer   │  │ State Mgmt  │  │ Local Store │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ REST API (HTTPS)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND LAYER                          │
│                   (Railway Hosting)                         │
│  ┌───────────────────────────────────────────────────────┐ │
│  │         FastAPI Server (server_working.py)            │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │ │
│  │  │   Routing    │  │ Rate Limiter │  │    CORS    │ │ │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │ │
│  │  ┌──────────────┐  ┌──────────────┐                 │ │
│  │  │Legal Logic   │  │ AI Provider  │                 │ │
│  │  │(prompts)     │  │  Interface   │                 │ │
│  │  └──────────────┘  └──────────────┘                 │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ API Call (HTTPS)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       AI LAYER                              │
│                  (Google Cloud)                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │           Google Gemini 2.5 Flash API                 │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │ │
│  │  │   NLP Model  │  │   Streaming  │  │  Response  │ │ │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Core language |
| FastAPI | 0.104+ | Web framework |
| Uvicorn | 0.24+ | ASGI server |
| Google Generative AI | 0.3+ | AI integration |
| python-dotenv | 1.0+ | Environment management |
| Pydantic | 2.0+ | Data validation |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2+ | UI framework |
| JavaScript (ES6+) | - | Core language |
| CSS3 | - | Styling |
| Fetch API | - | HTTP client |
| LocalStorage API | - | Client-side storage |

### Infrastructure

| Service | Purpose | Tier |
|---------|---------|------|
| Railway | Backend hosting | Free/Hobby |
| Vercel | Frontend hosting | Free |
| Google Cloud | AI API | Pay-per-use |
| GitHub | Version control | Free |
| GitHub Actions | CI/CD | Free |

---

## 🔧 Backend Architecture

### File Structure

```
backend/
├── server_working.py       # Main FastAPI application
├── legal_knowledge.py     # AI prompts and legal logic
├── ai_providers.py        # AI provider abstraction layer
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (local)
├── .env.example          # Environment template
├── Procfile              # Railway deployment config
└── railway.toml          # Railway settings
```

### Core Components

#### 1. **FastAPI Application** (`server_working.py`)

**Responsibilities:**
- HTTP request handling
- CORS configuration
- Rate limiting
- Request validation
- Response streaming
- Error handling

**Key Endpoints:**
```python
POST /api/query              # Main legal query endpoint
GET  /api/health            # Health check
OPTIONS /*                  # CORS preflight
```

**Middleware Stack:**
```
Request → CORS → Rate Limiter → Route Handler → Response
```

#### 2. **Legal Knowledge Module** (`legal_knowledge.py`)

**Responsibilities:**
- System prompt management
- Legal context injection
- Response formatting rules
- Nepal law specialization

**Key Components:**
```python
SYSTEM_PROMPT              # Base AI instructions
NEPAL_LAW_CONTEXT         # Legal framework context
RESPONSE_FORMAT           # Structured response template
```

**Prompt Engineering Strategy:**
- User-centric language
- Structured response format
- Nepal law specialization
- Practical action steps
- Cost and timeline estimates

#### 3. **AI Provider Interface** (`ai_providers.py`)

**Responsibilities:**
- AI provider abstraction
- API key management
- Streaming response handling
- Error handling and retries

**Supported Providers:**
```python
class AIProvider:
    - Google Gemini (primary)
    - OpenAI (future)
    - Anthropic (future)
```

**Streaming Implementation:**
```python
async def stream_response(prompt: str):
    async for chunk in ai_client.generate_content_stream(prompt):
        yield chunk.text
```

### Request Flow

```
1. Client Request
   ↓
2. CORS Validation
   ↓
3. Rate Limit Check
   ↓
4. Request Validation (Pydantic)
   ↓
5. Prompt Construction (legal_knowledge.py)
   ↓
6. AI API Call (ai_providers.py)
   ↓
7. Stream Response Chunks
   ↓
8. Client Receives Streaming Response
```

### Data Models

```python
class LegalQuery(BaseModel):
    query: str
    session_id: Optional[str] = None
    context: Optional[Dict] = None

class LegalResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime
    model_used: str
```

---

## 🎨 Frontend Architecture

### File Structure

```
frontend/
├── src/
│   ├── App.js              # Main React component
│   └── App.css             # Styling
├── public/
│   ├── index.html          # HTML template
│   └── favicon.ico         # Site icon
├── package.json            # Dependencies
└── .env.template           # Environment template
```

### Component Architecture

```
App (Root Component)
├── State Management
│   ├── messages (array)
│   ├── input (string)
│   ├── isLoading (boolean)
│   └── sessionId (string)
├── UI Components
│   ├── Header
│   │   └── Logo (clickable refresh)
│   ├── ChatContainer
│   │   ├── MessageList
│   │   │   ├── UserMessage
│   │   │   └── AIMessage (streaming)
│   │   └── ScrollToBottom
│   └── InputArea
│       ├── TextArea (auto-resize)
│       ├── SendButton
│       └── NewChatButton
└── Utilities
    ├── LocalStorage (history)
    ├── StreamingHandler
    └── KeyboardHandlers
```

### State Management

**Local State (useState):**
```javascript
const [messages, setMessages] = useState([])
const [input, setInput] = useState('')
const [isLoading, setIsLoading] = useState(false)
const [sessionId, setSessionId] = useState(generateSessionId())
```

**Persistent State (localStorage):**
```javascript
localStorage.setItem('chatHistory', JSON.stringify(messages))
localStorage.getItem('chatHistory')
```

### Streaming Implementation

```javascript
const handleSubmit = async () => {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: input })
  })

  const reader = response.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    
    const chunk = decoder.decode(value)
    // Update UI with chunk
    setMessages(prev => updateLastMessage(prev, chunk))
  }
}
```

### User Interactions

| Action | Trigger | Behavior |
|--------|---------|----------|
| Submit Query | Enter key | Send message, start streaming |
| New Line | Shift+Enter | Add line break in textarea |
| New Chat | Button click | Clear messages, new session |
| Refresh | Logo click | Reload page |
| Auto-scroll | New message | Scroll to bottom |

---

## 📡 API Documentation

### Endpoint: POST /api/query

**Purpose:** Submit legal query and receive streaming AI response

**Request:**
```json
{
  "query": "What are my rights if my neighbor builds on my property?",
  "session_id": "uuid-v4-string",
  "context": {
    "previous_queries": []
  }
}
```

**Response:** Server-Sent Events (SSE) stream
```
data: {"chunk": "Based on Nepal law, "}
data: {"chunk": "you have several rights..."}
data: {"chunk": "\n\n**Immediate Next Step:**\n"}
...
data: {"done": true}
```

**Status Codes:**
- `200` - Success (streaming)
- `400` - Bad request (invalid input)
- `429` - Too many requests (rate limit)
- `500` - Server error
- `503` - AI service unavailable

**Rate Limiting:**
- 10 requests per minute per IP
- Header: `X-RateLimit-Remaining`

---

## 🔄 Data Flow

### Query Processing Flow

```
┌──────────────┐
│ User Input   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Frontend Validation                  │
│ - Non-empty check                    │
│ - Length validation                  │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ HTTP POST Request                    │
│ - Add session ID                     │
│ - Add context                        │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Backend: CORS Check                  │
│ - Verify origin                      │
│ - Check headers                      │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Backend: Rate Limit Check            │
│ - Check IP request count             │
│ - Return 429 if exceeded             │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Backend: Request Validation          │
│ - Pydantic model validation          │
│ - Type checking                      │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Prompt Construction                  │
│ - Add system prompt                  │
│ - Add Nepal law context              │
│ - Add user query                     │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ AI API Call (Google Gemini)          │
│ - Send prompt                        │
│ - Request streaming                  │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Stream Response Chunks               │
│ - Receive chunks                     │
│ - Forward to frontend                │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Frontend: Display Streaming          │
│ - Append chunks to message           │
│ - Auto-scroll                        │
│ - Save to localStorage               │
└──────────────────────────────────────┘
```

---

## 🔒 Security Implementation

### 1. **API Key Protection**

**Implementation:**
```python
# Environment variable only
api_key = os.getenv('GOOGLE_API_KEY')

# Never in code
# api_key = 'AIzaSy...'  ❌ NEVER DO THIS
```

**Storage:**
- Local: `.env` file (gitignored)
- Production: Platform environment variables

### 2. **CORS Configuration**

**Implementation:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://law-gpt.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
```

**Purpose:**
- Prevent unauthorized domains from accessing API
- Allow only trusted frontend origins

### 3. **Rate Limiting**

**Implementation:**
```python
@app.post("/api/query")
@limiter.limit("10/minute")
async def query_endpoint(request: Request):
    # Handle request
```

**Purpose:**
- Prevent API abuse
- Control costs
- Ensure fair usage

### 4. **Input Validation**

**Implementation:**
```python
class LegalQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=5000)
    session_id: Optional[str] = Field(None, regex=r'^[a-f0-9-]{36}$')
```

**Purpose:**
- Prevent injection attacks
- Ensure data integrity
- Validate data types

### 5. **Error Handling**

**Implementation:**
```python
try:
    response = await ai_provider.generate(prompt)
except Exception as e:
    logger.error(f"AI Error: {str(e)}")
    raise HTTPException(
        status_code=500,
        detail="AI service temporarily unavailable"
    )
```

**Purpose:**
- Don't expose internal errors
- Log for debugging
- Return user-friendly messages

---

## 🚀 Deployment Architecture

### Production Environment

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Repository                    │
│                  (Source of Truth)                      │
└────────────┬────────────────────────┬───────────────────┘
             │                        │
             │ Push to dev.deploy     │ Push to main
             ▼                        ▼
┌────────────────────────┐  ┌────────────────────────┐
│   Railway (Backend)    │  │   Vercel (Frontend)    │
│                        │  │                        │
│ 1. Detect changes      │  │ 1. Detect changes      │
│ 2. Install deps        │  │ 2. Install deps        │
│ 3. Run tests (future)  │  │ 3. Build React app     │
│ 4. Deploy server       │  │ 4. Deploy static files │
│ 5. Health check        │  │ 5. Invalidate CDN      │
└────────────────────────┘  └────────────────────────┘
             │                        │
             │ API Calls              │ User Requests
             ▼                        ▼
┌────────────────────────┐  ┌────────────────────────┐
│  Google Gemini API     │  │   End Users            │
└────────────────────────┘  └────────────────────────┘
```

### Environment Configuration

**Development:**
```env
GOOGLE_API_KEY=dev_key
ALLOWED_ORIGINS=http://localhost:3000
AI_MODEL=gemini-2.5-flash
PORT=8000
```

**Production:**
```env
GOOGLE_API_KEY=prod_key
ALLOWED_ORIGINS=https://law-gpt.vercel.app
AI_MODEL=gemini-2.5-flash
PORT=8000
```

### Deployment Process

**Backend (Railway):**
1. Push code to GitHub
2. Railway webhook triggered
3. Build process starts
4. Install Python dependencies
5. Start Uvicorn server
6. Health check passes
7. Traffic routed to new deployment

**Frontend (Vercel):**
1. Push code to GitHub
2. Vercel webhook triggered
3. Build process starts
4. Install npm dependencies
5. Run `npm run build`
6. Deploy to CDN
7. Invalidate cache
8. Traffic routed to new deployment

---

## ⚡ Performance Considerations

### Backend Optimization

**1. Async/Await Pattern:**
```python
async def query_endpoint(request: Request):
    # Non-blocking I/O
    response = await ai_provider.generate(prompt)
```

**2. Streaming Responses:**
- Reduces perceived latency
- Better user experience
- Lower memory usage

**3. Connection Pooling:**
```python
# Reuse HTTP connections
client = httpx.AsyncClient()
```

### Frontend Optimization

**1. Lazy Loading:**
```javascript
// Load components only when needed
const HeavyComponent = React.lazy(() => import('./Heavy'))
```

**2. Debouncing:**
```javascript
// Prevent excessive API calls
const debouncedSubmit = debounce(handleSubmit, 300)
```

**3. Local Storage:**
```javascript
// Cache chat history locally
localStorage.setItem('history', JSON.stringify(messages))
```

### AI API Optimization

**1. Model Selection:**
- Using `gemini-2.5-flash` (faster, cheaper)
- Not using `gemini-pro` (slower, expensive)

**2. Prompt Optimization:**
- Clear, concise prompts
- Structured output format
- Reduced token usage

**3. Caching (Future):**
```python
# Cache common queries
@lru_cache(maxsize=100)
def get_cached_response(query_hash):
    return cached_responses.get(query_hash)
```

---

## 📊 Monitoring & Logging

### Current Implementation

**Backend Logging:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Query received: {query[:50]}...")
logger.error(f"AI Error: {str(e)}")
```

**Frontend Logging:**
```javascript
console.log('Query submitted:', query)
console.error('API Error:', error)
```

### Future Improvements

**1. Structured Logging:**
```python
logger.info("query_received", extra={
    "session_id": session_id,
    "query_length": len(query),
    "timestamp": datetime.now()
})
```

**2. Error Tracking:**
- Sentry integration
- Error aggregation
- Alert notifications

**3. Analytics:**
- Query patterns
- Response times
- User engagement
- Error rates

---

## 🔮 Future Architecture Considerations

### 1. **Database Integration**

**Proposed:** MongoDB Atlas

**Schema:**
```javascript
{
  session_id: String,
  user_id: String (future),
  queries: [{
    query: String,
    response: String,
    timestamp: Date,
    model_used: String
  }],
  created_at: Date,
  updated_at: Date
}
```

### 2. **Authentication System**

**Proposed:** JWT + OAuth

**Flow:**
```
User → OAuth Provider → JWT Token → Protected Routes
```

### 3. **Caching Layer**

**Proposed:** Redis

**Use Cases:**
- Common query responses
- Rate limiting counters
- Session data

### 4. **Load Balancing**

**Proposed:** Railway auto-scaling

**Configuration:**
```yaml
replicas: 2-10
cpu_threshold: 70%
memory_threshold: 80%
```

### 5. **CDN Integration**

**Current:** Vercel CDN (automatic)

**Future:** Cloudflare for additional features
- DDoS protection
- Advanced caching
- Analytics

---

## 📝 Development Guidelines

### Code Style

**Python (Backend):**
- PEP 8 compliance
- Type hints
- Docstrings for functions
- Async/await for I/O

**JavaScript (Frontend):**
- ES6+ features
- Functional components
- Hooks for state management
- PropTypes or TypeScript (future)

### Git Workflow

**Branches:**
- `main` - Production
- `dev.deploy` - Development
- `feature/*` - New features
- `fix/*` - Bug fixes

**Commit Messages:**
```
feat: Add user authentication
fix: Resolve CORS issue
docs: Update API documentation
refactor: Improve prompt structure
```

### Testing Strategy (Future)

**Backend:**
```python
# Unit tests
pytest tests/

# Integration tests
pytest tests/integration/

# Load tests
locust -f tests/load/
```

**Frontend:**
```javascript
// Unit tests
npm test

// E2E tests
npm run test:e2e
```

---

## 🆘 Troubleshooting Guide

### Common Issues

**1. CORS Errors**
- Check `ALLOWED_ORIGINS` in backend
- Verify frontend URL matches

**2. API Key Errors**
- Verify key in environment variables
- Check key is valid in Google Cloud Console

**3. Streaming Not Working**
- Check browser compatibility
- Verify response headers
- Check network tab in DevTools

**4. Deployment Failures**
- Check build logs
- Verify environment variables
- Check dependency versions

---

## 📚 Additional Resources

**Documentation:**
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Google Gemini API](https://ai.google.dev/docs)

**Tools:**
- [Postman](https://www.postman.com/) - API testing
- [React DevTools](https://react.dev/learn/react-developer-tools) - React debugging
- [Railway CLI](https://docs.railway.app/develop/cli) - Deployment management

---

**Document Version:** 1.0
**Last Updated:** October 23, 2025
**Maintained By:** Development Team
