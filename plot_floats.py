import time
import struct
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt


lines = []
xbuf = []
ybuf = []
tstart = 0
num_lines = 0
bufwidth = 0

#initialization function. needed for the 'blitting' option,
#which is the lowest latency plotting option
def init(): # required for blitting to give a clean slate.
	global lines
	global ax, label
	
	for line in lines:
		line.set_data([],[])
	return lines


def animate(args):

	global ax, lines, xbuf, ybuf, num_lines, bufwidth
	global label, pf, text_height

	for i in range(0,num_lines):
		del xbuf[i][0]
		del ybuf[i][0]
		xbuf[i].append(args[0])	#we have to make num_lines copies of xbuf to get numpy not to explode. I frankly don't understand why but it is what it is
	i = 0
	for arg in args:
		if(i > 0 and i <= num_lines):
			ybuf[i-1].append(arg)
		i = i + 1
	for i, line in enumerate(lines):
		line.set_data(xbuf[i],ybuf[i])
	
	if(pf):
		if args[-1] >= 0:
			label.set_text("Pass: " + str(args[-1]))
			label.set_color("Green")
		elif args[-1] == -2:
			label.set_text("FAIL!!")
			label.set_color("Red")
		else: 
			label.set_text("")
	else:
		label.set_text("")
	
	xmin = min(xbuf[0])
	xmax = max(xbuf[0])
	plt.setp(ax,xlim = (xmin,xmax))
	label.set_position(((xmax-xmin)/2 + xmin, text_height))
	ax.relim()
	ax.autoscale_view(scalex=False, scaley=False)
	return lines

def plot_floats(n, width, xmax, ylim, data_gen, pass_fail):
	
	global fig, ax, lines, xbuf, ybuf, num_lines, bufwidth, tstart
	global label, pf, text_height
	
	pf = pass_fail

	fig,ax = plt.subplots()
	plt.setp(ax,ylim = ylim)	#manually set axis y limits
	plt.setp(ax,xlim = (0,xmax))
	plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)


	text_height = (ylim[1] - ylim[0])*0.67+ylim[0]
	label = ax.text((xmax/2),text_height, "Starting...", ha='center', va='center', fontsize=35, color="Blue")
	
	num_lines = n
	bufwidth = width
	
	lines = []
	xbuf = []
	ybuf = []

	#setup xy buffers to plot and axes
	for i in range(num_lines):
		lines.append(ax.plot([],[])[0])
		xbuf.append([])
		ybuf.append([])
	#initalize all xy buffers to 0
	for i in range(0, num_lines):	
		for j in range(0,bufwidth):
			xbuf[i].append(0)
			ybuf[i].append(0)
			
	tstart = time.time()
		
	anim = animation.FuncAnimation(fig, animate, init_func=init, frames=data_gen, interval=0, blit=False,  save_count = 50)
	plt.show()
	
	
	
