@echo off
echo Starting Backend Servers...
echo.

start "Backend Server 1" cmd /k "set SERVER_ID=backend_1 && set SERVER_PORT=5001 && python backend_server.py"
timeout /t 2 /nobreak > nul

start "Backend Server 2" cmd /k "set SERVER_ID=backend_2 && set SERVER_PORT=5002 && python backend_server.py"
timeout /t 2 /nobreak > nul

start "Backend Server 3" cmd /k "set SERVER_ID=backend_3 && set SERVER_PORT=5003 && python backend_server.py"
timeout /t 2 /nobreak > nul

echo.
echo All backend servers started!
echo Check the opened windows for server status.
pause