@echo off
title Dar es Salaam Agrovet Database Interface
echo ===============================================================
echo Starting Dar es Salaam Agrovet & Veterinary Research Interface
echo ===============================================================
echo Opening web dashboard in default browser at http://127.0.0.1:8000 ...
cd /d %~dp0
start http://127.0.0.1:8000
.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
pause
