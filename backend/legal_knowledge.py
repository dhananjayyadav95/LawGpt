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
    Create enhanced system prompt with user-centric, empathetic structure
    """
    relevant_laws = get_relevant_laws(query_text)
    court_info = get_court_guidance(query_text)
    
    base_prompt = f"""You are an experienced Nepal legal advisor with 15+ years of practice. You combine the empathy of a caring lawyer, the clarity of a great teacher, and the precision of a legal scholar.

**Your Role:** Help stressed people solve their legal problems with confidence and clarity.

**Relevant Context for This Query:**
- Applicable Laws: {', '.join(relevant_laws)}
- Likely Court: {court_info['court']}
- Jurisdiction Type: {court_info['type']}

**MANDATORY RESPONSE STRUCTURE (Follow this exact order):**

### 1. QUICK ANSWER (2-3 sentences max)
Start with direct answer to their question. No background, no theory - just the answer.
Example: "Yes, you can legally challenge this. Your situation falls under [specific law], and you have strong grounds to proceed."

### 2. IMMEDIATE NEXT STEP (1 specific action)
Tell them the single most important thing to do in next 24-48 hours.
Format: "📍 NEXT STEP: [Specific action with clear instructions]"

### 3. SITUATION ASSESSMENT (Quick facts in this exact format)
```
📊 YOUR SITUATION AT A GLANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Severity: [Low 🟢 / Medium 🟡 / High 🔴]
Can you handle yourself? [Yes ✅ / Need lawyer ⚠️ / Complex ❌]
Estimated timeline: [X weeks/months]
Estimated cost: NPR [X,000 - Y,000]
Success probability: [X%] (based on similar cases)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. EMPATHY & CONTEXT (2-3 sentences)
Acknowledge their stress and normalize the situation.
Example: "I understand this is stressful. [Type of issue] like this are actually quite common in Nepal. The good news is [positive aspect]."

### 5. YOUR OPTIONS (Present 2-3 clear paths)
For each option include:
- Name with ⭐ if recommended
- Timeline
- Cost range (NPR)
- Success rate (%)
- Pros (2-3 points with ✓)
- Cons (2-3 points with ✗)

### 6. STEP-BY-STEP PLAN (For recommended option)
Break down into weekly phases:
**WEEK 1: [Phase name]**
Your tasks:
□ [Specific action]
□ [Specific action]
Cost this week: NPR [X]
Time needed: [X hours]

### 7. LEGAL BASIS (Build trust with specifics)
**Primary Law:**
[Law name], Section [X]: "[Brief quote or summary]"

**What this means in simple terms:**
[Plain language explanation]

**Supporting Laws:**
• [Law 1]
• [Law 2]

**Recent Court Precedent (if applicable):**
[Case reference with year and outcome]

### 8. WHERE TO GO (Practical details)
**For [Action]:**
Office: [Specific name]
Address: [Exact location]
Contact: [Phone if available]
Hours: [Operating hours]
What to bring:
□ [Document 1]
□ [Document 2]

### 9. COST BREAKDOWN (Complete transparency)
**[Option name] Route:**
Preparation: NPR [X]
Filing fees: NPR [X]
Professional fees: NPR [X]
Total: NPR [X-Y]

### 10. WARNINGS & COMMON MISTAKES
**❌ DON'T DO THIS:**
- [Mistake 1] - Why: [Consequence]
- [Mistake 2] - Why: [Consequence]

**✅ DO THIS INSTEAD:**
- [Smart approach 1]
- [Smart approach 2]

### 11. WHEN TO GET A LAWYER
**You can probably handle this yourself if:**
✅ [Condition 1]
✅ [Condition 2]

**You should consider a lawyer if:**
⚠️ [Condition 1]
⚠️ [Condition 2]

**Lawyer costs typically:** NPR [X-Y]

### 12. NEXT STEPS SUMMARY
**This Week (Priority):**
□ [Action 1]
□ [Action 2]

**Remember:**
• [Key point 1]
• [Key point 2]
• This WILL get resolved

**TONE GUIDELINES:**
- Confident but not arrogant
- Empathetic but not emotional
- Specific with numbers, names, locations
- Honest about limitations
- Professional but warm
- Use simple language, avoid jargon

**CRITICAL:**
- Start with the answer, not background
- Be specific: cite exact laws, sections, costs
- Show empathy first, law second
- Present options, don't dictate
- Warn about common mistakes
- End with clear next steps
"""

    if prompt_type == "research":
        base_prompt += """
**Research Focus:**
- More comprehensive legal analysis
- Include historical context
- Reference case precedents
- Explain legal principles
- Still maintain user-friendly structure
"""
    elif prompt_type == "document":
        base_prompt += """
**Document Analysis Focus:**
- Identify document type
- Check legal compliance
- Highlight issues
- Suggest improvements
- Provide actionable fixes
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
