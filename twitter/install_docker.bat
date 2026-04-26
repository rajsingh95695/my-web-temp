@echo off
echo ============================================
echo Docker Installation Guide for Windows
echo Twitter Sentiment Analysis Platform
echo ============================================
echo.

echo This script will help you install Docker Desktop on Windows.
echo.
echo PREREQUISITES:
echo 1. Windows 10/11 64-bit: Pro, Enterprise, or Education
echo 2. At least 4GB RAM (8GB recommended)
echo 3. Hardware Virtualization enabled in BIOS
echo 4. Administrator privileges
echo.

echo Checking system requirements...
echo.

REM Check Windows version
ver | findstr /i "10 11" >nul
if errorlevel 1 (
    echo ❌ ERROR: Windows 10 or 11 is required.
    echo Your Windows version:
    ver
    pause
    exit /b 1
) else (
    echo ✅ Windows version compatible
)

REM Check architecture
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo ✅ 64-bit system detected
) else (
    echo ❌ ERROR: 64-bit Windows is required for Docker.
    echo Your architecture: %PROCESSOR_ARCHITECTURE%
    pause
    exit /b 1
)

REM Check RAM (approximate)
wmic computersystem get TotalPhysicalMemory | findstr /v "TotalPhysicalMemory" > temp_ram.txt
set /p RAM=<temp_ram.txt
del temp_ram.txt
set /a RAM_GB=%RAM%/1073741824
echo ✅ System RAM: %RAM_GB% GB

if %RAM_GB% LSS 4 (
    echo ⚠️  WARNING: Minimum 4GB RAM recommended for Docker
)

echo.
echo ============================================
echo Step 1: Enable Hardware Virtualization
echo ============================================
echo.
echo Hardware Virtualization (VT-x/AMD-V) must be enabled in BIOS.
echo.
echo To check if it's enabled:
echo 1. Press Ctrl+Shift+Esc to open Task Manager
echo 2. Go to Performance tab
echo 3. Look for "Virtualization: Enabled"
echo.
echo If it shows "Disabled", you need to:
echo 1. Restart your computer
echo 2. Enter BIOS/UEFI settings (usually F2, F10, Del, or Esc during boot)
echo 3. Enable Intel VT-x or AMD-V
echo 4. Save and exit
echo.
pause

echo.
echo ============================================
echo Step 2: Install Docker Desktop
echo ============================================
echo.
echo There are two installation methods:
echo.
echo METHOD A: Automatic Download (Recommended)
echo   - This script will download Docker Desktop installer
echo   - File size: ~600MB
echo   - Requires internet connection
echo.
echo METHOD B: Manual Download
echo   - Download from: https://www.docker.com/products/docker-desktop/
echo   - Run the installer manually
echo.
choice /c AB /m "Choose installation method (A/B):"
if errorlevel 2 goto manual_download

:auto_download
echo.
echo Downloading Docker Desktop installer...
echo This may take a few minutes depending on your internet speed...
echo.

REM Download Docker Desktop installer
powershell -Command "Invoke-WebRequest -Uri 'https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe' -OutFile 'DockerDesktopInstaller.exe'"

if exist DockerDesktopInstaller.exe (
    echo ✅ Download complete!
    echo File: DockerDesktopInstaller.exe
    echo Size: %~z1 bytes
    echo.
) else (
    echo ❌ Download failed.
    echo Please download manually from: https://www.docker.com/products/docker-desktop/
    goto manual_download
)

echo Proceeding with installation...
echo.
goto install_docker

:manual_download
echo.
echo ============================================
echo Manual Installation Instructions
echo ============================================
echo.
echo 1. Open your web browser
echo 2. Go to: https://www.docker.com/products/docker-desktop/
echo 3. Click "Download for Windows"
echo 4. Run the downloaded installer (Docker Desktop Installer.exe)
echo 5. Follow the installation wizard
echo.
echo Installation steps:
echo   - Accept the terms
echo   - Enable WSL 2 (recommended)
echo   - Add shortcut to desktop (optional)
echo   - Click "Install"
echo   - Restart when prompted
echo.
echo After installation, return to this script and press any key...
pause
goto verify_installation

