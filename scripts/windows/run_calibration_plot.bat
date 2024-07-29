@echo off
echo Running Calibration Lines Plotter
SET fpath=%~dp0
python  "%fpath:~0,-1%"\..\..\plot_lines.py -b 230400 -n 4 -w 50 -t 2000 --ymin -163.84 --ymax 163.84 --scaler cal --passfail
