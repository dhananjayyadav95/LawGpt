from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class LegalQuery(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query_text: str
    user_session: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LegalQueryCreate(BaseModel):
    query_text: str
    user_session: Optional[str] = None

class LegalResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query_id: str
    response_text: str
    relevant_laws: List[str] = []
    sources: List[str] = []
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LegalAnalysis(BaseModel):
    query: LegalQuery
    response: LegalResponse

# Helper function to prepare data for MongoDB
def prepare_for_mongo(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
    return data

# Helper function to parse data from MongoDB
def parse_from_mongo(item):
    if isinstance(item, dict):
        for key, value in item.items():
            if isinstance(value, str) and 'T' in value and ':' in value:
                try:
                    item[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                except:
                    pass
    return item

@api_router.get("/")
async def root():
    return {"message": "Nepal Law Assistant API"}

@api_router.post("/analyze-legal-problem", response_model=LegalAnalysis)
async def analyze_legal_problem(input: LegalQueryCreate):
    try:
        # Create legal query record
        user_session = input.user_session or str(uuid.uuid4())
        query = LegalQuery(
            query_text=input.query_text,
            user_session=user_session
        )
        
        # Store query in database
        query_dict = prepare_for_mongo(query.dict())
        await db.legal_queries.insert_one(query_dict)
        
        # Initialize LLM chat with Gemini 2.5 Pro for cost efficiency
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="LLM API key not configured")
        
        chat = LlmChat(
            api_key=api_key,
            session_id=user_session,
            system_message="""You are an expert Nepal legal assistant. Your role is to:

1. Analyze legal problems and provide relevant Nepal law guidance
2. Reference specific Nepal acts, laws, and regulations when applicable
3. Provide practical legal advice within Nepal's legal framework
4. Always mention relevant sources and act names
5. Format your response with clear sections: Problem Analysis, Relevant Laws, Recommendations, and Sources

IMPORTANT: Focus on Nepal's legal system, acts, and regulations. Be specific about law references and provide actionable guidance."""
        ).with_model("gemini", "gemini-2.5-pro")
        
        # Create user message with the legal problem
        user_message = UserMessage(
            text=f"Legal Problem: {input.query_text}\n\nPlease analyze this legal issue according to Nepal law and provide relevant legal guidance with specific law references."
        )
        
        # Get AI response
        ai_response = await chat.send_message(user_message)
        
        # Parse the response to extract laws and sources
        response_text = str(ai_response)
        
        # Simple parsing to extract potential law references and sources
        relevant_laws = []
        sources = []
        
        # Look for common Nepal law patterns
        import re
        law_patterns = [
            r'Constitution of Nepal[^\n]*',
            r'Civil Code[^\n]*',
            r'Criminal Code[^\n]*',
            r'Act [0-9]{4}[^\n]*',
            r'Nepal[\s\w]*Act[^\n]*',
            r'Muluki[\s\w]*[^\n]*'
        ]
        
        for pattern in law_patterns:
            matches = re.findall(pattern, response_text, re.IGNORECASE)
            relevant_laws.extend(matches)
        
        # Remove duplicates and limit to most relevant
        relevant_laws = list(set(relevant_laws))[:10]
        
        # Add some common Nepal law sources
        sources = [
            "Constitution of Nepal 2072",
            "Nepal Law Commission",
            "Ministry of Law, Justice and Parliamentary Affairs",
            "Supreme Court of Nepal"
        ]
        
        # Create response record
        response = LegalResponse(
            query_id=query.id,
            response_text=response_text,
            relevant_laws=relevant_laws,
            sources=sources
        )
        
        # Store response in database
        response_dict = prepare_for_mongo(response.dict())
        await db.legal_responses.insert_one(response_dict)
        
        return LegalAnalysis(query=query, response=response)
        
    except Exception as e:
        logger.error(f"Error analyzing legal problem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing legal problem: {str(e)}")

@api_router.get("/legal-history/{user_session}", response_model=List[LegalAnalysis])
async def get_legal_history(user_session: str):
    try:
        # Get queries for this session
        queries = await db.legal_queries.find({"user_session": user_session}).sort("timestamp", -1).to_list(100)
        
        history = []
        for query_doc in queries:
            query_doc = parse_from_mongo(query_doc)
            query = LegalQuery(**query_doc)
            
            # Get corresponding response
            response_doc = await db.legal_responses.find_one({"query_id": query.id})
            if response_doc:
                response_doc = parse_from_mongo(response_doc)
                response = LegalResponse(**response_doc)
                history.append(LegalAnalysis(query=query, response=response))
        
        return history
        
    except Exception as e:
        logger.error(f"Error getting legal history: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving legal history")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
