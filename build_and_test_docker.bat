@echo off
echo Building and testing Psyonic plotting tools Docker container...

echo.
echo Choose Dockerfile to use:
echo 1. Python slim base (faster, smaller)
echo 2. Ubuntu base (more compatible, larger)
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Step 1: Building Docker image with Python slim base...
    docker build -t psyonic-plotting .
) else if "%choice%"=="2" (
    echo.
    echo Step 1: Building Docker image with Ubuntu base...
    docker build -f Dockerfile.alternative -t psyonic-plotting .
) else (
    echo Invalid choice. Using default Python slim base...
    docker build -t psyonic-plotting .
)

if %ERRORLEVEL% NEQ 0 (
    echo Error: Docker build failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Testing requirements.txt installation...
docker run --rm psyonic-plotting

if %ERRORLEVEL% NEQ 0 (
    echo Error: Container test failed!
    pause
    exit /b 1
)

echo.
echo Success! All dependencies are working correctly.
echo.
echo To run the actual calibration plot script (requires hardware):
echo docker run --rm -v /dev:/dev psyonic-plotting ./run_calibration_plot.sh
echo.
pause 