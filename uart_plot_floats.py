from plot_floats import plot_floats
import time
import numpy as np

num_lines = 3

tstart = time.time()

#get the data and expose it to plotting
def gen_points():
	#IMPORTANT: must always first yield t/time
	global tstart
	global num_lines
	
	while 1:
		t = time.time() - tstart
	
		list = []
		list.append(t)
		for i in range(0,num_lines):
			list.append(10*np.sin(t+i))		#pipe new data in here
		
		yield list	#first yield time


plot_floats(num_lines, 400, gen_points)	# note: gen_points must yield the same number of points as is passed in the num_lines argument