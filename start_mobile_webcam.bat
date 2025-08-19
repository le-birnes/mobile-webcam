@echo off
echo ============================================
echo       Starting Mobile Webcam System
echo ============================================
echo.

REM Get IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4" ^| findstr /v "127.0.0.1"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set IP_ADDRESS=%%b
        goto :found_ip
    )
)
:found_ip

echo Starting HTTPS server...
start "Mobile Webcam Server" cmd /k "node webcam_server_https.js"

timeout /t 2 /nobreak >nul

echo Starting Phone-to-OBS bridge...
start "Mobile Webcam Bridge" cmd /k "python phone_obs_rotation.py || py phone_obs_rotation.py"

echo.
echo ============================================
echo       Mobile Webcam is Running!
echo ============================================
echo.
echo On your phone, open browser and go to:
echo.
echo   https://%IP_ADDRESS%:8443/
echo.
echo Accept the security warning (self-signed certificate)
echo Then tap "Start Camera" on your phone
echo.
echo In OBS or any app, select "OBS Virtual Camera"
echo.
echo Press any key to stop all services...
pause >nul

echo.
echo Stopping services...
taskkill /FI "WindowTitle eq Mobile Webcam Server*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Mobile Webcam Bridge*" /T /F >nul 2>&1
echo Services stopped.
pause