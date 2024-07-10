#!/bin/bash

echo Running Calibration Lines Plotter
python3 $(dirname $(realpath $0))/../../plot_lines.py -b 230400 -n 4 -w 50 -t 2000 --ymin -40.96 --ymax 40.96 --scaler cal --passfail
