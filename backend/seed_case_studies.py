#!/usr/bin/env python3
"""
Nepal Legal Case Studies Database Seeder
Seeds the database with real-world case studies and solutions
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Comprehensive case studies database
CASE_STUDIES = [
    # Property Tax Cases
    {
        "case_title": "Property Tax Penalty Waiver - Kathmandu Municipality",
        "problem_description": "Received property tax notice with 100% penalty for 2-year delay in payment due to overseas employment",
        "solution_applied": "Filed penalty waiver application with municipality citing overseas employment certificate and financial hardship",
        "outcome": "Penalty reduced to 25%, saved Rs. 45,000 in penalties",
        "timeline": "21 days from application to resolution",
        "cost_involved": "Rs. 1,000 application fee + Rs. 15,000 base tax",
        "lessons_learned": [
            "Always inform municipality about overseas employment",
            "Keep employment certificates for penalty waiver",
            "File waiver application before paying full amount"
        ],
        "document_type": "tax_notice",
        "success_rating": 5,
        "location": "Kathmandu",
        "year": 2023,
        "tags": ["property_tax", "penalty_waiver", "overseas_employment"]
    },
    
    # Court Notice Cases
    {
        "case_title": "Court Summons Response - Property Boundary Dispute",
        "problem_description": "Received court summons for property boundary dispute filed by neighbor claiming 2 feet of land",
        "solution_applied": "Filed written statement within 15 days with land ownership certificate, survey report, and witness statements",
        "outcome": "Case settled through court mediation, boundary confirmed as per original survey",
        "timeline": "4 months from summons to settlement",
        "cost_involved": "Rs. 8,000 court fees + Rs. 25,000 lawyer fees + Rs. 5,000 survey costs",
        "lessons_learned": [
            "Never ignore court summons",
            "Gather all property documents immediately",
            "Court mediation is faster than full trial"
        ],
        "document_type": "court_notice",
        "success_rating": 4,
        "location": "Lalitpur",
        "year": 2023,
        "tags": ["property_dispute", "court_summons", "mediation"]
    },
    
    # Employment Cases
    {
        "case_title": "Wrongful Termination Compensation Success",
        "problem_description": "Terminated from job without proper notice period and end-of-service benefits after 3 years of employment",
        "solution_applied": "Filed complaint with District Labor Office with employment contract, salary slips, and termination letter",
        "outcome": "Received 3 months salary compensation plus all pending benefits totaling Rs. 180,000",
        "timeline": "45 days from complaint filing to resolution",
        "cost_involved": "Rs. 500 filing fee + Rs. 3,000 documentation costs",
        "lessons_learned": [
            "Keep all employment documents safe",
            "Labor Office is effective for employment disputes",
            "File complaint within 30 days of termination"
        ],
        "document_type": "employment_letter",
        "success_rating": 5,
        "location": "Pokhara",
        "year": 2023,
        "tags": ["wrongful_termination", "labor_office", "compensation"]
    },
    
    # Legal Notice Cases
    {
        "case_title": "Loan Recovery Through Legal Notice",
        "problem_description": "Friend borrowed Rs. 500,000 for business but refused to repay despite multiple requests",
        "solution_applied": "Sent legal notice through advocate demanding repayment within 15 days, then filed case in district court",
        "outcome": "Borrower agreed to repay in installments, avoided lengthy court case",
        "timeline": "30 days from legal notice to settlement agreement",
        "cost_involved": "Rs. 5,000 legal notice fee + Rs. 2,000 agreement drafting",
        "lessons_learned": [
            "Legal notice often resolves disputes without court",
            "Always have written loan agreements",
            "Act quickly before borrower disposes assets"
        ],
        "document_type": "legal_notice",
        "success_rating": 4,
        "location": "Chitwan",
        "year": 2023,
        "tags": ["loan_recovery", "legal_notice", "debt_collection"]
    },
    
    # Government Notice Cases
    {
        "case_title": "Business License Renewal After Penalty",
        "problem_description": "Business license expired 6 months ago, received closure notice from municipality with heavy penalty",
        "solution_applied": "Applied for license renewal with penalty waiver application citing COVID-19 business impact",
        "outcome": "License renewed with 50% penalty reduction, business operations resumed",
        "timeline": "15 days from application to license issuance",
        "cost_involved": "Rs. 8,000 renewal fee + Rs. 5,000 reduced penalty",
        "lessons_learned": [
            "Renew licenses before expiry to avoid penalties",
            "COVID-19 impact can be grounds for penalty waiver",
            "Municipality is flexible with genuine cases"
        ],
        "document_type": "government_notice",
        "success_rating": 4,
        "location": "Butwal",
        "year": 2023,
        "tags": ["business_license", "penalty_waiver", "covid_impact"]
    },
    
    # Contract Dispute Cases
    {
        "case_title": "Construction Contract Breach Resolution",
        "problem_description": "Contractor abandoned house construction project halfway, demanding extra payment beyond agreed amount",
        "solution_applied": "Negotiated through local ward office mediation with contract terms and completed work assessment",
        "outcome": "Contractor completed work as per original contract, no extra payment required",
        "timeline": "2 months from dispute to project completion",
        "cost_involved": "Rs. 2,000 mediation fee + Rs. 5,000 technical assessment",
        "lessons_learned": [
            "Clear contract terms prevent disputes",
            "Local mediation is effective for construction disputes",
            "Document all work progress with photos"
        ],
        "document_type": "contract",
        "success_rating": 4,
        "location": "Dharan",
        "year": 2023,
        "tags": ["construction_contract", "breach", "mediation"]
    },
    
    # Family Law Cases
    {
        "case_title": "Mutual Divorce with Property Settlement",
        "problem_description": "Couple wanted divorce by mutual consent with fair division of jointly acquired property",
        "solution_applied": "Filed joint petition in district court with property division agreement and child custody arrangement",
        "outcome": "Divorce granted in single hearing, property divided as agreed, child custody shared",
        "timeline": "3 months from petition filing to divorce decree",
        "cost_involved": "Rs. 15,000 court fees + Rs. 30,000 lawyer fees + Rs. 5,000 documentation",
        "lessons_learned": [
            "Mutual consent divorce is faster and cheaper",
            "Property agreement prevents future disputes",
            "Child welfare is court's primary concern"
        ],
        "document_type": "court_notice",
        "success_rating": 5,
        "location": "Biratnagar",
        "year": 2023,
        "tags": ["mutual_divorce", "property_division", "child_custody"]
    },
    
    # Insurance Cases
    {
        "case_title": "Motor Insurance Claim Success After Initial Rejection",
        "problem_description": "Insurance company rejected motor accident claim citing policy violation, demanded Rs. 200,000 repair costs",
        "solution_applied": "Filed complaint with Insurance Board with accident report, policy documents, and independent assessment",
        "outcome": "Insurance company paid full claim amount after board intervention",
        "timeline": "60 days from complaint to claim settlement",
        "cost_involved": "Rs. 1,000 complaint fee + Rs. 3,000 independent assessment",
        "lessons_learned": [
            "Insurance Board effectively resolves claim disputes",
            "Keep all policy documents and follow procedures",
            "Independent assessment strengthens claim"
        ],
        "document_type": "complaint",
        "success_rating": 5,
        "location": "Janakpur",
        "year": 2023,
        "tags": ["insurance_claim", "motor_accident", "insurance_board"]
    },
    
    # Land Registration Cases
    {
        "case_title": "Land Registration After Inheritance Dispute",
        "problem_description": "Unable to register inherited land due to objection from distant relative claiming ownership rights",
        "solution_applied": "Filed case in district court with inheritance documents, family tree, and witness testimonies",
        "outcome": "Court confirmed inheritance rights, land registered successfully",
        "timeline": "8 months from case filing to land registration",
        "cost_involved": "Rs. 25,000 court fees + Rs. 40,000 lawyer fees + Rs. 10,000 documentation",
        "lessons_learned": [
            "Inheritance disputes require strong documentation",
            "Family tree and witness testimony are crucial",
            "Court process ensures clear title"
        ],
        "document_type": "property_document",
        "success_rating": 4,
        "location": "Nepalgunj",
        "year": 2023,
        "tags": ["land_registration", "inheritance_dispute", "property_rights"]
    },
    
    # Consumer Rights Cases
    {
        "case_title": "Defective Product Compensation from Electronics Store",
        "problem_description": "Purchased laptop that failed within warranty period, store refused replacement or refund",
        "solution_applied": "Filed complaint with District Consumer Committee with purchase receipt and technical assessment report",
        "outcome": "Store ordered to provide full refund plus compensation for inconvenience",
        "timeline": "30 days from complaint to resolution",
        "cost_involved": "Rs. 500 complaint fee + Rs. 2,000 technical assessment",
        "lessons_learned": [
            "Consumer committees are effective for product disputes",
            "Keep all purchase receipts and warranty documents",
            "Technical assessment report strengthens case"
        ],
        "document_type": "complaint",
        "success_rating": 5,
        "location": "Hetauda",
        "year": 2023,
        "tags": ["consumer_rights", "defective_product", "warranty_dispute"]
    }
]

async def seed_case_studies():
    """Seed the database with case studies"""
    try:
        # Test connection first
        await client.admin.command('ping')
        print("✅ MongoDB connection successful")
        
        # Clear existing case studies
        await db.case_studies.delete_many({})
        print("Cleared existing case studies")
        
        # Insert new case studies
        for case_study in CASE_STUDIES:
            case_study['timestamp'] = datetime.now(timezone.utc)
            await db.case_studies.insert_one(case_study)
        
        print(f"Successfully seeded {len(CASE_STUDIES)} case studies")
        
        # Create indexes for better search performance
        await db.case_studies.create_index("document_type")
        await db.case_studies.create_index("tags")
        await db.case_studies.create_index("success_rating")
        await db.case_studies.create_index("location")
        
        print("Created database indexes")
        
        # Print summary
        print("\nCase Studies Summary:")
        for doc_type in set(case['document_type'] for case in CASE_STUDIES):
            count = len([case for case in CASE_STUDIES if case['document_type'] == doc_type])
            print(f"  {doc_type}: {count} cases")
        
    except Exception as e:
        print(f"⚠️  Database seeding failed: {e}")
        print("💡 The platform will still work without database seeding")
        print("📖 You can use a cloud MongoDB or install MongoDB locally")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_case_studies())