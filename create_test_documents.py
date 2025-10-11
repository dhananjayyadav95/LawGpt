#!/usr/bin/env python3
"""
Create test documents for Nepal Law Assistant testing
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_images():
    """Create test images with legal document text"""
    
    # Create test images directory
    os.makedirs("test_documents", exist_ok=True)
    
    # Test documents content
    test_docs = {
        "property_tax_notice.png": """
KATHMANDU METROPOLITAN CITY
PROPERTY TAX NOTICE

Notice No: KMC/REV/2024/001
Date: 2024-01-15

To: Mr. Ram Bahadur Thapa
Address: Ward No. 5, Kathmandu

Subject: Property Tax Payment Notice

Dear Sir/Madam,

This is to inform you that your property tax for the fiscal year 2023/24 
is overdue. The details are as follows:

Property ID: KMC-2024-001
Tax Amount: Rs. 25,000
Penalty: Rs. 12,500
Total Due: Rs. 37,500

Please pay the above amount within 15 days from the date of this notice
to avoid further penalty.

Payment can be made at:
- KMC Revenue Office, Kathmandu
- Online portal: kathmandu.gov.np

Thank you.

Revenue Officer
Kathmandu Metropolitan City
        """,
        
        "court_summons.png": """
DISTRICT COURT, KATHMANDU
COURT SUMMONS

Case No: 2024/CV/001
Date: 2024-02-01

To: Ms. Sita Devi Sharma
Address: Lalitpur-3, Patan

You are hereby summoned to appear before this court on 2024-02-20
at 10:00 AM in connection with the case filed by Mr. Hari Prasad
regarding property boundary dispute.

Case Details:
- Plaintiff: Mr. Hari Prasad
- Defendant: Ms. Sita Devi Sharma
- Subject: Property boundary dispute
- Claim Amount: Rs. 500,000

You are required to file your written statement within 15 days
of receiving this summons.

Failure to appear may result in ex-parte proceedings.

Registrar
District Court, Kathmandu
        """,
        
        "employment_termination.png": """
ABC PRIVATE LIMITED
TERMINATION LETTER

Date: 2024-01-30
Employee ID: EMP001

To: Mr. Krishna Bahadur Rai
Position: Senior Officer

Subject: Termination of Employment

Dear Mr. Rai,

We regret to inform you that your employment with ABC Private Limited
is terminated effective from 2024-02-15 due to the following reasons:

1. Repeated absence without prior notice
2. Failure to meet performance targets
3. Violation of company policies

As per your employment contract, you are entitled to:
- One month salary in lieu of notice: Rs. 45,000
- Pending salary for January 2024: Rs. 30,000
- Gratuity amount: Rs. 75,000

Please contact HR department for final settlement.

Sincerely,

Human Resources Manager
ABC Private Limited
        """,
        
        "legal_notice.png": """
LEGAL NOTICE

From: Advocate Ramesh Kumar Shrestha
      Nepal Bar Association License No: 12345
      Kathmandu, Nepal

To: Mr. Gopal Singh Thakuri
    Bhaktapur-5, Nepal

Date: 2024-01-25

Subject: Legal Notice for Recovery of Loan Amount

Dear Sir,

On behalf of my client Mr. Bishnu Prasad Adhikari, I serve you this
legal notice for the following:

FACTS:
1. You borrowed Rs. 300,000 from my client on 2023-06-15
2. The loan was to be repaid within 6 months with 12% annual interest
3. Despite repeated requests, you have failed to repay the amount
4. Total outstanding amount is Rs. 318,000 as of today

DEMAND:
You are hereby called upon to pay the outstanding amount of Rs. 318,000
within 15 days of receipt of this notice.

CONSEQUENCES:
Failure to comply will result in legal proceedings against you for
recovery of the amount along with interest and legal costs.

Advocate Ramesh Kumar Shrestha
For and on behalf of Mr. Bishnu Prasad Adhikari
        """
    }
    
    # Create images with text
    for filename, content in test_docs.items():
        # Create image
        img_width, img_height = 800, 1000
        image = Image.new('RGB', (img_width, img_height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Try to use a font, fallback to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 16)
            title_font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()
        
        # Draw text
        lines = content.strip().split('\n')
        y_position = 50
        
        for line in lines:
            if line.strip():
                # Use larger font for titles
                current_font = title_font if line.isupper() and len(line) < 50 else font
                draw.text((50, y_position), line.strip(), fill='black', font=current_font)
            y_position += 25
        
        # Save image
        filepath = os.path.join("test_documents", filename)
        image.save(filepath)
        print(f"✅ Created: {filepath}")
    
    print(f"\n📁 Test documents created in 'test_documents' folder")
    print("🧪 Use these images to test the OCR and problem-solving features")

def create_test_text_files():
    """Create test text files"""
    
    test_files = {
        "contract_dispute.txt": """
RENTAL AGREEMENT DISPUTE

I signed a rental agreement for a house in Kathmandu for Rs. 20,000 per month.
The landlord is now demanding Rs. 30,000 per month and threatening to evict me.
The original agreement was for 2 years and I have been paying regularly.
What are my rights as a tenant under Nepal law?
        """,
        
        "inheritance_problem.txt": """
PROPERTY INHERITANCE ISSUE

My father passed away 6 months ago and left a house in Lalitpur.
My uncle is claiming that he has rights to the property and is preventing
me from registering it in my name. I have the will and other documents.
How can I resolve this inheritance dispute?
        """,
        
        "business_license_issue.txt": """
BUSINESS LICENSE PROBLEM

My restaurant license expired 3 months ago due to COVID-19 financial problems.
The municipality has sent a closure notice with heavy penalties.
I want to renew the license but the penalty amount is very high.
Is there any way to get penalty waiver and renew my license?
        """
    }
    
    for filename, content in test_files.items():
        filepath = os.path.join("test_documents", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"✅ Created: {filepath}")

if __name__ == "__main__":
    print("🏛️ Creating Test Documents for Nepal Law Assistant")
    print("=" * 50)
    
    create_test_images()
    create_test_text_files()
    
    print("\n📋 Test Documents Created:")
    print("Images (for OCR testing):")
    print("  - property_tax_notice.png")
    print("  - court_summons.png") 
    print("  - employment_termination.png")
    print("  - legal_notice.png")
    print("\nText Files (for document upload testing):")
    print("  - contract_dispute.txt")
    print("  - inheritance_problem.txt")
    print("  - business_license_issue.txt")
    
    print("\n🧪 How to Test:")
    print("1. Start the platform (backend + frontend)")
    print("2. Upload these files using the Document or Photo tabs")
    print("3. Check if OCR extracts text correctly")
    print("4. Verify that solutions are relevant and actionable")
    print("5. Test different document types and scenarios")