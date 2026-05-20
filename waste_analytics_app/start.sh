#!/bin/bash
# Quick start script for local development

echo "🚀 Starting Hostel Waste Analytics App..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📚 Installing dependencies..."
pip install -q -r waste_app/requirements.txt

# Run Streamlit app
echo "🎯 Launching Streamlit app..."
echo "📍 Open your browser to: http://localhost:8501"
echo ""
streamlit run waste_app/app.py
