# Updated Docker Build for Psyonic Plotting Tools

## Overview
This Dockerfile has been updated to properly handle PyInstaller builds for the plotting software that uses matplotlib animations and serial communication.

## Key Improvements

### 1. Additional System Dependencies
Added comprehensive X11 and display libraries needed for matplotlib:
- **Graphics libraries**: `libgl1-mesa-glx`, `libxkbcommon-x11`, etc.
- **Image format support**: `libpng16-16`, `libjpeg-turbo8`, `libtiff5`, etc.
- **Font rendering**: `libharfbuzz0b`, `libfribidi0`, `libpango-1.0-0`, etc.
- **GUI frameworks**: `libgtk-3-0`, `libatk1.0-0`, `libgdk-3-0`, etc.
- **Audio/Device support**: `libasound2`, `libpulse0`, `libudev1`, `libusb-1.0-0`

### 2. Enhanced Python Dependencies
- Added `pyinstaller-hooks-contrib` for better PyInstaller compatibility
- Updated requirements.txt with additional dependencies

### 3. PyInstaller Configuration
- Created `plot-lines.spec` file for better control over the build process
- Added explicit hidden imports for matplotlib backends and animation
- Included all necessary numpy and serial dependencies

### 4. Dependency Testing
- Added `test_dependencies.py` to verify all dependencies are properly installed
- Tests run before PyInstaller build to catch issues early

## Files Added/Modified

### New Files:
- `plot-lines.spec` - PyInstaller specification file
- `test_dependencies.py` - Dependency verification script
- `README_Docker_Updated.md` - This documentation

### Modified Files:
- `Dockerfile` - Enhanced with additional dependencies and testing
- `requirements.txt` - Added pyinstaller-hooks-contrib

## Usage

### Building the Docker Image
```bash
docker build -t psyonic-plotting-tools .
```

### Running the Container
```bash
docker run -it --rm psyonic-plotting-tools
```

### Testing Dependencies Locally
If you want to test dependencies without building the full Docker image:
```bash
python3 test_dependencies.py
```

## Troubleshooting

### Common Issues:

1. **Matplotlib Backend Errors**
   - The Dockerfile now includes all necessary X11 libraries
   - Multiple backend options are included in the spec file

2. **Serial Port Access**
   - Added `libusb-1.0-0` and `libudev1` for device access
   - Serial tools are explicitly included in hidden imports

3. **Missing Dependencies**
   - Run `test_dependencies.py` to identify specific missing modules
   - Check the test output for detailed error messages

### Debug Mode
To build with console output for debugging:
```bash
# Modify the spec file to change console=False to console=True
# Or use the command line version:
pyinstaller --onefile --console --name plot-lines plot_lines.py
```

## Build Artifacts
The PyInstaller build will create:
- `dist/plot-lines` - The final executable
- `build/` - Build artifacts (can be cleaned up)
- `plot-lines.spec` - Build specification (keep for future builds)

## Notes
- The build uses the `--windowed` flag to create a GUI application
- All matplotlib backends are included to ensure compatibility across different systems
- The spec file can be modified to customize the build process further 