"""
Nepal Official Documents and Forms Database
Contains links and information about official government forms and procedures
"""

OFFICIAL_DOCUMENTS = {
    "tax_notice": {
        "forms": [
            {
                "name": "Property Tax Payment Form",
                "description": "Form for paying property tax to municipality",
                "office": "Local Municipality Office",
                "url": "https://kathmandu.gov.np/forms/property-tax",
                "required_documents": ["Citizenship certificate", "Property ownership certificate", "Previous tax receipt"]
            },
            {
                "name": "Tax Penalty Waiver Application",
                "description": "Application for waiving tax penalties",
                "office": "Municipality Revenue Section",
                "url": "https://kathmandu.gov.np/forms/penalty-waiver",
                "required_documents": ["Tax notice", "Reason for delay", "Supporting documents"]
            }
        ],
        "procedures": [
            "Visit municipality revenue section",
            "Fill property tax payment form",
            "Submit required documents",
            "Pay tax amount at counter",
            "Collect payment receipt"
        ],
        "offices": [
            "Kathmandu Metropolitan City - Revenue Department",
            "Lalitpur Metropolitan City - Tax Section",
            "Bhaktapur Municipality - Revenue Office"
        ]
    },
    
    "court_notice": {
        "forms": [
            {
                "name": "Written Statement Form",
                "description": "Response to court summons or petition",
                "office": "District Court Registry",
                "url": "https://supremecourt.gov.np/forms/written-statement",
                "required_documents": ["Court summons", "Supporting evidence", "Advocate authorization"]
            },
            {
                "name": "Appeal Application",
                "description": "Application for appealing court decision",
                "office": "Appellate Court",
                "url": "https://supremecourt.gov.np/forms/appeal",
                "required_documents": ["Lower court judgment", "Appeal grounds", "Court fee receipt"]
            }
        ],
        "procedures": [
            "File written statement within 15 days",
            "Submit all supporting documents",
            "Pay required court fees",
            "Attend court hearings as scheduled",
            "Follow court orders and procedures"
        ],
        "offices": [
            "Supreme Court of Nepal - Ramshah Path, Kathmandu",
            "District Courts - All 77 districts",
            "High Courts - 7 provinces"
        ]
    },
    
    "employment_letter": {
        "forms": [
            {
                "name": "Labor Complaint Form",
                "description": "Complaint form for employment disputes",
                "office": "District Labor Office",
                "url": "https://mol.gov.np/forms/labor-complaint",
                "required_documents": ["Employment contract", "Salary slips", "Termination letter", "ID documents"]
            },
            {
                "name": "Social Security Registration",
                "description": "Registration for social security benefits",
                "office": "Social Security Fund Office",
                "url": "https://ssf.gov.np/registration",
                "required_documents": ["Employment certificate", "Citizenship", "Bank account details"]
            }
        ],
        "procedures": [
            "File complaint within 30 days of incident",
            "Submit employment documents",
            "Attend labor office hearings",
            "Follow mediation process",
            "Implement agreed resolution"
        ],
        "offices": [
            "Department of Labor - Singha Durbar, Kathmandu",
            "District Labor Offices - All districts",
            "Social Security Fund - Regional offices"
        ]
    },
    
    "legal_notice": {
        "forms": [
            {
                "name": "Legal Notice Template",
                "description": "Standard format for legal notices",
                "office": "Nepal Bar Association",
                "url": "https://nepalbar.org.np/templates/legal-notice",
                "required_documents": ["Facts of the case", "Legal basis", "Demand/relief sought"]
            },
            {
                "name": "Advocate Authorization",
                "description": "Authorization letter for legal representation",
                "office": "Any Notary Public",
                "url": "https://nepalbar.org.np/forms/authorization",
                "required_documents": ["Client ID", "Advocate license", "Case details"]
            }
        ],
        "procedures": [
            "Draft legal notice with advocate",
            "Send through registered post",
            "Keep delivery receipt",
            "Wait for response period",
            "File court case if no response"
        ],
        "offices": [
            "Nepal Bar Association - Ramshah Path, Kathmandu",
            "District Bar Associations - All districts",
            "Notary Public Offices - Major cities"
        ]
    },
    
    "property_document": {
        "forms": [
            {
                "name": "Land Registration Application",
                "description": "Application for registering land ownership",
                "office": "Land Revenue Office",
                "url": "https://dolr.gov.np/forms/land-registration",
                "required_documents": ["Sale deed", "Tax clearance", "Survey report", "Citizenship"]
            },
            {
                "name": "Property Valuation Form",
                "description": "Form for property valuation assessment",
                "office": "District Administration Office",
                "url": "https://dao.gov.np/forms/property-valuation",
                "required_documents": ["Property documents", "Location map", "Construction details"]
            }
        ],
        "procedures": [
            "Verify property documents",
            "Get property surveyed",
            "Pay registration fees",
            "Submit application with documents",
            "Collect registered ownership certificate"
        ],
        "offices": [
            "Department of Land Records - Dillibazar, Kathmandu",
            "Land Revenue Offices - All districts",
            "Survey Offices - Regional centers"
        ]
    },
    
    "government_notice": {
        "forms": [
            {
                "name": "Business License Application",
                "description": "Application for business registration and licensing",
                "office": "Department of Industry",
                "url": "https://doi.gov.np/forms/business-license",
                "required_documents": ["Business plan", "Citizenship", "Office rental agreement", "Tax registration"]
            },
            {
                "name": "License Renewal Form",
                "description": "Form for renewing expired business license",
                "office": "Municipality/Industry Department",
                "url": "https://doi.gov.np/forms/license-renewal",
                "required_documents": ["Expired license", "Tax clearance", "Renewal fee", "Updated documents"]
            }
        ],
        "procedures": [
            "Check license requirements",
            "Prepare required documents",
            "Submit application with fees",
            "Complete inspection if required",
            "Collect renewed license"
        ],
        "offices": [
            "Department of Industry - Tripureshwor, Kathmandu",
            "Municipality Offices - Local areas",
            "One Stop Service Centers - Major cities"
        ]
    },
    
    "contract": {
        "forms": [
            {
                "name": "Contract Registration Form",
                "description": "Form for registering legal contracts",
                "office": "District Administration Office",
                "url": "https://dao.gov.np/forms/contract-registration",
                "required_documents": ["Original contract", "Party IDs", "Witness signatures", "Registration fee"]
            },
            {
                "name": "Contract Dispute Mediation",
                "description": "Application for contract dispute mediation",
                "office": "Mediation Center",
                "url": "https://mediation.gov.np/forms/dispute-resolution",
                "required_documents": ["Contract copy", "Dispute details", "Party agreements", "Mediation fee"]
            }
        ],
        "procedures": [
            "Draft contract with legal terms",
            "Get contract reviewed by lawyer",
            "Register contract if required",
            "Implement contract terms",
            "Resolve disputes through mediation"
        ],
        "offices": [
            "District Administration Offices - All districts",
            "Mediation Centers - Major cities",
            "Notary Public Offices - Urban areas"
        ]
    },
    
    "complaint": {
        "forms": [
            {
                "name": "Police Complaint (FIR)",
                "description": "First Information Report for criminal complaints",
                "office": "Nepal Police Station",
                "url": "https://nepalpolice.gov.np/forms/fir",
                "required_documents": ["Incident details", "Evidence", "Witness information", "ID documents"]
            },
            {
                "name": "Consumer Complaint Form",
                "description": "Complaint form for consumer rights violations",
                "office": "Consumer Committee",
                "url": "https://consumer.gov.np/forms/complaint",
                "required_documents": ["Purchase receipt", "Product details", "Complaint description", "Evidence"]
            }
        ],
        "procedures": [
            "Report incident immediately",
            "File formal complaint",
            "Provide evidence and witnesses",
            "Cooperate with investigation",
            "Follow up on case progress"
        ],
        "offices": [
            "Nepal Police - Local police stations",
            "Consumer Committees - District level",
            "Human Rights Commission - Regional offices"
        ]
    }
}

def get_official_documents(document_type: str):
    """Get official documents and procedures for a document type"""
    return OFFICIAL_DOCUMENTS.get(document_type, {
        "forms": [],
        "procedures": ["Consult with relevant government office for specific procedures"],
        "offices": ["Contact local government offices for assistance"]
    })

def get_all_document_types():
    """Get all available document types"""
    return list(OFFICIAL_DOCUMENTS.keys())

def search_forms(query: str):
    """Search for forms based on query"""
    results = []
    query_lower = query.lower()
    
    for doc_type, data in OFFICIAL_DOCUMENTS.items():
        for form in data.get('forms', []):
            if (query_lower in form['name'].lower() or 
                query_lower in form['description'].lower() or
                query_lower in doc_type.lower()):
                results.append({
                    'document_type': doc_type,
                    'form': form
                })
    
    return results