@echo off
REM Quick start script for Windows

echo 🚀 Starting Hostel Waste Analytics App...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📚 Installing dependencies...
pip install -q -r waste_app\requirements.txt

REM Run Streamlit app
echo 🎯 Launching Streamlit app...
echo 📍 Open your browser to: http://localhost:8501
echo.
streamlit run waste_app\app.py

pause
