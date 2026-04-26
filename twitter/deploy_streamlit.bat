@echo off
echo ============================================
echo Twitter Sentiment Analysis Platform
echo Streamlit Cloud Deployment Assistant
echo ============================================
echo.

echo यह script आपको Streamlit Cloud पर deploy करने में help करेगा।
echo.
echo Step-by-step instructions:
echo.

echo Step 1: GitHub Repository Setup
echo --------------------------------
echo 1. https://github.com पर जाएं
echo 2. "New repository" बटन पर क्लिक करें
echo 3. Repository name: twitter-sentiment-analysis
echo 4. "Create repository" बटन पर क्लिक करें
echo.
echo Step 2: Git Initialize करें (अगर पहले से नहीं किया है)
echo -----------------------------------------------------
echo.
echo क्या आपने already git initialize किया है?
choice /c YN /m "Have you already initialized git? (Y/N):"
if errorlevel 2 goto init_git
goto skip_git_init

:init_git
echo.
echo Initializing git repository...
git init
git add .
git commit -m "Initial commit for Twitter Sentiment Analysis Platform"
git branch -M main
echo ✅ Git initialized
echo.

:skip_git_init
echo.
echo Step 3: GitHub Repository URL
echo ------------------------------
set /p GITHUB_URL=Enter your GitHub repository URL (e.g., https://github.com/your-username/twitter-sentiment-analysis.git): 

echo.
echo Step 4: Git Remote Add और Push
echo -------------------------------
echo Adding remote repository...
git remote add origin %GITHUB_URL%
git push -u origin main

if errorlevel 1 (
    echo ❌ Git push failed.
    echo Please check:
    echo 1. GitHub URL is correct
    echo 2. You have git installed
    echo 3. You're logged in to GitHub
    echo.
    echo Manual command:
    echo git remote add origin %GITHUB_URL%
    echo git push -u origin main
    echo.
    pause
    exit /b 1
)

echo ✅ Code pushed to GitHub successfully!
echo.

echo Step 5: Streamlit Cloud Setup
echo ------------------------------
echo.
echo 1. Open https://streamlit.io/cloud in your browser
echo 2. Click "Get started" and sign in with GitHub
echo 3. Click "New app" button
echo 4. Select your repository: twitter-sentiment-analysis
echo 5. Configure settings:
echo    - Main file path: app.py
echo    - Python version: 3.9
echo    - Branch: main
echo.
echo Step 6: Add Secrets to Streamlit Cloud
echo ---------------------------------------
echo.
echo After creating app, go to:
echo 1. App settings → "Secrets"
echo 2. Paste this configuration:
echo.
echo [secrets]
echo RAPIDAPI_KEY = "68ed5d9870msh56c48d238ea984bp1aba51jsn0c4437f4859b"
echo.
echo Step 7: Deploy App
echo ------------------
echo.
echo Click "Deploy" button and wait 2-3 minutes.
echo.
echo Your app will be available at:
echo https://your-app-name.streamlit.app
echo.

echo Step 8: Verify Deployment
echo --------------------------
echo.
echo After deployment, open your app URL and:
echo 1. Check if page loads without errors
echo 2. Try searching for a keyword (e.g., "technology")
echo 3. Verify charts are displaying correctly
echo.

echo ============================================
echo Deployment Files Check
echo ============================================
echo.
echo Checking required files for Streamlit Cloud...
echo.

set ALL_GOOD=1

if exist app.py (
    echo ✅ app.py found (main application)
) else (
    echo ❌ app.py missing
    set ALL_GOOD=0
)

if exist requirements.txt (
    echo ✅ requirements.txt found (dependencies)
    
    REM Check if all required packages are listed
    findstr "streamlit" requirements.txt >nul
    if errorlevel 1 (
        echo ⚠️  streamlit not in requirements.txt
    )
    
    findstr "requests" requirements.txt >nul
    if errorlevel 1 (
        echo ⚠️  requests not in requirements.txt
    )
    
    findstr "plotly" requirements.txt >nul
    if errorlevel 1 (
        echo ⚠️  plotly not in requirements.txt
    )
    
    findstr "vaderSentiment" requirements.txt >nul
    if errorlevel 1 (
        echo ⚠️  vaderSentiment not in requirements.txt
    )
    
    findstr "pandas" requirements.txt >nul
    if errorlevel 1 (
        echo ⚠️  pandas not in requirements.txt
    )
) else (
    echo ❌ requirements.txt missing
    set ALL_GOOD=0
)

if exist .streamlit\secrets.toml (
    echo ✅ .streamlit/secrets.toml found (local secrets)
    
    REM Check if API key is present
    findstr "RAPIDAPI_KEY" .streamlit\secrets.toml >nul
    if errorlevel 1 (
        echo ⚠️  RAPIDAPI_KEY not found in secrets.toml
    ) else (
        echo ✅ API key configured in secrets.toml
    )
) else (
    echo ⚠️  .streamlit/secrets.toml not found (will use Streamlit Cloud secrets)
)

if exist assets\styles.css (
    echo ✅ assets/styles.css found (custom styling)
) else (
    echo ⚠️  assets/styles.css not found (UI may look different)
)

echo.
echo ============================================
if %ALL_GOOD%==1 (
    echo ✅ ALL FILES READY FOR STREAMLIT CLOUD DEPLOYMENT!
    echo.
    echo Summary:
    echo 1. Code pushed to GitHub: ✅
    echo 2. Required files present: ✅
    echo 3. API key configured: ✅
    echo 4. Dependencies listed: ✅
    echo.
    echo Next: Complete Streamlit Cloud setup as described above.
) else (
    echo ⚠️  SOME FILES ARE MISSING OR INCOMPLETE
    echo Please fix the issues above before deploying.
)

echo ============================================
echo.
echo Useful Commands for Troubleshooting:
echo ------------------------------------
echo 1. Test locally: run_without_docker.bat
echo 2. Check Python: python --version
echo 3. Install dependencies: pip install -r requirements.txt
echo 4. Run app: streamlit run app.py
echo.
echo Streamlit Cloud Documentation:
echo https://docs.streamlit.io/deploy/streamlit-cloud
echo.
echo Press any key to exit...
pause