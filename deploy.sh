#!/bin/bash

# Nepal Law Assistant Platform Deployment Script

echo "🏛️ Deploying Nepal Law Assistant Platform..."

# Check if required tools are installed
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed. Aborting." >&2; exit 1; }

# Backend deployment
echo "📦 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env file from template..."
    cp .env.example .env 2>/dev/null || echo "Please create .env file with required configuration"
fi

cd ..

# Frontend deployment
echo "🎨 Setting up frontend..."
cd frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Creating frontend .env file..."
    echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env
    echo "WDS_SOCKET_PORT=443" >> .env
fi

# Build frontend for production
echo "Building frontend for production..."
npm run build

cd ..

# Create startup scripts
echo "📝 Creating startup scripts..."

# Backend startup script
cat > start-backend.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Nepal Law Assistant Backend..."
cd backend
source venv/bin/activate
uvicorn server:app --reload --host 0.0.0.0 --port 8000
EOF

# Frontend startup script
cat > start-frontend.sh << 'EOF'
#!/bin/bash
echo "🎨 Starting Nepal Law Assistant Frontend..."
cd frontend
npm start
EOF

# Make scripts executable
chmod +x start-backend.sh
chmod +x start-frontend.sh

# Create production startup script
cat > start-production.sh << 'EOF'
#!/bin/bash
echo "🏛️ Starting Nepal Law Assistant Platform in Production Mode..."

# Start backend in background
echo "Starting backend server..."
cd backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Serve frontend build
echo "Starting frontend server..."
cd ../frontend
npx serve -s build -l 3000 &
FRONTEND_PID=$!

echo "✅ Platform started successfully!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"

# Create stop script
cat > ../stop-production.sh << 'STOP_EOF'
#!/bin/bash
echo "🛑 Stopping Nepal Law Assistant Platform..."
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
echo "✅ Platform stopped successfully!"
STOP_EOF

chmod +x ../stop-production.sh

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
EOF

chmod +x start-production.sh

# Seed case studies database
echo "📚 Seeding case studies database..."
cd backend
source venv/bin/activate
python seed_case_studies.py
cd ..

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🚀 Quick Start Commands:"
echo "  Development:"
echo "    Backend:  ./start-backend.sh"
echo "    Frontend: ./start-frontend.sh"
echo ""
echo "  Production:"
echo "    Start:    ./start-production.sh"
echo "    Stop:     ./stop-production.sh"
echo ""
echo "📋 Next Steps:"
echo "  1. Configure your .env files in backend/ and frontend/"
echo "  2. Set up MongoDB connection"
echo "  3. Add your Emergent LLM API key"
echo "  4. Install Tesseract OCR for image processing"
echo "  5. Start the platform using the scripts above"
echo ""
echo "🔧 Additional Setup:"
echo "  • Install Tesseract: sudo apt-get install tesseract-ocr tesseract-ocr-nep"
echo "  • MongoDB: Ensure MongoDB is running on localhost:27017"
echo "  • API Key: Get Emergent LLM API key and add to backend/.env"
echo ""
echo "📚 Documentation: See README.md for detailed setup instructions"
echo "🏛️ Nepal Law Assistant Platform is ready to serve!"