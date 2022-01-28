import serial
from serial.tools import list_ports
from plot_floats import plot_floats
import time
import numpy as np
import struct
import sys

num_lines = 0
ser = []
reset_count = 0
tstart = 0

def setupSerial(baud):
	global ser
	global num_lines
	
	print("Searching for serial ports...")
	com_ports_list = list(list_ports.comports())
	port = ""

	for p in com_ports_list:
		if(p):
			port = p
			print("Found:", port)
			break
	if not port:
		print("No port found")
		quit()
		
	try: 
		print("Connecting...")
		ser = serial.Serial(port[0], baud, timeout = (num_lines * 0.02))
		print("Connected!")
	except: 
		print("Failed to Connect!")
		return False
		
	return True
		


def readSerial():
	global num_lines
	global tstart
	global reset_count
	
	positions = [0.0] * (1+num_lines)
	
	while 1:
	
		t = time.time() - tstart
		data = ser.read(4*num_lines)
		positions[0] = t
		needReset = False
		if len(data) == (4*num_lines):
			for i in range(0, num_lines):
				positions[i+1]=(struct.unpack('f', data[(4*i):(4*i + 4)])[0])
				if abs(positions[i+1]) > 1000 or abs(positions[i+1]) < 0.000001:
					needReset = True
		
		if needReset:
			ser.reset_input_buffer()	
			reset_count+=1
			needReset = False
			
		print(str(positions))
		yield positions
		

def plot_lines(baud, bufWidth, numLines):
	global tstart
	global num_lines
	num_lines = numLines
	tstart = time.time()
			
	if setupSerial(baud):
		plot_floats(num_lines, bufWidth, readSerial)
		ser.close()		
		print("Completed with " + str(reset_count) + " resets")


if __name__ == "__main__":
	params = [460800, 500, 4]
	if len(sys.argv) < 4:
		print("Using Default Settings!")
	else:
		for i in range(0,3):
			params[i] = int(sys.argv[i+1])
			
	print("Baud Rate: " + str(params[0]))
	print("Buffer Width: " + str(params[1]))
	print("Number of Lines: " + str(params[2]))
	
	time.sleep(2)
	
	plot_lines(params[0], params[1], params[2])  

