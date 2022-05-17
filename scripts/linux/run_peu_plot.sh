#!/bin/bash

echo Running PEU Lines Plotter
python3.9 $(dirname $(realpath $0))/../../plot_lines.py -b 921600 --buffer 300 -n 7 -w 300 -t 6000 --ymin -0.05 --ymax 60.5 --scaler peu