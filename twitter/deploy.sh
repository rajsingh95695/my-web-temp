#!/bin/bash

# ============================================
# Twitter Sentiment Analysis Platform
# Deployment Script for Linux/Mac
# ============================================

set -e

echo "============================================"
echo "Twitter Sentiment Analysis Platform"
echo "Deployment Script for Linux/Mac"
echo "============================================"
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ ERROR: Docker is not installed or not in PATH."
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if command -v docker-compose &> /dev/null; then
    COMPOSE_COMMAND="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_COMMAND="docker compose"
else
    echo "❌ ERROR: Docker Compose is not available."
    echo "Please install Docker Compose or update Docker Desktop."
    exit 1
fi

echo "✅ Docker and Docker Compose are available."
echo

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        echo "Creating fresh .env file..."
        cat > .env << EOF
RAPIDAPI_KEY=your_api_key_here
DB_PASSWORD=admin123
GRAFANA_PASSWORD=admin123
EOF
    fi
    echo "⚠️  Please edit .env file and add your RapidAPI key."
    echo
fi

# Check if RapidAPI key is set
if grep -q "RAPIDAPI_KEY=your_api_key_here" .env 2>/dev/null || ! grep -q "RAPIDAPI_KEY=" .env 2>/dev/null; then
    echo "⚠️  WARNING: RapidAPI key is not set in .env file."
    echo "The application will not be able to fetch tweets without a valid API key."
    echo "You can get a free API key from: https://rapidapi.com/omarmhaimdat/api/twitter-api45"
    echo
    read -p "Continue without API key? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 0
    fi
fi

# Create necessary directories
echo "Creating required directories..."
mkdir -p logs data reports .streamlit nginx monitoring

# Copy secrets if needed
if [ ! -f .streamlit/secrets.toml ]; then
    echo "Copying secrets template..."
    if [ -f .streamlit/secrets.toml.example ]; then
        cp .streamlit/secrets.toml.example .streamlit/secrets.toml
    else
        echo "Creating secrets.toml..."
        cat > .streamlit/secrets.toml << EOF
[secrets]
RAPIDAPI_KEY = "your_api_key_here"
EOF
    fi
fi

echo
echo "============================================"
echo "Starting Docker Compose Deployment..."
echo "============================================"
echo

# Build and start containers
echo "Step 1: Building Docker images..."
$COMPOSE_COMMAND build --no-cache

if [ $? -ne 0 ]; then
    echo "❌ ERROR: Docker build failed."
    exit 1
fi

echo
echo "Step 2: Starting services..."
$COMPOSE_COMMAND up -d

if [ $? -ne 0 ]; then
    echo "❌ ERROR: Docker Compose failed to start services."
    exit 1
fi

echo
echo "============================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "============================================"
echo
echo "Services running:"
echo
echo "📊 Streamlit App: http://localhost:8501"
echo "🗄️  PostgreSQL: localhost:5432 (user: admin, password: admin123)"
echo "🔥 Redis: localhost:6379"
echo "📈 Grafana: http://localhost:3000 (admin/admin123)"
echo "📊 Prometheus: http://localhost:9090"
echo
echo "Useful commands:"
echo "- View logs: $COMPOSE_COMMAND logs -f"
echo "- Stop services: $COMPOSE_COMMAND down"
echo "- Restart app: $COMPOSE_COMMAND restart twitter-sentiment-app"
echo "- Check status: $COMPOSE_COMMAND ps"
echo
echo "To update the application:"
echo "1. Make your changes to app.py"
echo "2. Run: $COMPOSE_COMMAND build --no-cache"
echo "3. Run: $COMPOSE_COMMAND up -d"
echo
echo "Waiting for services to be ready..."
sleep 10

# Check if services are running
echo
echo "Checking service status..."
$COMPOSE_COMMAND ps

echo
echo "🎉 Deployment successful! Open http://localhost:8501 in your browser."