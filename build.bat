@echo off
REM Psyonic Plotting Tools Build Script for Windows
REM This script builds the Docker image and extracts the executable

echo 🚀 Building Psyonic Plotting Tools...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Build the Docker image
echo [INFO] Building Docker image...
docker build -t psyonic-plotting-tools .

if %errorlevel% neq 0 (
    echo [ERROR] Docker build failed!
    exit /b 1
)

echo [INFO] Docker image built successfully!

REM Extract the executable from the container
echo [INFO] Extracting executable from container...
docker run --rm -v "%cd%:/host" psyonic-plotting-tools /bin/bash -c "cp /app/dist/plot-lines /host/dist"

if %errorlevel% neq 0 (
    echo [ERROR] Failed to extract executable from container!
    exit /b 1
)

REM Check if the executable was created
if exist "dist/plot-lines" (
    echo [INFO] Executable extracted successfully!
    echo [INFO] File: %cd%\dist\plot-lines
    
    REM Show file info
    echo.
    echo [INFO] File information:
    dir plot-lines
    
    echo.
    echo [INFO] Build completed successfully!
    echo [INFO] You can now run: plot-lines
    
) else (
    echo [ERROR] Executable not found after extraction!
    exit /b 1
)

REM Optional: Clean up Docker image (uncomment if you want to save space)
REM echo [WARNING] Cleaning up Docker image...
REM docker rmi psyonic-plotting-tools
REM echo [INFO] Docker image removed.

pause