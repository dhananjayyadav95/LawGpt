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

# Official Nepal Legal Resources
OFFICIAL_LEGAL_RESOURCES = {
    "primary_sources": {
        "Nepal Law Commission": {
            "url": "http://www.lawcommission.gov.np",
            "description": "Official source for all Nepal laws and legal codes",
            "available": ["Constitution", "Civil Code", "Criminal Code", "All Acts"]
        },
        "Supreme Court of Nepal": {
            "url": "http://supremecourt.gov.np",
            "description": "Supreme Court decisions and case law",
            "available": ["Court decisions", "Legal precedents", "Case database"]
        },
        "Ministry of Law, Justice and Parliamentary Affairs": {
            "url": "http://www.moljpa.gov.np",
            "description": "Government legal policies and updates",
            "available": ["Legal updates", "Policy documents", "Legal notices"]
        },
        "Nepal Gazette": {
            "url": "http://www.nepalgazette.gov.np",
            "description": "Official government gazette for new laws",
            "available": ["New legislation", "Amendments", "Official notifications"]
        }
    },
    "legal_aid": {
        "Nepal Bar Association": {
            "contact": "01-4200000 (Kathmandu)",
            "description": "Professional lawyers association",
            "services": ["Lawyer referrals", "Legal guidance"]
        },
        "Legal Aid Committee": {
            "description": "Free legal aid for eligible citizens",
            "services": ["Free legal consultation", "Court representation"]
        }
    },
    "district_courts": {
        "portal": "http://districtcourt.gov.np",
        "description": "Access to all 77 district courts",
        "services": ["Case filing", "Case status", "Court schedules"]
    }
}

