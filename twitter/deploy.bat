@echo off
echo ============================================
echo Twitter Sentiment Analysis Platform
echo Deployment Script for Windows
echo ============================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Docker is not installed or not in PATH.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ WARNING: docker-compose not found, trying docker compose...
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo ❌ ERROR: Docker Compose is not available.
        echo Please install Docker Compose or update Docker Desktop.
        pause
        exit /b 1
    )
    set COMPOSE_COMMAND=docker compose
) else (
    set COMPOSE_COMMAND=docker-compose
)

echo ✅ Docker and Docker Compose are available.
echo.

REM Create environment file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env >nul 2>&1
    if errorlevel 1 (
        echo Creating fresh .env file...
        echo RAPIDAPI_KEY=your_api_key_here > .env
        echo DB_PASSWORD=admin123 >> .env
        echo GRAFANA_PASSWORD=admin123 >> .env
    )
    echo ⚠️ Please edit .env file and add your RapidAPI key.
    echo.
)

REM Check if RapidAPI key is set
setlocal enabledelayedexpansion
set KEY_SET=0
for /f "tokens=2 delims==" %%a in ('findstr "RAPIDAPI_KEY" .env 2^>nul') do (
    if not "%%a"=="your_api_key_here" (
        set KEY_SET=1
    )
)

if !KEY_SET!==0 (
    echo ⚠️ WARNING: RapidAPI key is not set in .env file.
    echo The application will not be able to fetch tweets without a valid API key.
    echo You can get a free API key from: https://rapidapi.com/omarmhaimdat/api/twitter-api45
    echo.
    choice /c YN /m "Continue without API key? (Y/N)"
    if errorlevel 2 (
        echo Deployment cancelled.
        pause
        exit /b 0
    )
)

REM Create necessary directories
echo Creating required directories...
mkdir logs 2>nul
mkdir data 2>nul
mkdir reports 2>nul
mkdir .streamlit 2>nul

REM Copy secrets if needed
if not exist .streamlit\secrets.toml (
    echo Copying secrets template...
    copy .streamlit\secrets.toml.example .streamlit\secrets.toml 2>nul
    if errorlevel 1 (
        echo Creating secrets.toml...
        echo [secrets] > .streamlit\secrets.toml
        echo RAPIDAPI_KEY = "your_api_key_here" >> .streamlit\secrets.toml
    )
)

echo.
echo ============================================
echo Starting Docker Compose Deployment...
echo ============================================
echo.

REM Build and start containers
echo Step 1: Building Docker images...
%COMPOSE_COMMAND% build --no-cache

if errorlevel 1 (
    echo ❌ ERROR: Docker build failed.
    pause
    exit /b 1
)

echo.
echo Step 2: Starting services...
%COMPOSE_COMMAND% up -d

if errorlevel 1 (
    echo ❌ ERROR: Docker Compose failed to start services.
    pause
    exit /b 1
)

echo.
echo ============================================
echo ✅ DEPLOYMENT COMPLETE!
echo ============================================
echo.
echo Services running:
echo.
echo 📊 Streamlit App: http://localhost:8501
echo 🗄️  PostgreSQL: localhost:5432 (user: admin, password: admin123)
echo 🔥 Redis: localhost:6379
echo 📈 Grafana: http://localhost:3000 (admin/admin123)
echo 📊 Prometheus: http://localhost:9090
echo.
echo Useful commands:
echo - View logs: %COMPOSE_COMMAND% logs -f
echo - Stop services: %COMPOSE_COMMAND% down
echo - Restart app: %COMPOSE_COMMAND% restart twitter-sentiment-app
echo - Check status: %COMPOSE_COMMAND% ps
echo.
echo To update the application:
echo 1. Make your changes to app.py
echo 2. Run: %COMPOSE_COMMAND% build --no-cache
echo 3. Run: %COMPOSE_COMMAND% up -d
echo.
pause