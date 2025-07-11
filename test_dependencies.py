#!/usr/bin/env python3
"""
Test script to verify all dependencies are properly installed
"""

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import serial
        print("✓ pyserial imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pyserial: {e}")
        return False
    
    try:
        import matplotlib
        print("✓ matplotlib imported successfully")
        print(f"  matplotlib version: {matplotlib.__version__}")
    except ImportError as e:
        print(f"✗ Failed to import matplotlib: {e}")
        return False
    
    try:
        import numpy
        print("✓ numpy imported successfully")
        print(f"  numpy version: {numpy.__version__}")
    except ImportError as e:
        print(f"✗ Failed to import numpy: {e}")
        return False
    
    try:
        from matplotlib import pyplot as plt
        print("✓ matplotlib.pyplot imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import matplotlib.pyplot: {e}")
        return False
    
    try:
        from matplotlib import animation
        print("✓ matplotlib.animation imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import matplotlib.animation: {e}")
        return False
    
    try:
        from serial.tools import list_ports
        print("✓ serial.tools.list_ports imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import serial.tools.list_ports: {e}")
        return False
    
    return True

def test_matplotlib_backend():
    """Test matplotlib backend functionality"""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend for testing
        from matplotlib import pyplot as plt
        
        # Create a simple plot
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 2])
        plt.close(fig)
        print("✓ matplotlib plotting functionality works")
        return True
    except Exception as e:
        print(f"✗ matplotlib plotting failed: {e}")
        return False

def test_serial_ports():
    """Test serial port listing functionality"""
    try:
        from serial.tools import list_ports
        ports = list(list_ports.comports())
        print(f"✓ Serial port listing works, found {len(ports)} ports")
        return True
    except Exception as e:
        print(f"✗ Serial port listing failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing dependencies for plot_lines.py...")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_matplotlib_backend()
    success &= test_serial_ports()
    
    print("=" * 50)
    if success:
        print("✓ All dependency tests passed!")
        print("Your environment should be ready for PyInstaller.")
    else:
        print("✗ Some dependency tests failed.")
        print("Please check the error messages above.") 