# Docker Container for Psyonic Plotting Tools

This Docker container allows you to test the `requirements.txt` dependencies and run the calibration plot script in an isolated environment.

## Quick Start

### Using Docker Compose (Recommended)
```bash
# Build and test the container
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### Using Docker directly
```bash
# Build the image
docker build -t psyonic-plotting .

# Test requirements installation
docker run --rm psyonic-plotting

# Run the actual calibration plot script (requires hardware)
docker run --rm -v /dev:/dev psyonic-plotting ./run_calibration_plot.sh
```

### Using Windows batch script
```cmd
# Run the provided batch script
scripts\windows\build_and_test_docker.bat
```

## What the Container Does

1. **Tests Dependencies**: Verifies that all packages in `requirements.txt` can be installed and imported:
   - `pyserial==3.5`
   - `matplotlib==3.3.2`
   - `numpy==1.21.3`

2. **Provides Runtime Environment**: Sets up a Linux environment with all necessary system dependencies for matplotlib and serial communication.

3. **Enables Hardware Testing**: When connected to actual hardware, you can run the calibration plot script with real-time plotting.

## Container Features

- **Base Image**: Python 3.9 slim (lightweight)
- **System Dependencies**: Includes gcc, g++, and matplotlib dependencies
- **Volume Mounting**: Mounts `/dev` for serial port access
- **Non-interactive Backend**: Uses `Agg` backend for matplotlib to work in headless environments

## Testing Without Hardware

The container includes a test script that verifies all dependencies without requiring actual hardware:

```bash
docker run --rm psyonic-plotting ./test_requirements.sh
```

This will:
- Import all required packages
- Display version information
- Confirm successful installation

## Running with Hardware

To run the actual calibration plot script with hardware:

```bash
# On Linux/macOS
docker run --rm -v /dev:/dev --device=/dev/ttyUSB0 psyonic-plotting ./run_calibration_plot.sh

# On Windows (adjust COM port as needed)
docker run --rm -v /dev:/dev --device=/dev/ttyS0 psyonic-plotting ./run_calibration_plot.sh
```

## Troubleshooting

### Build Issues
- Ensure Docker is installed and running
- Check that all files are in the correct locations
- Verify internet connection for downloading packages

### Runtime Issues
- For serial communication: ensure proper device mounting
- For plotting: the container uses non-interactive backend by default
- For hardware access: ensure proper permissions and device mapping

### Version Conflicts
If you encounter version conflicts, you can modify the `requirements.txt` file and rebuild:

```bash
docker-compose build --no-cache
```

## File Structure

```
psyonic-plotting-tools/
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Docker Compose configuration
├── requirements.txt           # Python dependencies
├── plot_lines.py             # Main plotting script
├── plot_floats.py            # Matplotlib plotting functions
├── scripts/
│   └── windows/
│       └── build_and_test_docker.bat  # Windows build script
└── README_Docker.md          # This file
``` 