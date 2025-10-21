"""
Nepal Legal Knowledge Base and Enhanced Response System
Provides structured legal information and citation support
"""

# Nepal Legal Framework - Key Laws and Codes
NEPAL_LEGAL_FRAMEWORK = {
    "constitution": {
        "name": "Constitution of Nepal 2072 (2015)",
        "key_sections": {
            "fundamental_rights": "Articles 16-46",
            "directive_principles": "Articles 47-52",
            "federal_structure": "Articles 56-84",
            "judicial_system": "Articles 128-165"
        }
    },
    "civil_code": {
        "name": "Muluki Dewani Samhita 2074 (Civil Code 2017)",
        "areas": ["Property Rights", "Contract Law", "Family Law", "Tort Law", "Inheritance"]
    },
    "criminal_code": {
        "name": "Muluki Foujdari Samhita 2074 (Criminal Code 2017)",
        "areas": ["Criminal Offenses", "Criminal Procedure", "Evidence Law", "Sentencing"]
    },
    "specialized_laws": {
        "Company Act 2063": "Business and corporate matters",
        "Labor Act 2074": "Employment and labor relations",
        "Land Act 2021": "Property and land ownership",
        "Child Act 2075": "Child rights and protection",
        "Consumer Protection Act": "Consumer rights",
        "Foreign Employment Act": "Overseas employment"
    }
}

# Common Legal Topics and Relevant Laws
LEGAL_TOPIC_MAPPING = {
    "property": ["Land Act 2021", "Civil Code 2074", "Constitution Article 25"],
    "inheritance": ["Civil Code 2074 Part 3", "Constitution Article 38"],
    "employment": ["Labor Act 2074", "Social Security Act", "Constitution Article 33"],
    "contract": ["Contract Act 2056", "Civil Code 2074", "Constitution Article 20"],
    "criminal": ["Criminal Code 2074", "Criminal Procedure Code 2074", "Constitution Article 20"],
    "family": ["Civil Code 2074", "Marriage Registration Act", "Child Act 2075"],
    "business": ["Company Act 2063", "Contract Act 2056", "Arbitration Act 2055"],
    "tax": ["Income Tax Act 2058", "VAT Act 2052", "Constitution Article 59"],
    "consumer": ["Consumer Protection Act", "Civil Code 2074"],
    "land": ["Land Act 2021", "Land Revenue Act", "Constitution Article 25"]
}

# Court System Hierarchy
COURT_SYSTEM = {
    "supreme_court": {
        "name": "Supreme Court of Nepal",
        "jurisdiction": ["Constitutional", "Appellate", "Original", "Advisory"],
        "location": "Kathmandu"
    },
    "high_courts": {
        "count": 7,
        "provinces": ["Province 1", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim"],
        "jurisdiction": ["Appellate", "Original", "Administrative"]
    },
    "district_courts": {
        "count": 77,
        "jurisdiction": ["Civil", "Criminal", "Administrative"]
    }
}

def get_relevant_laws(query_text: str) -> list:
    """
    Identify relevant Nepal laws based on query keywords
    """
    query_lower = query_text.lower()
    relevant_laws = []
    
    # Check for topic matches
    for topic, laws in LEGAL_TOPIC_MAPPING.items():
        if topic in query_lower:
            relevant_laws.extend(laws)
    
    # Check for specific law mentions
    keywords = {
        "property": ["Land Act 2021", "Civil Code 2074"],
        "inherit": ["Civil Code 2074 Part 3"],
        "employ": ["Labor Act 2074"],
        "work": ["Labor Act 2074"],
        "contract": ["Contract Act 2056", "Civil Code 2074"],
        "crime": ["Criminal Code 2074"],
        "theft": ["Criminal Code 2074"],
        "assault": ["Criminal Code 2074"],
        "marriage": ["Civil Code 2074", "Marriage Registration Act"],
        "divorce": ["Civil Code 2074"],
        "child": ["Child Act 2075", "Civil Code 2074"],
        "company": ["Company Act 2063"],
        "business": ["Company Act 2063", "Contract Act 2056"],
        "tax": ["Income Tax Act 2058"],
        "consumer": ["Consumer Protection Act"],
        "land": ["Land Act 2021"]
    }
    
    for keyword, laws in keywords.items():
        if keyword in query_lower:
            relevant_laws.extend(laws)
    
    # Remove duplicates and return
    return list(set(relevant_laws)) if relevant_laws else ["Constitution of Nepal 2072", "Civil Code 2074"]

def get_court_guidance(query_text: str) -> dict:
    """
    Provide guidance on which court handles the matter
    """
    query_lower = query_text.lower()
    
    if any(word in query_lower for word in ["constitutional", "fundamental right", "constitution"]):
        return {
            "court": "Supreme Court of Nepal",
            "type": "Constitutional Jurisdiction",
            "process": "File writ petition under Article 133"
        }
    elif any(word in query_lower for word in ["appeal", "high court"]):
        return {
            "court": "High Court",
            "type": "Appellate Jurisdiction",
            "process": "File appeal within 35 days of district court decision"
        }
    else:
        return {
            "court": "District Court",
            "type": "Original Jurisdiction",
            "process": "File petition/complaint at local district court"
        }

def create_enhanced_prompt(query_text: str, prompt_type: str = "analysis") -> str:
    """
    Create enhanced system prompt with relevant legal context
    """
    relevant_laws = get_relevant_laws(query_text)
    court_info = get_court_guidance(query_text)
    
    base_prompt = f"""You are an expert Nepal legal assistant with LL.B qualification and 10+ years of experience in Nepal's legal system.

**Your Expertise:**
- Deep knowledge of Nepal Constitution 2072, Civil Code 2074, Criminal Code 2074
- Practical experience with Nepal court procedures
- Understanding of both English and Nepali legal terminology
- Familiarity with recent legal amendments and case precedents

**Relevant Laws for this Query:**
{chr(10).join(f'- {law}' for law in relevant_laws)}

**Court Jurisdiction:**
- Court: {court_info['court']}
- Type: {court_info['type']}
- Process: {court_info['process']}

**Response Requirements:**
1. **Legal Analysis**: Provide accurate analysis based on Nepal law
2. **Cite Specific Laws**: Reference exact acts, sections, and articles
3. **Practical Guidance**: Give actionable steps the person can take
4. **Court Procedures**: Explain relevant court processes
5. **Timeline**: Mention typical timeframes if applicable
6. **Documents Needed**: List required documents
7. **Warnings**: Highlight important legal considerations
8. **Professional Advice**: Recommend consulting a lawyer for complex matters

**Response Structure:**
Use clear headings and bullet points. Be specific, accurate, and practical.
Always cite the specific law, section, or article you're referencing.
"""

    if prompt_type == "research":
        base_prompt += """
**Research Focus:**
- Provide comprehensive legal research
- Include historical context and recent amendments
- Reference important case precedents if known
- Explain legal principles and their application
"""
    elif prompt_type == "document":
        base_prompt += """
**Document Analysis Focus:**
- Identify document type and legal significance
- Check for required clauses and legal compliance
- Highlight potential legal issues
- Suggest improvements or missing elements
"""
    
    return base_prompt

def format_legal_response(ai_response: str, relevant_laws: list) -> dict:
    """
    Structure the AI response with proper formatting and citations
    """
    return {
        "analysis": ai_response,
        "cited_laws": relevant_laws,
        "disclaimer": "This is general legal information. For specific legal advice, consult a qualified Nepal lawyer.",
        "sources": [
            "Constitution of Nepal 2072",
            "Nepal Legal Code 2074",
            "Supreme Court of Nepal Guidelines"
        ]
    }
