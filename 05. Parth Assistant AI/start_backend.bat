@echo off
title PARTH ASSISTANT AI — Backend Server
echo ============================================
echo  PARTH ASSISTANT AI Backend Starting...
echo  URL: http://localhost:8000
echo  Health: http://localhost:8000/api/health
echo ============================================
cd /d "%~dp0"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
pause
