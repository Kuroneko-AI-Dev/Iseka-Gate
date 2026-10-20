@echo off
title Isekai Live

echo ==============================
echo   STARTING ISEKAI LIVE
echo ==============================

echo.
echo [1/3] Starting Backend...
start "Backend - Port 8000" cmd /k "cd /d "%~dp0backend" && call "%~dp0venv\Scripts\activate.bat" && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo [2/3] Starting Supertone...
start "Supertone - Port 9000" cmd /k "cd /d "%~dp0supertone" && call venv\Scripts\activate.bat && uvicorn app:app --host 0.0.0.0 --port 9000 --reload"

echo.
echo [3/3] Starting Frontend...
start "Frontend - Vite" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ==============================
echo   SEMUA SERVER SUDAH DIMULAI
echo ==============================

pause