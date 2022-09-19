#!/bin/bash

echo Running RS485 Min Max Plotter
python3.9 $(dirname $(realpath $0))/../../plot_lines.py -b 460800 --buffer 300 -n 4 -w 300 -t 6000 --ymin 0 --ymax 1800 -zp 1