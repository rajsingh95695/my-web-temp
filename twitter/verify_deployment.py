#!/usr/bin/env python3
"""
Deployment Verification Script
Checks if all required deployment files are properly created.
"""

import os
import sys
import yaml
import json
from pathlib import Path

REQUIRED_FILES = [
    "Dockerfile",
    "docker-compose.yml",
    "deploy.bat",
    "deploy.sh",
    ".env.example",
    "DEPLOYMENT_GUIDE.md",
    "requirements.txt",
    "app.py",
    ".streamlit/secrets.toml",
    "init-db.sql",
    "monitoring/prometheus.yml"
]

REQUIRED_DIRS = [
    "nginx",
    "monitoring",
    "data",
    "logs",
    "reports",
    ".streamlit"
]

def check_file_exists(filepath):
    """Check if a file exists and is readable."""
    path = Path(filepath)
    if not path.exists():
        return False, f"❌ Missing: {filepath}"
    
    if not path.is_file():
        return False, f"❌ Not a file: {filepath}"
    
    try:
        if path.stat().st_size == 0:
            return False, f"❌ Empty file: {filepath}"
    except:
        pass
    
    return True, f"✅ Found: {filepath}"

def check_directory_exists(dirpath):
    """Check if a directory exists."""
    path = Path(dirpath)
    if not path.exists():
        return False, f"❌ Missing directory: {dirpath}"
    
    if not path.is_dir():
        return False, f"❌ Not a directory: {dirpath}"
    
    return True, f"✅ Directory exists: {dirpath}"

def validate_dockerfile():
    """Validate Dockerfile structure."""
    try:
        with open("Dockerfile", "r") as f:
            content = f.read()
        
        checks = [
            ("FROM python", "Python base image"),
            ("COPY requirements.txt", "Requirements copy"),
            ("RUN pip install", "Dependency installation"),
            ("EXPOSE 8501", "Port exposure"),
            ("CMD streamlit", "Streamlit command")
        ]
        
        results = []
        for check, desc in checks:
            if check in content:
                results.append(f"✅ {desc}")
            else:
                results.append(f"❌ Missing {desc}")
        
        return results
    except Exception as e:
        return [f"❌ Error reading Dockerfile: {str(e)}"]

def validate_docker_compose():
    """Validate docker-compose.yml structure."""
    try:
        with open("docker-compose.yml", "r") as f:
            content = yaml.safe_load(f)
        
        checks = []
        
        # Check required services
        required_services = ["twitter-sentiment-app", "postgres", "redis"]
        for service in required_services:
            if service in content.get("services", {}):
                checks.append(f"✅ Service: {service}")
            else:
                checks.append(f"❌ Missing service: {service}")
        
        # Check ports
        app_service = content.get("services", {}).get("twitter-sentiment-app", {})
        if "ports" in app_service and "8501:8501" in str(app_service["ports"]):
            checks.append("✅ Port mapping correct")
        else:
            checks.append("❌ Port mapping missing or incorrect")
        
        return checks
    except Exception as e:
        return [f"❌ Error reading docker-compose.yml: {str(e)}"]

def validate_requirements():
    """Validate requirements.txt."""
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
        
        required_packages = ["streamlit", "requests", "plotly", "vaderSentiment", "pandas"]
        checks = []
        
        for package in required_packages:
            if package.lower() in content.lower():
                checks.append(f"✅ Package: {package}")
            else:
                checks.append(f"❌ Missing package: {package}")
        
        return checks
    except Exception as e:
        return [f"❌ Error reading requirements.txt: {str(e)}"]

def validate_app_py():
    """Validate app.py structure."""
    try:
        with open("app.py", "r") as f:
            content = f.read()
        
        checks = []
        
        # Check for key components
        key_components = [
            ("import streamlit", "Streamlit import"),
            ("analyze_sentiment", "Sentiment analysis function"),
            ("st.title", "Streamlit title"),
            ("st.slider", "Tweet limit slider"),
            ("st.button", "Analyze button"),
            ("plotly", "Plotly visualization"),
            ("RAPIDAPI_KEY", "API key usage")
        ]
        
        for component, desc in key_components:
            if component in content:
                checks.append(f"✅ {desc}")
            else:
                checks.append(f"❌ Missing {desc}")
        
        return checks
    except Exception as e:
        return [f"❌ Error reading app.py: {str(e)}"]

def main():
    """Main verification function."""
    print("=" * 60)
    print("Twitter Sentiment Analysis Platform - Deployment Verification")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Check directories
    print("📁 Checking directories...")
    for dirpath in REQUIRED_DIRS:
        passed, message = check_directory_exists(dirpath)
        print(f"  {message}")
        if not passed:
            all_passed = False
    
    print()
    
    # Check files
    print("📄 Checking files...")
    for filepath in REQUIRED_FILES:
        passed, message = check_file_exists(filepath)
        print(f"  {message}")
        if not passed:
            all_passed = False
    
    print()
    
    # Validate Dockerfile
    print("🐳 Validating Dockerfile...")
    docker_checks = validate_dockerfile()
    for check in docker_checks:
        print(f"  {check}")
        if "❌" in check:
            all_passed = False
    
    print()
    
    # Validate docker-compose.yml
    print("🐳 Validating docker-compose.yml...")
    compose_checks = validate_docker_compose()
    for check in compose_checks:
        print(f"  {check}")
        if "❌" in check:
            all_passed = False
    
    print()
    
    # Validate requirements.txt
    print("📦 Validating requirements.txt...")
    req_checks = validate_requirements()
    for check in req_checks:
        print(f"  {check}")
        if "❌" in check:
            all_passed = False
    
    print()
    
    # Validate app.py
    print("📱 Validating app.py...")
    app_checks = validate_app_py()
    for check in app_checks:
        print(f"  {check}")
        if "❌" in check:
            all_passed = False
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("🎉 DEPLOYMENT VERIFICATION PASSED!")
        print("All deployment files are properly created and configured.")
        print()
        print("Next steps:")
        print("1. Edit .env file with your RapidAPI key")
        print("2. Run: deploy.bat (Windows) or ./deploy.sh (Linux/Mac)")
        print("3. Access the app at http://localhost:8501")
        return 0
    else:
        print("⚠️  DEPLOYMENT VERIFICATION FAILED!")
        print("Some files are missing or incorrectly configured.")
        print("Please check the errors above and fix them.")
        return 1

if __name__ == "__main__":
    sys.exit(main())