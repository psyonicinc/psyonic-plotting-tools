@echo off
echo Running PEU Lines Plotter
python %~dp0\..\plot_lines.py -b 921600 --buffer 300 -n 7 -w 300 -t 6000 --ymin -0.05 --ymax 100.5 --scaler peu