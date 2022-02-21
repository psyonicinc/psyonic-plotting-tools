@echo off
echo Running Calibration Lines Plotter
python %~dp0\..\..\plot_lines.py -b 115200 -n 4 -w 50 -t 2000 --ymin -0.02 --ymax 0.08 --scaler cal