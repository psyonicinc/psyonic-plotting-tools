# Alternative Dockerfile using ubuntu base image
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    build-essential \
    libgl1-mesa-glx \
    libxrender1 \
    libxext6 \
    libsm6 \
    libx11-6 \
    libfontconfig1 \
    libfreetype6 \
    libpng16-16 \
    libjpeg-turbo8 \
    libtiff5 \
    libopenjp2-7 \
    libxcb1 \
    libxkbcommon0 \
    libatk1.0-0 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libudev1 \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir -r requirements.txt

# Install PyInstaller and additional dependencies needed for matplotlib
RUN pip3 install pyinstaller
RUN pip3 install pyinstaller-hooks-contrib

# Copy the application files
COPY plot_lines.py .
COPY plot_floats.py .
COPY plot-lines.spec .

# Build using the spec file for better control
RUN pyinstaller plot-lines.spec --clean

CMD ["./dist/plot-lines"] 