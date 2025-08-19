@echo off
echo ============================================
echo    Mobile Webcam Installer for Windows
echo ============================================
echo.

REM Check for Python
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python is not installed!
        echo Please install Python from https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)
echo [OK] Python found

REM Check for Node.js
echo Checking for Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js found

REM Check for OpenSSL
echo Checking for OpenSSL...
where openssl >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] OpenSSL not found in PATH
    echo Trying Git's OpenSSL...
    if exist "C:\Program Files\Git\usr\bin\openssl.exe" (
        set PATH=%PATH%;C:\Program Files\Git\usr\bin
        echo [OK] Found OpenSSL in Git installation
    ) else (
        echo [WARNING] OpenSSL not found - you'll need to generate certificates manually
    )
) else (
    echo [OK] OpenSSL found
)

echo.
echo Installing Python dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Installing Node.js dependencies...
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo.
echo Checking for OBS Virtual Camera...
%PYTHON_CMD% -c "import pyvirtualcam; cam = pyvirtualcam.Camera(width=640, height=480, fps=30, device='OBS Virtual Camera'); cam.close(); print('[OK] OBS Virtual Camera detected')" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] OBS Virtual Camera not detected!
    echo Please install OBS Studio and OBS Virtual Camera plugin
    echo Download from: https://obsproject.com/
    echo.
)

echo.
echo Generating SSL certificates...
if exist server.key (
    echo [INFO] SSL certificates already exist
) else (
    where openssl >nul 2>&1
    if %errorlevel% equ 0 (
        echo Creating self-signed certificate...
        openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.cert -days 365 -nodes -subj "/CN=localhost"
        if exist server.key (
            echo [OK] SSL certificates generated
        ) else (
            echo [WARNING] Failed to generate certificates
            echo You'll need to create them manually
        )
    ) else (
        echo [WARNING] Cannot generate certificates without OpenSSL
        echo You'll need to create them manually
    )
)

echo.
echo ============================================
echo    Installation Complete!
echo ============================================
echo.
echo To start Mobile Webcam:
echo 1. Run: start_mobile_webcam.bat
echo    Or manually:
echo    - Terminal 1: node webcam_server_https.js
echo    - Terminal 2: python phone_obs_rotation.py
echo.
echo 2. On your phone, open browser and go to:
echo    https://YOUR_PC_IP:8443/
echo.
echo Your PC's IP addresses:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do echo   %%a
echo.
pause