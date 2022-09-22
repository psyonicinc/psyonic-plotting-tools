#!/bin/bash

echo Running Calibration Lines Plotter
python3.9 $(dirname $(realpath $0))/../../plot_lines.py -b 230400 -n 4 -w 50 -t 2000 --ymin -0.01 --ymax 0.01 --scaler cal --passfail
