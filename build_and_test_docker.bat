@echo off
echo Building and testing Psyonic plotting tools Docker container...


echo Step 1: Building Docker image with Python slim base...
docker build -t psyonic-plotting .

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