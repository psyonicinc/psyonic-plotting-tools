@echo off
echo Running Calibration Lines Plotter
python ..\..\plot_lines.py -b 230400 -n 4 -w 7 --buffer 50 -t 6000 --ymin -0.01 --ymax 0.01 --scaler cal