@echo off
title Distributed Load Balancer - Complete System (Port 9000)
color 0A

echo ========================================
echo   Distributed Load Balancer System
echo   Load Balancer Port: 9000
echo ========================================
echo.

echo Step 1: Starting Backend Servers...
start "Backend Server 1" cmd /k "set SERVER_ID=backend_1 && set SERVER_PORT=5001 && python backend_server.py"
timeout /t 2 /nobreak > nul

start "Backend Server 2" cmd /k "set SERVER_ID=backend_2 && set SERVER_PORT=5002 && python backend_server.py"
timeout /t 2 /nobreak > nul

start "Backend Server 3" cmd /k "set SERVER_ID=backend_3 && set SERVER_PORT=5003 && python backend_server.py"
timeout /t 2 /nobreak > nul

echo.
echo Step 2: Starting Load Balancer on Port 9000...
set LB_ID=load_balancer_main
set LB_PORT=9000
set ALGORITHM=round_robin

start "Load Balancer - Port 9000" cmd /k "set LB_ID=%LB_ID% && set LB_PORT=%LB_PORT% && set ALGORITHM=%ALGORITHM% && python load_balancer.py"
timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo   System Ready!
echo ========================================
echo.
echo Backend Servers: http://localhost:5001, 5002, 5003
echo Load Balancer:   http://localhost:9000
echo Dashboard:       Open dashboard.html in browser
echo.
echo Testing Load Balancer connection...
timeout /t 2 /nobreak > nul

curl http://localhost:9000/health 2>nul
if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Load Balancer is responding on port 9000
) else (
    echo.
    echo WARNING: Load Balancer may not be ready yet. Wait 10 seconds and open dashboard.
)

echo.
echo Now open dashboard.html in your browser!
echo.
pause