@echo off
echo Starting ASMg and DeviceClientApp...

:: Start ASMg
start cmd /k "cd %~dp0 && python run.py"

:: Start DeviceClientApp
start cmd /k "cd %~dp0\..\DeviceClientApp && python device_client_app.py"

echo Both applications started! 