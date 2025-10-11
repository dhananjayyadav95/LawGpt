  # Nepal Law Assistant Platform

A comprehensive AI-powered legal assistance platform designed specifically for Nepal's legal system. This platform helps users get legal guidance, analyze documents, conduct legal research, and access Nepal law resources.

## 🏛️ Features

### 1. **Text-Based Legal Consultation**
- Ask legal questions in plain language
- Get AI-powered responses with Nepal law references
- Session-based query history
- Relevant law citations and sources

### 2. **Document Analysis**
- Upload PDF, DOCX, or TXT legal documents
- AI analysis of document content
- Identification of legal issues and risks
- Specific recommendations based on Nepal law
- Relevant law references for uploaded documents

### 3. **Comprehensive Legal Research**
- In-depth legal research with case precedents
- Supreme Court of Nepal case references
- Step-by-step legal procedures
- Required documents and timelines
- Cost estimates and legal remedies

### 4. **Legal Document Templates** (Coming Soon)
- Generate legal document templates
- Court-compliant formats
- Customizable placeholders
- Filing instructions and requirements

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - Document database for storing queries and analyses
- **Emergent LLM** - AI integration with Gemini 2.5 Pro
- **PyPDF2** - PDF document processing
- **python-docx** - Word document processing

### Frontend
- **React 19** - Modern React with latest features
- **shadcn/ui** - Beautiful, accessible UI components
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client for API calls

### AI & Legal Analysis
- **Multiple AI Providers** - OpenAI GPT-4, Anthropic Claude, Google Gemini, Emergent LLM
- **Flexible Configuration** - Choose the AI provider that fits your needs and budget
- **Custom Legal Prompts** - Specialized for Nepal law across all providers
- **Document Processing** - Text extraction and analysis
- **Legal Pattern Recognition** - Identifies laws, cases, and procedures

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB
- Emergent LLM API key

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nepal-law-assistant
   ```

2. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration:
   # MONGO_URL=mongodb://localhost:27017
   # DB_NAME=nepal_law_db
   # AI_PROVIDER=openai  # or anthropic, google, emergent
   # OPENAI_API_KEY=your_openai_api_key_here
   # CORS_ORIGINS=http://localhost:3000
   ```

4. **Start the backend server**
   ```bash
   uvicorn server:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration:
   # REACT_APP_BACKEND_URL=http://localhost:8000
   ```

3. **Start the frontend development server**
   ```bash
   npm start
   ```

4. **Access the application**
   Open [http://localhost:3000](http://localhost:3000) in your browser

## 📚 API Endpoints

### Legal Consultation
- `POST /api/analyze-legal-problem` - Analyze legal problems
- `GET /api/legal-history/{session}` - Get query history

### Document Analysis
- `POST /api/upload-document` - Upload and analyze documents
- `GET /api/document-history/{session}` - Get document analysis history

### Legal Research
- `POST /api/legal-research` - Comprehensive legal research
- `GET /api/legal-templates` - Get available document templates
- `POST /api/generate-legal-template` - Generate legal document templates

## 🏛️ Nepal Legal System Integration

### Supported Legal Areas
- **Constitutional Law** - Constitution of Nepal 2072
- **Civil Law** - Civil Code and procedures
- **Criminal Law** - Criminal Code and procedures
- **Property Law** - Land and property regulations
- **Family Law** - Marriage, divorce, inheritance
- **Commercial Law** - Business and contract law
- **Administrative Law** - Government procedures

### Legal Document Support
- Court petitions and applications
- Legal notices and contracts
- Affidavits and power of attorney
- Property transfer documents
- Complaint applications
- Appeal documents

### Case Precedent Integration
- Supreme Court of Nepal decisions
- Nepal Law Journal references
- Legal precedent analysis
- Court procedure guidance

## 🔒 Security & Privacy

- **Session-based data storage** - User data isolated by session
- **Secure file upload** - File type and size validation
- **Data encryption** - Sensitive data protection
- **Privacy compliance** - No personal data retention beyond session

## 🌟 Key Benefits

### For Citizens
- **Accessible Legal Guidance** - Get legal help in plain language
- **Cost-Effective** - Reduce initial legal consultation costs
- **24/7 Availability** - Access legal guidance anytime
- **Document Analysis** - Understand legal documents quickly

### For Legal Professionals
- **Research Assistant** - Quick access to legal precedents
- **Document Templates** - Generate standard legal documents
- **Case Analysis** - AI-powered legal document review
- **Client Education** - Help clients understand legal issues

### For Students & Researchers
- **Legal Education** - Learn Nepal law through practical examples
- **Research Tool** - Access comprehensive legal information
- **Case Studies** - Analyze real legal scenarios
- **Academic Support** - Understand complex legal concepts

## 🛣️ Roadmap

### Phase 1 (Current)
- ✅ Basic legal consultation
- ✅ Document upload and analysis
- ✅ Legal research with precedents
- ✅ Session-based history

### Phase 2 (In Development)
- 🔄 Legal document template generator
- 🔄 Multi-language support (Nepali)
- 🔄 Advanced case precedent search
- 🔄 Legal procedure workflows

### Phase 3 (Planned)
- 📋 Lawyer directory integration
- 📋 Court filing assistance
- 📋 Legal fee calculator
- 📋 Mobile application

## 🤝 Contributing

We welcome contributions from legal professionals, developers, and Nepal law experts. Please see our contributing guidelines for more information.

### Areas for Contribution
- Legal knowledge base expansion
- Nepal law document templates
- Case precedent database
- Multi-language support
- UI/UX improvements

## 📄 Legal Disclaimer

This platform provides general legal information and AI-generated guidance. It is not a substitute for professional legal advice. For specific legal matters, please consult with qualified Nepal legal professionals.

## 📞 Support

For technical support or legal content questions, please contact our team or create an issue in the repository.

---

**Built with ❤️ for Nepal's legal community**
