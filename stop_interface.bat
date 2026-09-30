@echo off
title Stop Dar es Salaam Agrovet Interface
echo Stopping Agrovet Database Interface on port 8000...
for /f tokens=5 %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /f /pid %%a >nul 2>&1
)
echo Interface stopped successfully.
pause
