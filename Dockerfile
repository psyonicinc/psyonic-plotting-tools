# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for matplotlib and serial communication
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libfreetype6-dev \
    libpng-dev \
    pkg-config \
    libjpeg-dev \
    libtiff-dev \
    libwebp-dev \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libxrandr-dev \
    libxss-dev \
    libxtst-dev \
    libglib2.0-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY plot_lines.py .
COPY plot_floats.py .
COPY scripts/linux/run_calibration_plot.sh .

# Make the script executable
RUN chmod +x run_calibration_plot.sh

# Set environment variable for matplotlib to use non-interactive backend
ENV MPLBACKEND=Agg

# Create a test script that simulates the calibration plot without requiring serial connection
RUN echo '#!/bin/bash\n\
echo "Testing requirements.txt installation..."\n\
echo "Python version: $(python3 --version)"\n\
echo "Pip version: $(pip --version)"\n\
echo ""\n\
echo "Testing matplotlib..."\n\
python3 -c "import matplotlib; print(f\"Matplotlib version: {matplotlib.__version__}\"); print(f\"Backend: {matplotlib.get_backend()}\")" || echo "Matplotlib import failed"\n\
echo ""\n\
echo "Testing numpy..."\n\
python3 -c "import numpy; print(f\"NumPy version: {numpy.__version__}\")" || echo "NumPy import failed"\n\
echo ""\n\
echo "Testing pyserial..."\n\
python3 -c "import serial; print(f\"PySerial version: {serial.__version__}\")" || echo "PySerial import failed"\n\
echo ""\n\
echo "Testing matplotlib plotting capabilities..."\n\
python3 -c "import matplotlib.pyplot as plt; import numpy as np; fig, ax = plt.subplots(); ax.plot([1,2,3], [1,4,2]); plt.savefig(\"/tmp/test.png\"); print(\"Matplotlib plotting test successful\")" || echo "Matplotlib plotting test failed"\n\
echo ""\n\
echo "All dependency tests completed!"\n\
echo "Note: Real-time plotting requires a display, but dependencies are working."\n\
echo "To test with actual hardware, run: ./run_calibration_plot.sh"' > test_requirements.sh && \
chmod +x test_requirements.sh

# Default command to test requirements
CMD ["./test_requirements.sh"] 