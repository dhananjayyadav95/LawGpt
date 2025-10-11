#!/bin/bash
echo "🚀 Starting Nepal Law Assistant Backend..."
uvicorn server_working:app --host 0.0.0.0 --port ${PORT:-8000}