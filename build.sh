#!/bin/bash

# Psyonic Plotting Tools Build Script
# This script builds the Docker image and extracts the executable

set -e  # Exit on any error

echo "🚀 Building Psyonic Plotting Tools..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build the Docker image
print_status "Building Docker image..."
docker build -t psyonic-plotting-tools .

if [ $? -ne 0 ]; then
    print_error "Docker build failed!"
    exit 1
fi

print_status "Docker image built successfully!"

# Extract the executable from the container
print_status "Extracting executable from container..."
docker run --rm -v $(pwd):/host psyonic-plotting-tools /bin/bash -c "cp /app/dist/plot-lines /host/dist"

if [ $? -ne 0 ]; then
    print_error "Failed to extract executable from container!"
    exit 1
fi

# Check if the executable was created
if [ -f "./plot-lines" ]; then
    print_status "Executable extracted successfully!"
    print_status "File: $(pwd)/plot-lines"
    
    # Make it executable
    chmod +x ./plot-lines
    
    # Show file info
    echo ""
    print_status "File information:"
    ls -lh ./plot-lines
    
    echo ""
    print_status "Build completed successfully! 🎉"
    print_status "You can now run: ./plot-lines"
    
else
    print_error "Executable not found after extraction!"
    exit 1
fi

# Optional: Clean up Docker image (uncomment if you want to save space)
# print_warning "Cleaning up Docker image..."
# docker rmi psyonic-plotting-tools
# print_status "Docker image removed." 