:install_docker
echo ============================================
echo Running Docker Desktop Installer
echo ============================================
echo.
echo The installer will now run. Please follow these steps:
echo.
echo 1. Accept the Docker Subscription Service Agreement
echo 2. Check "Use WSL 2 instead of Hyper-V" (recommended)
echo 3. Click "OK" to install required Windows components
echo 4. Wait for installation to complete
echo 5. Click "Close and restart" when prompted
echo.
echo IMPORTANT: Your computer will restart after installation.
echo Save any open work before continuing.
echo.
pause

echo Starting installer...
start /wait DockerDesktopInstaller.exe

echo.
echo ============================================
echo Post-Installation Setup
echo ============================================
echo.
echo After your computer restarts:
echo 1. Docker Desktop will start automatically
echo 2. Accept the terms if prompted
echo 3. Wait for Docker to initialize (may take a few minutes)
echo 4. You'll see a "Docker is running" notification
echo.
echo Press any key after Docker Desktop is running...
pause

:verify_installation
echo.
echo ============================================
echo Verifying Docker Installation
echo ============================================
echo.
echo Checking Docker version...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker not found in PATH.
    echo Trying alternative locations...
    
    REM Check common Docker installation paths
    if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
        echo ✅ Docker found in Program Files
        setx PATH "%PATH%;C:\Program Files\Docker\Docker\resources\bin"
        echo Added Docker to PATH. Please restart command prompt.
    ) else if exist "%LOCALAPPDATA%\Docker\resources\bin\docker.exe" (
        echo ✅ Docker found in AppData
        setx PATH "%PATH%;%LOCALAPPDATA%\Docker\resources\bin"
        echo Added Docker to PATH. Please restart command prompt.
    ) else (
        echo ❌ Docker not found. Please ensure installation completed successfully.
        echo Try running Docker Desktop manually from Start Menu.
        pause
        exit /b 1
    )
) else (
    docker --version
    echo ✅ Docker is installed and in PATH!
)

echo.
echo Checking Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Docker Compose not found (will use docker compose command)
    ) else (
        echo ✅ Docker Compose (docker compose) is available
    )
) else (
    docker-compose --version
    echo ✅ Docker Compose is available
)

echo.
echo Testing Docker with a simple command...
docker run --rm hello-world >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Docker test failed. Docker might not be running.
    echo Please ensure Docker Desktop is running.
    echo.
    echo To start Docker Desktop:
    echo 1. Search for "Docker Desktop" in Start Menu
    echo 2. Run it and wait for the whale icon in system tray
    echo 3. Try again after Docker is running
) else (
    echo ✅ Docker test successful! Hello-world container ran correctly.
)

echo.
echo ============================================
echo Docker Installation Complete!
echo ============================================
echo.
echo ✅ Docker is now installed on your system.
echo.
echo Next steps for Twitter Sentiment Analysis Platform:
echo 1. Ensure Docker Desktop is running (whale icon in system tray)
echo 2. Open a NEW command prompt (to refresh PATH)
echo 3. Navigate to your project folder:
echo    cd /d "c:\Users\rajsi\OneDrive\Desktop\ScienceKit\twitter"
echo 4. Run the deployment script:
echo    deploy.bat
echo.
echo Troubleshooting tips:
echo - If Docker commands fail, restart Docker Desktop
echo - If WSL 2 issues occur, run: wsl --update
echo - For network issues, check Docker Desktop settings
echo - Ensure Windows Subsystem for Linux is enabled
echo.
echo For more help, visit:
echo - Docker Docs: https://docs.docker.com/desktop/
echo - WSL 2 Setup: https://docs.microsoft.com/en-us/windows/wsl/install
echo.
echo Press any key to exit...
pause

REM Cleanup
if exist DockerDesktopInstaller.exe (
    echo.
    echo Cleaning up installer file...
    del DockerDesktopInstaller.exe
    echo Installer removed.
)