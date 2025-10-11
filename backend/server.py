from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
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
from ai_providers import get_ai_provider, generate_ai_response
import PyPDF2
import docx
import io
import base64
# OCR imports - handle gracefully if not installed
try:
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter
    import cv2
    import numpy as np
    import easyocr
    from pdf2image import convert_from_bytes
    OCR_AVAILABLE = True
except ImportError as e:
    logger.warning(f"OCR dependencies not available: {e}")
    OCR_AVAILABLE = False
    # Create dummy classes to prevent errors
    class Image:
        @staticmethod
        def open(*args, **kwargs):
            raise HTTPException(status_code=500, detail="OCR not available - install pytesseract, opencv-python, easyocr")
    class pytesseract:
        @staticmethod
        def image_to_string(*args, **kwargs):
            raise HTTPException(status_code=500, detail="OCR not available")
import json
from typing import Dict, Any
from official_documents import get_official_documents, search_forms

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

class DocumentUpload(BaseModel):
    filename: str
    content: str
    file_type: str
    user_session: Optional[str] = None

class DocumentAnalysis(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    file_type: str
    extracted_text: str
    analysis: str
    relevant_laws: List[str] = []
    legal_issues: List[str] = []
    recommendations: List[str] = []
    user_session: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProblemSolution(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    problem_type: str
    urgency_level: str  # critical, high, medium, low
    immediate_actions: List[str] = []
    step_by_step_solution: List[Dict[str, Any]] = []
    required_documents: List[str] = []
    official_forms: List[Dict[str, str]] = []
    similar_cases: List[Dict[str, Any]] = []
    timeline: Dict[str, str] = {}
    cost_estimate: Dict[str, Any] = {}
    success_probability: int = 0  # 0-100
    warnings: List[str] = []
    when_to_seek_lawyer: str = ""
    user_session: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CaseStudy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    case_title: str
    problem_description: str
    solution_applied: str
    outcome: str
    timeline: str
    cost_involved: str
    lessons_learned: List[str] = []
    document_type: str
    success_rating: int  # 1-5
    location: str = "Nepal"
    year: int
    tags: List[str] = []

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

# Document processing functions
def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

def extract_text_from_docx(file_content: bytes) -> str:
    try:
        doc = docx.Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading DOCX: {str(e)}")

def extract_text_from_txt(file_content: bytes) -> str:
    try:
        return file_content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return file_content.decode('latin-1')
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading text file: {str(e)}")

# Advanced Image Processing Functions
def preprocess_image_for_ocr(image):
    """Advanced image preprocessing for better OCR accuracy"""
    if not OCR_AVAILABLE:
        raise HTTPException(status_code=500, detail="OCR not available - install required packages")
    
    try:
        # Convert to numpy array for OpenCV processing
        img_array = np.array(image)
        
        # Convert to grayscale if not already
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Noise reduction
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # Adaptive thresholding for better text extraction
        binary = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Morphological operations to clean up
        kernel = np.ones((1,1), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return Image.fromarray(cleaned)
    except Exception as e:
        logger.warning(f"Image preprocessing failed: {e}, using original image")
        return image

def extract_text_from_image_advanced(file_content: bytes, filename: str) -> Dict[str, Any]:
    """Advanced OCR with multiple engines and confidence scoring"""
    if not OCR_AVAILABLE:
        raise HTTPException(status_code=500, detail="OCR functionality not available. Install: pip install pytesseract opencv-python easyocr")
    
    try:
        # Load image
        image = Image.open(io.BytesIO(file_content))
        
        # Preprocess image
        processed_image = preprocess_image_for_ocr(image)
        
        # Initialize OCR engines
        results = {}
        
        # Method 1: Tesseract OCR (supports Nepali)
        try:
            # English + Nepali
            tesseract_text = pytesseract.image_to_string(processed_image, lang='eng+nep')
            tesseract_confidence = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT)
            avg_confidence = np.mean([int(conf) for conf in tesseract_confidence['conf'] if int(conf) > 0])
            
            results['tesseract'] = {
                'text': tesseract_text,
                'confidence': avg_confidence,
                'language': 'eng+nep'
            }
        except Exception as e:
            logger.warning(f"Tesseract OCR failed: {e}")
        
        # Method 2: EasyOCR (better for handwritten text)
        try:
            reader = easyocr.Reader(['en', 'ne'])  # English and Nepali
            easyocr_results = reader.readtext(np.array(processed_image))
            
            easyocr_text = ' '.join([result[1] for result in easyocr_results])
            easyocr_confidence = np.mean([result[2] for result in easyocr_results]) * 100
            
            results['easyocr'] = {
                'text': easyocr_text,
                'confidence': easyocr_confidence,
                'language': 'en+ne'
            }
        except Exception as e:
            logger.warning(f"EasyOCR failed: {e}")
        
        # Choose best result based on confidence and text length
        best_result = None
        best_score = 0
        
        for engine, result in results.items():
            # Score based on confidence and text length
            score = result['confidence'] * (len(result['text'].strip()) / 100)
            if score > best_score and len(result['text'].strip()) > 10:
                best_score = score
                best_result = result
                best_result['engine'] = engine
        
        if not best_result:
            # Fallback to any available result
            best_result = list(results.values())[0] if results else {
                'text': '', 'confidence': 0, 'engine': 'none'
            }
        
        # Document type detection
        document_type = detect_document_type(best_result['text'])
        
        return {
            'extracted_text': best_result['text'],
            'confidence': best_result.get('confidence', 0),
            'engine_used': best_result.get('engine', 'unknown'),
            'document_type': document_type,
            'all_results': results
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

def detect_document_type(text: str) -> str:
    """Detect the type of legal document based on content"""
    text_lower = text.lower()
    
    # Document type patterns
    patterns = {
        'court_notice': ['court', 'summons', 'hearing', 'case', 'plaintiff', 'defendant'],
        'tax_notice': ['tax', 'revenue', 'municipality', 'ward', 'payment', 'due'],
        'legal_notice': ['legal notice', 'advocate', 'lawyer', 'demand', 'breach'],
        'employment_letter': ['employment', 'termination', 'salary', 'employee', 'resignation'],
        'property_document': ['property', 'land', 'ownership', 'deed', 'registration'],
        'government_notice': ['government', 'ministry', 'department', 'license', 'permit'],
        'contract': ['agreement', 'contract', 'party', 'terms', 'conditions'],
        'complaint': ['complaint', 'grievance', 'police', 'fir', 'incident']
    }
    
    # Score each document type
    scores = {}
    for doc_type, keywords in patterns.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            scores[doc_type] = score
    
    # Return the highest scoring type
    if scores:
        return max(scores, key=scores.get)
    else:
        return 'unknown_document'

def extract_text_from_pdf_with_ocr(file_content: bytes) -> str:
    """Extract text from PDF with OCR fallback for scanned documents"""
    try:
        # First try regular PDF text extraction
        regular_text = extract_text_from_pdf(file_content)
        
        # If we get substantial text, use it
        if len(regular_text.strip()) > 100:
            return regular_text
        
        # Otherwise, use OCR on PDF pages
        logger.info("PDF appears to be scanned, using OCR...")
        images = convert_from_bytes(file_content)
        
        all_text = []
        for i, image in enumerate(images):
            try:
                ocr_result = extract_text_from_image_advanced(
                    io.BytesIO(image.tobytes()), f"pdf_page_{i}"
                )
                all_text.append(ocr_result['extracted_text'])
            except Exception as e:
                logger.warning(f"OCR failed for PDF page {i}: {e}")
        
        return '\n\n'.join(all_text)
        
    except Exception as e:
        logger.error(f"PDF OCR processing failed: {e}")
        return extract_text_from_pdf(file_content)  # Fallback to regular extraction

async def analyze_document_with_ai(text: str, filename: str, user_session: str) -> dict:
    """Analyze document content using AI for legal insights"""
    try:
        system_message = """You are an expert Nepal legal document analyzer with LL.B qualification. Your role is to:

1. Analyze legal documents and identify key legal issues
2. Reference specific Nepal laws, acts, and regulations that apply
3. Provide practical legal recommendations and next steps
4. Identify potential legal risks or opportunities
5. Suggest which legal procedures or remedies are available

IMPORTANT: Focus on Nepal's legal system. Be specific about law references and provide actionable guidance.

Format your response with clear sections:
- Document Summary
- Legal Issues Identified  
- Applicable Nepal Laws
- Recommendations & Next Steps
- Potential Risks/Considerations"""
        
        user_message = f"Document: {filename}\n\nContent:\n{text[:4000]}...\n\nPlease analyze this document according to Nepal law and provide comprehensive legal guidance."
        
        # Get AI response using configured provider
        response_text = await generate_ai_response(system_message, user_message)
        
        # Extract structured information
        import re
        
        # Extract legal issues
        legal_issues = []
        issues_match = re.search(r'Legal Issues?[:\s]*(.*?)(?=Applicable|Recommendations|$)', response_text, re.DOTALL | re.IGNORECASE)
        if issues_match:
            issues_text = issues_match.group(1)
            legal_issues = [issue.strip() for issue in re.findall(r'[-•]\s*([^\n]+)', issues_text)]
        
        # Extract recommendations
        recommendations = []
        rec_match = re.search(r'Recommendations?[:\s]*(.*?)(?=Potential|Risks|$)', response_text, re.DOTALL | re.IGNORECASE)
        if rec_match:
            rec_text = rec_match.group(1)
            recommendations = [rec.strip() for rec in re.findall(r'[-•]\s*([^\n]+)', rec_text)]
        
        # Extract relevant laws
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
            matches = re.findall(pattern, response_text, re.IGNORECASE)
            relevant_laws.extend(matches)
        
        relevant_laws = list(set(relevant_laws))[:10]
        
        return {
            'analysis': response_text,
            'legal_issues': legal_issues[:10],
            'recommendations': recommendations[:10],
            'relevant_laws': relevant_laws
        }
        
    except Exception as e:
        logger.error(f"Error in AI document analysis: {str(e)}")
        return {
            'analysis': f"Document uploaded successfully but AI analysis failed: {str(e)}",
            'legal_issues': [],
            'recommendations': [],
            'relevant_laws': []
        }

async def create_problem_solution(problem_text: str, document_type: str, user_session: str) -> ProblemSolution:
    """Advanced AI-powered problem solving engine"""
    try:
        system_message = f"""You are Nepal's most experienced legal problem solver with 20+ years of practical experience. Your job is to provide ACTIONABLE SOLUTIONS, not just legal information.

CRITICAL INSTRUCTIONS:
1. Analyze the problem and provide IMMEDIATE actionable steps
2. Create a complete step-by-step solution roadmap with specific timelines
3. Identify urgency level (critical/high/medium/low) based on deadlines and consequences
4. List exact documents needed with specific names and sources
5. Provide official government forms with direct links/names
6. Reference real case examples of how people solved similar problems
7. Estimate realistic costs and timeframes
8. Calculate success probability based on Nepal legal system
9. Warn about potential pitfalls and mistakes to avoid
10. Clearly state when professional legal help is absolutely necessary

RESPONSE FORMAT (JSON-like structure):
- Problem Type: [specific category]
- Urgency Level: [critical/high/medium/low with reasoning]
- Immediate Actions: [what to do in next 24-48 hours]
- Step-by-Step Solution: [numbered steps with timeline for each]
- Required Documents: [exact document names and where to get them]
- Official Forms: [government forms with office names]
- Timeline: [realistic timeframe for resolution]
- Cost Estimate: [breakdown of expected costs]
- Success Probability: [percentage with reasoning]
- Warnings: [critical mistakes to avoid]
- When to Seek Lawyer: [specific conditions requiring legal help]

Document Type Detected: {document_type}
Focus on practical solutions that work in Nepal's system."""
        
        user_message = f"PROBLEM TO SOLVE:\n{problem_text}\n\nProvide a complete, actionable solution with specific steps, timelines, and practical guidance for Nepal."
        
        # Get AI response using configured provider
        response_text = await generate_ai_response(system_message, user_message)
        
        # Parse the structured response
        solution_data = parse_solution_response(response_text, document_type)
        
        # Get similar cases from database
        similar_cases = await get_similar_cases(document_type, problem_text)
        
        # Get official documents and forms
        official_docs = get_official_documents(document_type)
        
        # Create solution object
        solution = ProblemSolution(
            problem_type=solution_data.get('problem_type', document_type),
            urgency_level=solution_data.get('urgency_level', 'medium'),
            immediate_actions=solution_data.get('immediate_actions', []),
            step_by_step_solution=solution_data.get('step_by_step_solution', []),
            required_documents=solution_data.get('required_documents', []),
            official_forms=official_docs.get('forms', []),
            similar_cases=similar_cases,
            timeline=solution_data.get('timeline', {}),
            cost_estimate=solution_data.get('cost_estimate', {}),
            success_probability=solution_data.get('success_probability', 70),
            warnings=solution_data.get('warnings', []),
            when_to_seek_lawyer=solution_data.get('when_to_seek_lawyer', ''),
            user_session=user_session
        )
        
        return solution
        
    except Exception as e:
        logger.error(f"Error creating problem solution: {str(e)}")
        # Return basic solution as fallback
        return ProblemSolution(
            problem_type=document_type,
            urgency_level='medium',
            immediate_actions=['Consult with a legal professional for guidance'],
            user_session=user_session
        )

def parse_solution_response(response_text: str, document_type: str) -> Dict[str, Any]:
    """Parse AI response into structured solution data"""
    import re
    
    solution_data = {}
    
    # Extract urgency level
    urgency_match = re.search(r'urgency[:\s]*([a-zA-Z]+)', response_text, re.IGNORECASE)
    if urgency_match:
        solution_data['urgency_level'] = urgency_match.group(1).lower()
    
    # Extract immediate actions
    immediate_actions = []
    immediate_section = re.search(r'immediate actions?[:\s]*(.*?)(?=step|required|timeline|$)', response_text, re.DOTALL | re.IGNORECASE)
    if immediate_section:
        actions_text = immediate_section.group(1)
        immediate_actions = [action.strip() for action in re.findall(r'[-•]\s*([^\n]+)', actions_text)]
    
    solution_data['immediate_actions'] = immediate_actions[:5]
    
    # Extract step-by-step solution
    steps = []
    steps_section = re.search(r'step[s\-\s]*by[s\-\s]*step[:\s]*(.*?)(?=required|timeline|cost|$)', response_text, re.DOTALL | re.IGNORECASE)
    if steps_section:
        steps_text = steps_section.group(1)
        step_matches = re.findall(r'(\d+)[.\s]*([^\n]+)', steps_text)
        for i, (num, desc) in enumerate(step_matches):
            steps.append({
                'step': int(num),
                'description': desc.strip(),
                'timeline': f'{i+1}-{i+3} days',
                'priority': 'high' if i < 2 else 'medium'
            })
    
    solution_data['step_by_step_solution'] = steps
    
    # Extract required documents
    documents = []
    docs_section = re.search(r'required documents?[:\s]*(.*?)(?=official|timeline|cost|$)', response_text, re.DOTALL | re.IGNORECASE)
    if docs_section:
        docs_text = docs_section.group(1)
        documents = [doc.strip() for doc in re.findall(r'[-•]\s*([^\n]+)', docs_text)]
    
    solution_data['required_documents'] = documents[:10]
    
    # Extract success probability
    prob_match = re.search(r'success probability[:\s]*(\d+)', response_text, re.IGNORECASE)
    if prob_match:
        solution_data['success_probability'] = int(prob_match.group(1))
    
    # Extract warnings
    warnings = []
    warnings_section = re.search(r'warnings?[:\s]*(.*?)(?=when to seek|$)', response_text, re.DOTALL | re.IGNORECASE)
    if warnings_section:
        warnings_text = warnings_section.group(1)
        warnings = [warning.strip() for warning in re.findall(r'[-•]\s*([^\n]+)', warnings_text)]
    
    solution_data['warnings'] = warnings[:5]
    
    return solution_data

async def get_similar_cases(document_type: str, problem_text: str) -> List[Dict[str, Any]]:
    """Retrieve similar case studies from database"""
    try:
        # Search for similar cases in database
        similar_cases = await db.case_studies.find({
            "document_type": document_type,
            "success_rating": {"$gte": 3}
        }).limit(3).to_list(3)
        
        # If no cases found, return sample cases based on document type
        if not similar_cases:
            similar_cases = get_sample_cases(document_type)
        
        return similar_cases
        
    except Exception as e:
        logger.error(f"Error retrieving similar cases: {e}")
        return get_sample_cases(document_type)

def get_sample_cases(document_type: str) -> List[Dict[str, Any]]:
    """Return sample case studies based on document type"""
    sample_cases = {
        'tax_notice': [
            {
                'case_title': 'Property Tax Penalty Waiver Success',
                'problem_description': 'Received property tax notice with 50% penalty for late payment',
                'solution_applied': 'Filed penalty waiver application with municipality citing financial hardship',
                'outcome': 'Penalty reduced by 75%, paid only base tax amount',
                'timeline': '15 days',
                'cost_involved': 'Rs. 500 application fee + base tax',
                'success_rating': 4
            }
        ],
        'court_notice': [
            {
                'case_title': 'Court Summons Response Success',
                'problem_description': 'Received court summons for property dispute case',
                'solution_applied': 'Filed written statement within 15 days with supporting documents',
                'outcome': 'Case settled through court mediation, avoided lengthy trial',
                'timeline': '3 months',
                'cost_involved': 'Rs. 5,000 court fees + Rs. 15,000 lawyer fees',
                'success_rating': 5
            }
        ],
        'employment_letter': [
            {
                'case_title': 'Wrongful Termination Compensation',
                'problem_description': 'Terminated without proper notice period compensation',
                'solution_applied': 'Filed complaint with Labor Office with employment contract evidence',
                'outcome': 'Received 3 months salary as compensation plus reinstatement offer',
                'timeline': '45 days',
                'cost_involved': 'Rs. 1,000 filing fee',
                'success_rating': 4
            }
        ]
    }
    
    return sample_cases.get(document_type, [
        {
            'case_title': 'General Legal Issue Resolution',
            'problem_description': 'Similar legal problem resolved successfully',
            'solution_applied': 'Followed proper legal procedures and documentation',
            'outcome': 'Positive resolution achieved',
            'timeline': 'Varies by case complexity',
            'cost_involved': 'Depends on specific requirements',
            'success_rating': 3
        }
    ])

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
        
        # Use flexible AI provider system
        system_message = """You are an expert Nepal legal assistant. Your role is to:

1. Analyze legal problems and provide relevant Nepal law guidance
2. Reference specific Nepal acts, laws, and regulations when applicable
3. Provide practical legal advice within Nepal's legal framework
4. Always mention relevant sources and act names
5. Format your response with clear sections: Problem Analysis, Relevant Laws, Recommendations, and Sources

IMPORTANT: Focus on Nepal's legal system, acts, and regulations. Be specific about law references and provide actionable guidance."""
        
        user_message = f"Legal Problem: {input.query_text}\n\nPlease analyze this legal issue according to Nepal law and provide relevant legal guidance with specific law references."
        
        # Get AI response using configured provider
        ai_response = await generate_ai_response(system_message, user_message)
        
        # Parse the response to extract laws and sources
        response_text = ai_response
        
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

@api_router.post("/upload-document", response_model=DocumentAnalysis)
async def upload_document(file: UploadFile = File(...), user_session: Optional[str] = None):
    try:
        # Validate file type - now includes images
        allowed_types = [
            'application/pdf', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
            'text/plain',
            'image/jpeg',
            'image/jpg', 
            'image/png',
            'image/bmp',
            'image/tiff'
        ]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF, DOCX, TXT, or image files (JPG, PNG, BMP, TIFF).")
        
        # Read file content
        file_content = await file.read()
        
        # Extract text based on file type
        if file.content_type == 'application/pdf':
            extracted_text = extract_text_from_pdf_with_ocr(file_content)
            file_type = 'pdf'
            document_type = detect_document_type(extracted_text)
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            extracted_text = extract_text_from_docx(file_content)
            file_type = 'docx'
            document_type = detect_document_type(extracted_text)
        elif file.content_type == 'text/plain':
            extracted_text = extract_text_from_txt(file_content)
            file_type = 'txt'
            document_type = detect_document_type(extracted_text)
        else:  # Image files
            ocr_result = extract_text_from_image_advanced(file_content, file.filename)
            extracted_text = ocr_result['extracted_text']
            file_type = f"image_{file.content_type.split('/')[-1]}"
            document_type = ocr_result['document_type']
        
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text content found in the document")
        
        # Generate session if not provided
        session_id = user_session or str(uuid.uuid4())
        
        # Analyze document with AI
        ai_analysis = analyze_document_with_ai(extracted_text, file.filename, session_id)
        
        # Create document analysis record
        doc_analysis = DocumentAnalysis(
            filename=file.filename,
            file_type=file_type,
            extracted_text=extracted_text[:2000],  # Store first 2000 chars for reference
            analysis=ai_analysis['analysis'],
            relevant_laws=ai_analysis['relevant_laws'],
            legal_issues=ai_analysis['legal_issues'],
            recommendations=ai_analysis['recommendations'],
            user_session=session_id
        )
        
        # Store in database
        doc_dict = prepare_for_mongo(doc_analysis.dict())
        await db.document_analyses.insert_one(doc_dict)
        
        return doc_analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@api_router.post("/solve-problem", response_model=ProblemSolution)
async def solve_problem(request: dict):
    """Advanced problem solving endpoint with actionable solutions"""
    try:
        problem_text = request.get('problem_text', '')
        document_type = request.get('document_type', 'general')
        user_session = request.get('user_session', str(uuid.uuid4()))
        
        if not problem_text.strip():
            raise HTTPException(status_code=400, detail="Problem description is required")
        
        # Create comprehensive solution
        solution = create_problem_solution(problem_text, document_type, user_session)
        
        # Store solution in database
        solution_dict = prepare_for_mongo(solution.dict())
        await db.problem_solutions.insert_one(solution_dict)
        
        return solution
        
    except Exception as e:
        logger.error(f"Error solving problem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error solving problem: {str(e)}")

@api_router.post("/analyze-image-problem")
async def analyze_image_problem(file: UploadFile = File(...), user_session: Optional[str] = None):
    """Analyze uploaded image and provide complete problem solution"""
    try:
        # Validate image file
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Please upload an image file")
        
        # Read and process image
        file_content = await file.read()
        session_id = user_session or str(uuid.uuid4())
        
        # Extract text using advanced OCR
        ocr_result = extract_text_from_image_advanced(file_content, file.filename)
        extracted_text = ocr_result['extracted_text']
        document_type = ocr_result['document_type']
        
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract readable text from image")
        
        # Create comprehensive problem solution
        solution = create_problem_solution(extracted_text, document_type, session_id)
        
        # Enhanced response with OCR details
        response = {
            'ocr_result': ocr_result,
            'solution': solution,
            'extracted_text': extracted_text,
            'document_type': document_type,
            'confidence': ocr_result.get('confidence', 0)
        }
        
        # Store both OCR result and solution
        await db.image_analyses.insert_one(prepare_for_mongo(response))
        
        return response
        
    except Exception as e:
        logger.error(f"Error analyzing image problem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing image problem: {str(e)}")

@api_router.get("/official-forms/{document_type}")
async def get_official_forms(document_type: str):
    """Get official forms and procedures for a document type"""
    try:
        official_docs = get_official_documents(document_type)
        return {
            "document_type": document_type,
            "forms": official_docs.get('forms', []),
            "procedures": official_docs.get('procedures', []),
            "offices": official_docs.get('offices', [])
        }
    except Exception as e:
        logger.error(f"Error getting official forms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting official forms: {str(e)}")

@api_router.get("/search-forms")
async def search_official_forms(query: str):
    """Search for official forms based on query"""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Search query is required")
        
        results = search_forms(query)
        return {
            "query": query,
            "results": results,
            "total_found": len(results)
        }
    except Exception as e:
        logger.error(f"Error searching forms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching forms: {str(e)}")

@api_router.get("/case-studies/{document_type}")
async def get_case_studies_by_type(document_type: str, limit: int = 5):
    """Get case studies for a specific document type"""
    try:
        case_studies = await db.case_studies.find({
            "document_type": document_type
        }).sort("success_rating", -1).limit(limit).to_list(limit)
        
        return {
            "document_type": document_type,
            "case_studies": case_studies,
            "total_found": len(case_studies)
        }
    except Exception as e:
        logger.error(f"Error getting case studies: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting case studies: {str(e)}")

@api_router.get("/document-history/{user_session}", response_model=List[DocumentAnalysis])
async def get_document_history(user_session: str):
    try:
        # Get document analyses for this session
        docs = await db.document_analyses.find({"user_session": user_session}).sort("timestamp", -1).to_list(50)
        
        history = []
        for doc in docs:
            doc = parse_from_mongo(doc)
            history.append(DocumentAnalysis(**doc))
        
        return history
        
    except Exception as e:
        logger.error(f"Error getting document history: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving document history")

@api_router.post("/legal-research")
async def legal_research(query: LegalQueryCreate):
    """Enhanced legal research with case precedents and detailed analysis"""
    try:
        user_session = query.user_session or str(uuid.uuid4())
        
        system_message = """You are a senior Nepal legal expert with LL.B qualification and extensive experience in Nepal's legal system. Your role is to provide comprehensive legal research including:

1. Detailed analysis of the legal issue under Nepal law
2. Relevant case precedents from Nepal Supreme Court
3. Specific articles and sections from Nepal Constitution 2072
4. Applicable acts, codes, and regulations
5. Step-by-step legal procedure recommendations
6. Potential outcomes and legal remedies
7. Required documents and evidence
8. Timeline and costs involved

IMPORTANT: 
- Reference specific Nepal laws with exact article/section numbers
- Mention relevant Supreme Court decisions when applicable
- Provide practical, actionable legal guidance
- Include both civil and criminal law aspects if relevant
- Consider local court procedures and requirements

Format your response with clear sections:
- Legal Issue Analysis
- Applicable Laws & Regulations  
- Case Precedents (if any)
- Legal Procedure & Steps
- Required Documents
- Expected Timeline & Costs
- Potential Outcomes
- Recommendations"""
        
        user_message = f"Legal Research Query: {query.query_text}\n\nPlease provide comprehensive legal research and analysis according to Nepal law with case precedents and detailed procedural guidance."
        
        # Get AI response using configured provider
        response_text = await generate_ai_response(system_message, user_message)
        
        # Enhanced parsing for legal research
        import re
        
        relevant_laws = []
        case_precedents = []
        procedures = []
        
        # Extract Nepal laws with more patterns
        law_patterns = [
            r'Constitution of Nepal[^\n]*Article\s*\d+[^\n]*',
            r'Civil Code[^\n]*Section\s*\d+[^\n]*',
            r'Criminal Code[^\n]*Section\s*\d+[^\n]*',
            r'Nepal[\s\w]*Act[^\n]*\d{4}[^\n]*',
            r'Muluki[\s\w]*[^\n]*',
            r'Article\s*\d+[^\n]*Constitution[^\n]*',
            r'Section\s*\d+[^\n]*Code[^\n]*'
        ]
        
        for pattern in law_patterns:
            matches = re.findall(pattern, response_text, re.IGNORECASE)
            relevant_laws.extend(matches)
        
        # Extract case precedents
        case_patterns = [
            r'Supreme Court[^\n]*\d{4}[^\n]*',
            r'NKP\s*\d+[^\n]*',
            r'Nepal Law Journal[^\n]*',
            r'precedent[^\n]*case[^\n]*'
        ]
        
        for pattern in case_patterns:
            matches = re.findall(pattern, response_text, re.IGNORECASE)
            case_precedents.extend(matches)
        
        relevant_laws = list(set(relevant_laws))[:15]
        case_precedents = list(set(case_precedents))[:10]
        
        # Create enhanced legal query record
        legal_query = LegalQuery(
            query_text=query.query_text,
            user_session=user_session
        )
        
        # Store query in database
        query_dict = prepare_for_mongo(legal_query.dict())
        await db.legal_queries.insert_one(query_dict)
        
        # Create enhanced response
        enhanced_response = LegalResponse(
            query_id=legal_query.id,
            response_text=response_text,
            relevant_laws=relevant_laws,
            sources=[
                "Constitution of Nepal 2072",
                "Nepal Law Commission",
                "Supreme Court of Nepal",
                "Ministry of Law, Justice and Parliamentary Affairs",
                "Nepal Gazette",
                "Nepal Law Journal",
                "Local Court Procedures Manual"
            ]
        )
        
        # Store response in database
        response_dict = prepare_for_mongo(enhanced_response.dict())
        await db.legal_responses.insert_one(response_dict)
        
        return {
            "query": legal_query,
            "response": enhanced_response,
            "case_precedents": case_precedents,
            "research_type": "comprehensive"
        }
        
    except Exception as e:
        logger.error(f"Error in legal research: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in legal research: {str(e)}")

class DocumentTemplate(BaseModel):
    template_type: str
    title: str
    content: str
    instructions: str
    required_fields: List[str] = []

@api_router.post("/generate-legal-template")
async def generate_legal_template(request: dict):
    """Generate legal document templates based on user requirements"""
    try:
        template_type = request.get('template_type', '')
        case_details = request.get('case_details', '')
        user_session = request.get('user_session', str(uuid.uuid4()))
        
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="LLM API key not configured")
        
        chat = LlmChat(
            api_key=api_key,
            session_id=user_session,
            system_message="""You are a Nepal legal document expert. Generate professional legal document templates according to Nepal law format and requirements. Include:

1. Proper legal document structure and format
2. Required legal language and terminology in Nepal context
3. All necessary clauses and sections
4. Placeholder fields for customization
5. Legal requirements and filing procedures
6. Court format compliance

Available template types:
- Legal Notice
- Petition/Application
- Contract Agreement
- Power of Attorney
- Affidavit
- Complaint Application
- Appeal Application
- Bail Application
- Divorce Petition
- Property Transfer Deed

Format the template with:
- Proper heading and court details
- Legal formatting
- [PLACEHOLDER] fields for customization
- Required attachments list
- Filing instructions"""
        ).with_model("gemini", "gemini-2.5-pro")
        
        user_message = UserMessage(
            text=f"Generate a {template_type} template for Nepal legal system. Case details: {case_details}\n\nProvide a complete, professional template with proper legal formatting and all required sections."
        )
        
        ai_response = await chat.send_message(user_message)
        template_content = str(ai_response)
        
        # Extract required fields from template
        import re
        required_fields = re.findall(r'\[([A-Z_\s]+)\]', template_content)
        required_fields = list(set(required_fields))
        
        template = DocumentTemplate(
            template_type=template_type,
            title=f"{template_type} - Nepal Legal Template",
            content=template_content,
            instructions=f"Fill in all [PLACEHOLDER] fields with your specific information. Ensure all details are accurate before filing.",
            required_fields=required_fields
        )
        
        return template
        
    except Exception as e:
        logger.error(f"Error generating legal template: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating legal template: {str(e)}")

@api_router.get("/legal-templates")
async def get_legal_templates():
    """Get list of available legal document templates"""
    templates = [
        {"type": "legal_notice", "name": "Legal Notice", "description": "Formal legal notice for various purposes"},
        {"type": "petition", "name": "Court Petition", "description": "General court petition/application"},
        {"type": "contract", "name": "Contract Agreement", "description": "Legal contract between parties"},
        {"type": "power_of_attorney", "name": "Power of Attorney", "description": "Authorization document"},
        {"type": "affidavit", "name": "Affidavit", "description": "Sworn statement document"},
        {"type": "complaint", "name": "Complaint Application", "description": "Formal complaint to authorities"},
        {"type": "appeal", "name": "Appeal Application", "description": "Court appeal document"},
        {"type": "bail", "name": "Bail Application", "description": "Bail request document"},
        {"type": "divorce", "name": "Divorce Petition", "description": "Divorce proceedings document"},
        {"type": "property_transfer", "name": "Property Transfer Deed", "description": "Property ownership transfer"}
    ]
    return templates

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
