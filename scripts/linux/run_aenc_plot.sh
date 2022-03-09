#!/bin/bash

echo Running AENC Plotter
python3.9 $(dirname $(realpath $0))/../../plot_lines.py -b 230400 --buffer 300 -n 1 -c -w 300 -t 5000 --ymin -3.25 --ymax 3.25 --scaler aenc --discard 20