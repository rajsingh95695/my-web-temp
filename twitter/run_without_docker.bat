@echo off
echo ============================================
echo Twitter Sentiment Analysis Platform
echo Non-Docker Deployment (Local Python)
echo ============================================
echo.

echo This script runs the application without Docker.
echo Perfect for testing while Docker is being installed.
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found in PATH.
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo.
    echo After installing Python:
    echo 1. Check "Add Python to PATH" during installation
    echo 2. Restart command prompt
    echo 3. Run this script again
    pause
    exit /b 1
)

python --version
echo ✅ Python is available
echo.

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  pip not found. Trying python -m pip...
    python -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ pip is not available.
        echo Please ensure pip is installed with Python.
        pause
        exit /b 1
    )
    set PIP_CMD=python -m pip
) else (
    set PIP_CMD=pip
)

echo ✅ pip is available
echo.

REM Install dependencies
echo Step 1: Installing Python dependencies...
echo This may take a few minutes...
echo.

%PIP_CMD% install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies.
    echo Trying individual packages...
    
    %PIP_CMD% install streamlit requests plotly vaderSentiment pandas
    
    if errorlevel 1 (
        echo ❌ Still failed. Please check your internet connection.
        echo You can install manually:
        echo pip install streamlit requests plotly vaderSentiment pandas
        pause
        exit /b 1
    )
)

echo ✅ Dependencies installed successfully
echo.

REM Create necessary directories
echo Step 2: Creating required directories...
mkdir logs 2>nul
mkdir data 2>nul
mkdir reports 2>nul
mkdir .streamlit 2>nul

echo ✅ Directories created
echo.

REM Check if secrets file exists
if not exist .streamlit\secrets.toml (
    echo Step 3: Creating secrets file...
    echo [secrets] > .streamlit\secrets.toml
    echo RAPIDAPI_KEY = "68ed5d9870msh56c48d238ea984bp1aba51jsn0c4437f4859b" >> .streamlit\secrets.toml
    echo ✅ secrets.toml created with your API key
) else (
    echo ✅ secrets.toml already exists
)

echo.
echo ============================================
echo 🚀 Starting Twitter Sentiment Analysis App
echo ============================================
echo.
echo Application will start at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

REM Run the application
echo Starting Streamlit server...
echo.

python -m streamlit run app.py

if errorlevel 1 (
    echo.
    echo ❌ Failed to start Streamlit.
    echo.
    echo Troubleshooting:
    echo 1. Ensure all dependencies are installed
    echo 2. Check if port 8501 is already in use
    echo 3. Try: streamlit run app.py
    echo.
    echo Alternative command:
    echo python app.py
    echo.
    pause
)