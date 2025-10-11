"""
Nepal Law Assistant Backend - No Database Version
Simplified version that works without MongoDB
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Nepal Law Assistant API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import AI provider
try:
    from ai_providers import generate_ai_response
    AI_AVAILABLE = True
    logger.info("✅ AI providers loaded successfully")
except Exception as e:
    logger.warning(f"⚠️  AI providers not available: {e}")
    AI_AVAILABLE = False

# Data models
class LegalQueryCreate(BaseModel):
    query_text: str
    user_session: Optional[str] = None

class LegalResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    response_text: str
    relevant_laws: List[str] = []
    sources: List[str] = []
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LegalQuery(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query_text: str
    user_session: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LegalAnalysis(BaseModel):
    query: LegalQuery
    response: LegalResponse

# Routes
@app.get("/")
async def root():
    return {"message": "Nepal Law Assistant API", "status": "running", "database": "disabled"}

@app.get("/api/")
async def api_root():
    return {"message": "Nepal Law Assistant API", "version": "1.0.0", "ai_available": AI_AVAILABLE}

@app.post("/api/analyze-legal-problem", response_model=LegalAnalysis)
async def analyze_legal_problem(input: LegalQueryCreate):
    """Analyze legal problems using AI"""
    try:
        if not AI_AVAILABLE:
            raise HTTPException(status_code=500, detail="AI provider not configured")
        
        # Create legal query record
        user_session = input.user_session or str(uuid.uuid4())
        query = LegalQuery(
            query_text=input.query_text,
            user_session=user_session
        )
        
        # System message for Nepal legal analysis
        system_message = """You are an expert Nepal legal assistant with LL.B qualification. Your role is to:

1. Analyze legal problems and provide relevant Nepal law guidance
2. Reference specific Nepal acts, laws, and regulations when applicable
3. Provide practical legal advice within Nepal's legal framework
4. Always mention relevant sources and act names
5. Format your response with clear sections: Problem Analysis, Relevant Laws, Recommendations, and Sources

IMPORTANT: Focus on Nepal's legal system, acts, and regulations. Be specific about law references and provide actionable guidance."""
        
        user_message = f"Legal Problem: {input.query_text}\n\nPlease analyze this legal issue according to Nepal law and provide relevant legal guidance with specific law references."
        
        # Get AI response
        ai_response = await generate_ai_response(system_message, user_message)
        
        # Parse response for laws and sources
        import re
        relevant_laws = []
        law_patterns = [
            r'Constitution of Nepal[^\n]*',
            r'Civil Code[^\n]*',
            r'Criminal Code[^\n]*',
            r'Act [0-9]{4}[^\n]*',
            r'Nepal[\s\w]*Act[^\n]*',
            r'Muluki[\s\w]*[^\n]*'
        ]
        
        for pattern in law_patterns:
            matches = re.findall(pattern, ai_response, re.IGNORECASE)
            relevant_laws.extend(matches)
        
        relevant_laws = list(set(relevant_laws))[:10]
        
        # Create response
        response = LegalResponse(
            query_id=query.id,
            response_text=ai_response,
            relevant_laws=relevant_laws,
            sources=[
                "Constitution of Nepal 2072",
                "Nepal Law Commission",
                "Supreme Court of Nepal",
                "Ministry of Law, Justice and Parliamentary Affairs"
            ]
        )
        
        return LegalAnalysis(query=query, response=response)
        
    except Exception as e:
        logger.error(f"Error analyzing legal problem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing legal problem: {str(e)}")

@app.post("/api/solve-problem")
async def solve_problem(request: dict):
    """Simple problem solving endpoint"""
    try:
        if not AI_AVAILABLE:
            raise HTTPException(status_code=500, detail="AI provider not configured")
        
        problem_text = request.get('problem_text', '')
        if not problem_text:
            raise HTTPException(status_code=400, detail="Problem text is required")
        
        system_message = """You are Nepal's most experienced legal problem solver. Provide ACTIONABLE SOLUTIONS with:
1. Immediate actions to take
2. Step-by-step solution
3. Required documents
4. Timeline and costs
5. Success probability
Focus on practical solutions for Nepal's legal system."""
        
        user_message = f"PROBLEM: {problem_text}\n\nProvide a complete, actionable solution for Nepal."
        
        ai_response = await generate_ai_response(system_message, user_message)
        
        return {
            "problem_type": "general",
            "urgency_level": "medium",
            "immediate_actions": ["Consult the detailed analysis below"],
            "step_by_step_solution": [{"step": 1, "description": ai_response}],
            "success_probability": 75,
            "analysis": ai_response
        }
        
    except Exception as e:
        logger.error(f"Error solving problem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error solving problem: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_available": AI_AVAILABLE,
        "database": "disabled",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)