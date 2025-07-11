# Psyonic Plotting Tools

A collection of Python tools for real-time plotting and data visualization from serial devices.

## Requirements

The project requires the following Python packages (specified in `requirements.txt`):

- `pyserial==3.5` - Serial communication library
- `matplotlib==3.3.2` - Plotting and visualization library
- `numpy==1.21.3` - Numerical computing library

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Repository

```bash
git clone <repository-url>
cd psyonic-plotting-tools
```

Or download and extract the ZIP file to your desired location.

### Step 2: Install Python Dependencies

#### Option A: Install using requirements.txt (Recommended)

```bash
# Install all required packages
pip install -r requirements.txt
```

#### Option B: Install packages individually

```bash
pip install pyserial==3.5
pip install matplotlib==3.3.2
pip install numpy==1.21.3
```

#### Option C: Install in a virtual environment (Recommended for isolation)

```bash
# Create a virtual environment
python -m venv psyonic_env

# Activate the virtual environment
# On Windows:
psyonic_env\Scripts\activate
# On Linux/macOS:
source psyonic_env/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Verify Installation

Test that all packages are installed correctly:

```bash
python -c "import serial; print(f'PySerial version: {serial.__version__}')"
python -c "import matplotlib; print(f'Matplotlib version: {matplotlib.__version__}')"
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
```

## Usage

### plot_lines.py

Main plotting script for real-time data visualization from serial devices.

#### Basic Usage

```bash
python plot_lines.py [options]
```

#### Command Line Options

- `-b, --baud` - Baud rate (default: 115200)
- `-n, --num_lines` - Number of data lines to plot (default: 1)
- `-w, --width` - Buffer width for plotting (default: 100)
- `-t, --timeout` - Serial timeout in milliseconds (default: 1000)
- `--ymin` - Minimum Y-axis value
- `--ymax` - Maximum Y-axis value
- `--scaler` - Data scaling preset (none, cal, peu, fsr, aenc)
- `--passfail` - Enable pass/fail message checking

#### Examples

```bash
# Basic calibration plot
python plot_lines.py -b 230400 -n 4 -w 50 -t 2000 --ymin -183.84 --ymax 183.84 --scaler cal --passfail

# Simple plotting with default settings
python plot_lines.py -b 115200 -n 2

# Custom scaling and limits
python plot_lines.py -b 9600 -n 1 --ymin 0 --ymax 100 --scaler none
```

### plot_floats.py

Utility module for matplotlib-based plotting functions (used by plot_lines.py).

## Scripts

### Linux Scripts

Located in `scripts/linux/`:

- `run_calibration_plot.sh` - Runs the calibration plot with predefined parameters
- `run_fsr_plot.sh` - Runs FSR (Force Sensing Resistor) plotting
- `run_peu_plot.sh` - Runs PEU plotting
- `run_aenc_plot.sh` - Runs AENC plotting
- `install.sh` - Installation script for dependencies

### Windows Scripts

Located in `scripts/windows/`:

- `run_calibration_plot.bat` - Windows version of calibration plot
- `run_fsr_plot.bat` - Windows version of FSR plotting
- `run_peu_plot.bat` - Windows version of PEU plotting
- `run_aenc_plot.bat` - Windows version of AENC plotting
- `install.bat` - Windows installation script

## Quick Start

### Using Linux Scripts

```bash
# Make scripts executable
chmod +x scripts/linux/*.sh

# Run calibration plot
./scripts/linux/run_calibration_plot.sh
```

### Using Windows Scripts

```cmd
# Run calibration plot
scripts\windows\run_calibration_plot.bat
```

### Manual Execution

```bash
# Run with Python directly
python plot_lines.py -b 230400 -n 4 -w 50 -t 2000 --ymin -183.84 --ymax 183.84 --scaler cal --passfail
```

## Hardware Requirements

- USB-to-Serial device or built-in serial port
- Compatible hardware device sending data over serial
- Proper serial port permissions (Linux: add user to dialout group)

### Linux Serial Port Setup

```bash
# Add user to dialout group for serial port access
sudo usermod -a -G dialout $USER

# Log out and back in, or run:
newgrp dialout
```

## Troubleshooting

### Common Issues

1. **Import Error: No module named 'serial'**
   ```bash
   pip install pyserial==3.5
   ```

2. **Import Error: No module named 'matplotlib'**
   ```bash
   pip install matplotlib==3.3.2
   ```

3. **Serial Port Permission Denied (Linux)**
   ```bash
   sudo usermod -a -G dialout $USER
   # Log out and back in
   ```

4. **No Serial Port Found**
   - Check device connections
   - Verify correct port name (Linux: `/dev/ttyUSB0`, Windows: `COM1`)
   - Ensure device drivers are installed

5. **Matplotlib Backend Issues**
   ```bash
   # Set non-interactive backend for headless systems
   export MPLBACKEND=Agg
   ```

### Version Conflicts

If you encounter version conflicts:

```bash
# Upgrade pip first
pip install --upgrade pip

# Install with --force-reinstall if needed
pip install --force-reinstall -r requirements.txt
```

### Virtual Environment Issues

```bash
# Create fresh virtual environment
python -m venv fresh_env
source fresh_env/bin/activate  # Linux/macOS
# or
fresh_env\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt
```

## Development

### Adding New Dependencies

1. Install the new package:
   ```bash
   pip install new_package
   ```

2. Update requirements.txt:
   ```bash
   pip freeze > requirements.txt
   ```

3. Or manually add to requirements.txt:
   ```
   new_package==1.2.3
   ```

### Testing

Test the installation:

```bash
# Test imports
python -c "import serial, matplotlib, numpy; print('All packages imported successfully')"

# Test plotting (no hardware required)
python plot_lines.py --help
```

## License

[Add your license information here]

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the command line help: `python plot_lines.py --help`
- Ensure all dependencies are installed correctly 