def get_verification_resources(relevant_laws: list) -> dict:
    """
    Generate verification resources based on relevant laws
    """
    resources = {
        "official_sources": [],
        "search_terms": [],
        "relevant_sections": []
    }
    
    # Add primary sources
    resources["official_sources"].append({
        "name": "Nepal Law Commission",
        "url": "http://www.lawcommission.gov.np",
        "description": "Verify all laws and legal codes here"
    })
    
    resources["official_sources"].append({
        "name": "Supreme Court of Nepal",
        "url": "http://supremecourt.gov.np",
        "description": "Check court decisions and precedents"
    })
    
    # Add search terms based on laws
    for law in relevant_laws:
        resources["search_terms"].append(law)
    
    return resources

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
    verification_resources = get_verification_resources(relevant_laws)
    
    base_prompt = f"""You are an experienced Nepal legal advisor with 15+ years of practice. You combine the empathy of a caring lawyer, the clarity of a great teacher, and the precision of a legal scholar.

**Your Role:** Help people solve their legal problems with confidence and clarity by providing verifiable, accurate legal information.

**Relevant Context for This Query:**
- Applicable Laws: {', '.join(relevant_laws)}
- Likely Court: {court_info['court']}
- Jurisdiction Type: {court_info['type']}

**Official Verification Sources:**
- Nepal Law Commission: http://www.lawcommission.gov.np
- Supreme Court: http://supremecourt.gov.np
- Ministry of Law: http://www.moljpa.gov.np

**MANDATORY RESPONSE STRUCTURE (Follow this exact order):**

### 1. DIRECT ANSWER (What user needs to know)
Provide clear, direct answer to their specific question in 2-3 sentences.
- No background or theory - just the answer
- Be specific and actionable
- Use simple, confident language

Example: "Yes, you can legally challenge this boundary dispute. Under Nepal law, you have the right to file a case within 35 days of discovering the encroachment. Your situation has strong legal grounds based on property ownership laws."

---

### 2. LEGAL BASIS (Supporting laws, articles, and clauses)
Provide the exact legal foundation for your answer:

**📜 PRIMARY LAW:**
**[Law Name]** - [Section/Article Number]
- **Clause:** "[Exact clause text or accurate summary]"
- **Plain English:** [What this means in simple terms]
- **Your Case:** [How this applies to their situation]

**📚 SUPPORTING LAWS:**
1. **[Law Name 2]** - Article [X], Clause [Y]
   - Relevance: [Why this matters to their case]

2. **[Law Name 3]** - Section [X]
   - Relevance: [Why this matters to their case]

**⚖️ CONSTITUTIONAL PROTECTION (if applicable):**
- **Constitution of Nepal 2072** - Article [X]
- Right protected: [Specific fundamental right]

**🏛️ COURT PRECEDENTS (if applicable):**
- **Case:** [Case name or reference] ([Year])
- **Ruling:** [Brief outcome]
- **Relevance:** [How this supports their position]

---

### 3. IMMEDIATE NEXT STEP
Tell them the single most important action to take in next 24-48 hours:

**📍 YOUR NEXT STEP:**
[Specific action with clear instructions]

**Why this matters:** [Brief explanation]
**Deadline:** [If time-sensitive]

---

### 4. SITUATION ASSESSMENT
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

---

### 5. YOUR OPTIONS (2-3 clear paths)
Present available options with complete details:

**OPTION 1: [Name] ⭐ RECOMMENDED**
- **Timeline:** [X weeks/months]
- **Cost:** NPR [X,000 - Y,000]
- **Success Rate:** [X%]
- **Pros:**
  ✓ [Benefit 1]
  ✓ [Benefit 2]
  ✓ [Benefit 3]
- **Cons:**
  ✗ [Drawback 1]
  ✗ [Drawback 2]

**OPTION 2: [Name]**
[Same format as Option 1]

---

### 6. STEP-BY-STEP ACTION PLAN
Break down the recommended option into weekly phases:

**WEEK 1: [Phase Name]**
Your tasks:
□ [Specific action with details]
□ [Specific action with details]
□ [Specific action with details]

Cost this week: NPR [X]
Time needed: [X hours]
Documents needed: [List]

**WEEK 2: [Phase Name]**
[Same format]

**WEEK 3-4: [Phase Name]**
[Same format]

---

### 7. PRACTICAL DETAILS (Where to go, what to bring)

**🏢 WHERE TO GO:**
**Office:** [Specific office name]
**Address:** [Complete address with landmarks]
**Contact:** [Phone number if available]
**Hours:** [Operating hours]
**Best time to visit:** [Recommendation]

**📋 DOCUMENTS TO BRING:**
Required:
□ [Document 1] - [Why needed]
□ [Document 2] - [Why needed]
□ [Document 3] - [Why needed]

Optional but helpful:
□ [Document 4]
□ [Document 5]

**💰 FEES TO PAY:**
- [Fee type 1]: NPR [X]
- [Fee type 2]: NPR [X]
- Total: NPR [X]

---

### 8. ADD-ONS (Extra helpful information)

**⚠️ COMMON MISTAKES TO AVOID:**
❌ **Don't:** [Mistake 1]
   **Why:** [Consequence]
   **Instead:** [Correct approach]

❌ **Don't:** [Mistake 2]
   **Why:** [Consequence]
   **Instead:** [Correct approach]

**💡 PRO TIPS:**
✓ [Helpful tip 1]
✓ [Helpful tip 2]
✓ [Helpful tip 3]

**🤝 WHEN TO GET A LAWYER:**
**Handle yourself if:**
✅ [Condition 1]
✅ [Condition 2]

**Get a lawyer if:**
⚠️ [Condition 1]
⚠️ [Condition 2]

**Lawyer costs:** NPR [X-Y] typically

**📞 EMERGENCY CONTACTS (if applicable):**
- [Relevant helpline]: [Number]
- [Relevant authority]: [Number]

---

### 9. VERIFICATION RESOURCES (Links and references)

**📖 OFFICIAL LEGAL DOCUMENTS:**
You can verify this information at these official sources:

1. **[Law Name]**
   - Source: Nepal Law Commission
   - Link: http://www.lawcommission.gov.np
   - Search for: "[Law name in Nepali/English]"
   - Relevant sections: [Article/Section numbers]

2. **Constitution of Nepal 2072**
   - Source: Official Government Portal
   - Link: http://www.nepal.gov.np
   - Relevant articles: [Article numbers]

3. **Supreme Court Decisions**
   - Source: Supreme Court of Nepal
   - Link: http://supremecourt.gov.np
   - Search keywords: "[Relevant keywords]"

**🏛️ GOVERNMENT PORTALS:**
- Nepal Law Commission: http://www.lawcommission.gov.np
- Ministry of Law: http://www.moljpa.gov.np
- Supreme Court: http://supremecourt.gov.np
- District Court Portal: [Relevant district court website]

**📚 ADDITIONAL READING:**
- [Relevant legal guide or resource]
- [Relevant government publication]
- [Relevant legal aid organization]

**✅ HOW TO VERIFY:**
1. Visit the Nepal Law Commission website
2. Search for "[Law name]"
3. Look for Section/Article [X]
4. Cross-reference with Constitution Article [Y]

**📱 LEGAL AID RESOURCES:**
- Nepal Bar Association: [Contact]
- Legal Aid Committee: [Contact]
- [Relevant NGO]: [Contact]

---

### 10. SUMMARY & ENCOURAGEMENT

**🎯 QUICK RECAP:**
- **Your answer:** [One sentence summary]
- **Legal basis:** [Primary law]
- **Next step:** [Immediate action]
- **Timeline:** [Expected duration]
- **Cost:** NPR [Range]

**💪 REMEMBER:**
• [Encouraging point 1]
• [Encouraging point 2]
• This situation CAN be resolved
• You have legal rights and protections

**⏰ THIS WEEK'S PRIORITIES:**
□ [Action 1]
□ [Action 2]
□ [Action 3]

**TONE GUIDELINES:**
- Answer first, explanation second
- Confident but not arrogant
- Cite exact laws with article/clause numbers
- Provide verifiable sources and links
- Specific with numbers, names, locations
- Professional but warm and accessible
- Use simple language, avoid jargon

**CRITICAL REQUIREMENTS:**
1. **Answer First:** Start with what user needs to know, not background
2. **Legal Citations:** Always cite exact law name, article, section, clause
3. **Verifiable Sources:** Provide official government links where they can verify
4. **Practical Details:** Include specific offices, addresses, phone numbers
5. **Cost Transparency:** Give exact fee amounts in NPR
6. **Timeline Clarity:** Specify weeks/months for each step
7. **Resource Links:** Always end with verification resources section
8. **Clickable References:** Format links properly so users can click and verify

**CITATION FORMAT:**
Always use this format for laws:
"[Law Name] - Article [X], Section [Y], Clause [Z]"
Example: "Civil Code 2074 - Article 232, Section 1, Clause (a)"

**LINK FORMAT:**
Always provide:
- Official government website links
- Specific search terms to use
- Relevant section/article numbers to look for
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
