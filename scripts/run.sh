#!/bin/bash
# Helper script to run the Hong Kong Criminal Law Expert System

# Change to project root directory
cd "$(dirname "$0")/.."

echo "=========================================="
echo "HK Criminal Law Expert System"
echo "=========================================="
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if activation was successful
if [ $? -eq 0 ]; then
    echo "✅ Virtual environment activated"
    echo ""
    
    # Check if port 8080 is in use and kill the process
    echo "Checking for existing processes on port 8080..."
    PORT_PID=$(lsof -ti:8080)
    if [ ! -z "$PORT_PID" ]; then
        echo "⚠️  Port 8080 is in use by process $PORT_PID"
        echo "🔄 Stopping existing process..."
        kill -9 $PORT_PID 2>/dev/null
        sleep 1
        echo "✅ Port cleared"
    else
        echo "✅ Port 8080 is available"
    fi
    echo ""
    
    # Run the application
    echo "Starting Flask application..."
    echo "Access the system at: http://localhost:8080"
    echo "Press Ctrl+C to stop the server"
    echo ""
    python3 webapp/app.py
else
    echo "❌ Error: Virtual environment not found"
    echo "Please run: python3 -m venv venv"
    echo "Then run: source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

