import time
import struct
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

bufwidth = 1000
num_lines = 5


fig,ax = plt.subplots()
plt.setp(ax,ylim = (-1,1))	#manually set axis y limits
plt.setp(ax,xlim = (0,50))
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

#initialization function. needed for the 'blitting' option,
#which is the lowest latency plotting option
def init(): # required for blitting to give a clean slate.
	for line in lines:
		line.set_data([],[])
	return lines



def gen_points():
	#IMPORTANT: must always first yield t/time
	global tstart
	t = time.time() - tstart
	
	list = []
	list.append(t)
	for i in range(0,num_lines):
		list.append(np.sin(t+i))
	
	yield list	#first yield time

	


def animate(args):
	for i in range(0,num_lines):
		del xbuf[i][0]
		del ybuf[i][0]
		xbuf[i].append(args[0])	#we have to make num_lines copies of xbuf to get numpy not to explode. I frankly don't understand why but it is what it is
	i = 0
	for arg in args:
		if(i > 0):
			ybuf[i-1].append(arg)
		i = i + 1
	for i, line in enumerate(lines):
		line.set_data(xbuf[i],ybuf[i])
	
	xmin = min(xbuf[0])
	xmax = max(xbuf[0])
	plt.setp(ax,xlim = (xmin,xmax))

	ax.relim()
	ax.autoscale_view(scalex=False, scaley=False)
	return lines
	
	
	
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=gen_points, interval=0, blit=True,  save_count = 50)
plt.show()