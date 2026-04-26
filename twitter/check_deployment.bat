@echo off
echo ============================================
echo Twitter Sentiment Analysis Platform
echo Deployment Files Check
echo ============================================
echo.

echo Checking required files...
echo.

set ALL_OK=1

REM Check main files
if exist Dockerfile (
    echo ✅ Dockerfile found
) else (
    echo ❌ Dockerfile missing
    set ALL_OK=0
)

if exist docker-compose.yml (
    echo ✅ docker-compose.yml found
) else (
    echo ❌ docker-compose.yml missing
    set ALL_OK=0
)

if exist deploy.bat (
    echo ✅ deploy.bat found
) else (
    echo ❌ deploy.bat missing
    set ALL_OK=0
)

if exist deploy.sh (
    echo ✅ deploy.sh found
) else (
    echo ❌ deploy.sh missing
    set ALL_OK=0
)

if exist .env.example (
    echo ✅ .env.example found
) else (
    echo ❌ .env.example missing
    set ALL_OK=0
)

if exist DEPLOYMENT_GUIDE.md (
    echo ✅ DEPLOYMENT_GUIDE.md found
) else (
    echo ❌ DEPLOYMENT_GUIDE.md missing
    set ALL_OK=0
)

if exist requirements.txt (
    echo ✅ requirements.txt found
) else (
    echo ❌ requirements.txt missing
    set ALL_OK=0
)

if exist app.py (
    echo ✅ app.py found
) else (
    echo ❌ app.py missing
    set ALL_OK=0
)

if exist init-db.sql (
    echo ✅ init-db.sql found
) else (
    echo ❌ init-db.sql missing
    set ALL_OK=0
)

REM Check directories
echo.
echo Checking directories...

if exist .streamlit (
    echo ✅ .streamlit directory found
) else (
    echo ❌ .streamlit directory missing
    set ALL_OK=0
)

if exist monitoring (
    echo ✅ monitoring directory found
) else (
    echo ❌ monitoring directory missing
    set ALL_OK=0
)

if exist nginx (
    echo ✅ nginx directory found
) else (
    echo ❌ nginx directory missing
    set ALL_OK=0
)

REM Check .streamlit/secrets.toml
if exist .streamlit\secrets.toml (
    echo ✅ .streamlit/secrets.toml found
) else (
    echo ⚠️  .streamlit/secrets.toml missing (will be created by deploy script)
)

REM Check monitoring/prometheus.yml
if exist monitoring\prometheus.yml (
    echo ✅ monitoring/prometheus.yml found
) else (
    echo ❌ monitoring/prometheus.yml missing
    set ALL_OK=0
)

echo.
echo ============================================
if %ALL_OK%==1 (
    echo ✅ ALL DEPLOYMENT FILES ARE READY!
    echo.
    echo Next steps:
    echo 1. Edit .env file with your RapidAPI key
    echo 2. Run deploy.bat to start the application
    echo 3. Access the app at http://localhost:8501
) else (
    echo ⚠️  SOME FILES ARE MISSING
    echo Please check the errors above and create missing files.
)
echo ============================================
echo.

REM Show file sizes for key files
echo File sizes:
for %%f in (Dockerfile docker-compose.yml app.py requirements.txt) do (
    if exist %%f (
        for %%i in (%%f) do set size=%%~zi
        set /a size_kb=!size!/1024
        echo   %%f: !size_kb! KB
    )
)

echo.
pause