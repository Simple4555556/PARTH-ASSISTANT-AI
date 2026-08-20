@echo off
title PARTH ASSISTANT AI — Full Stack Launcher
echo ============================================
echo  PARTH ASSISTANT AI — Full Stack Launch
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:5173
echo ============================================

cd /d "%~dp0"

:: Start backend in a new window
start "PARTH Backend" cmd /k "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

:: Wait 3 seconds for backend to boot
timeout /t 3 /nobreak > nul

:: Start frontend in a new window
start "PARTH Frontend" cmd /k "cd frontend && npm run dev"

:: Open browser
timeout /t 4 /nobreak > nul
start http://localhost:5173

echo.
echo Both servers are starting in separate windows.
echo Open http://localhost:5173 in your browser.
pause
