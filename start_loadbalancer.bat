@echo off
echo Starting Load Balancer on Port 9000...
echo.
echo Choose Load Balancing Algorithm:
echo 1. Round Robin
echo 2. Least Connections
echo 3. Weighted
echo 4. Least Response Time
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    set ALGORITHM=round_robin
    echo Starting with Round Robin algorithm...
) else if "%choice%"=="2" (
    set ALGORITHM=least_connections
    echo Starting with Least Connections algorithm...
) else if "%choice%"=="3" (
    set ALGORITHM=weighted
    echo Starting with Weighted algorithm...
) else if "%choice%"=="4" (
    set ALGORITHM=least_response_time
    echo Starting with Least Response Time algorithm...
) else (
    echo Invalid choice. Using Round Robin as default.
    set ALGORITHM=round_robin
)

set LB_ID=load_balancer_main
set LB_PORT=9000

start "Load Balancer - Port 9000" cmd /k "set LB_ID=%LB_ID% && set LB_PORT=%LB_PORT% && set ALGORITHM=%ALGORITHM% && python load_balancer.py"

echo.
echo Load Balancer started on port 9000!
echo Dashboard should connect to http://localhost:9000
echo.
pause