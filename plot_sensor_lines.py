import serial
from serial.tools import list_ports
from plot_floats import plot_floats
from abh_api_core import farr_to_barr
import time
import numpy as np
import struct
import sys

num_lines = 0
ser = []
reset_count = 0
total_count = 0
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
		ser = serial.Serial(port[0], baud, timeout = 0.02)
		print("Connected!")
	except: 
		print("Failed to Connect!")
		return False
		
	return True
		


def readSerial():
	global num_lines
	global tstart
	global reset_count
	global total_count
	
	pressures = [0.0] * (1+num_lines)
	prev_pressure = pressures.copy()
	pos = [15., 15., 15., 15., 15., -15.]
	while 1:
		t = time.time() - tstart
		msg = farr_to_barr(pos)
		ser.write(msg)
		data = ser.read(71)
		pressures[0] = t
		needReset = False
		if len(data) == (71):
			sum = 0
			for byte in data: 
				sum = (sum + byte)%256
			
			if sum != 0:
				needReset = 0
			else:
				for i in range(0, int(num_lines/2)):
					dualData = data[24+(i*3):24+((i*3)+3)]
					data1 = struct.unpack('H', dualData[0:2])[0] & 0x0FFF
					data2 = (struct.unpack('H', dualData[1:3])[0] & 0xFFF0) >> 4
					pressures[(2*i)+1] = int(data1)
					pressures[(2*i)+2] = int(data2)
					if (data1 > 4000) or (data2 > 4000):
						needReset = True
		else: 
			needReset = True
			
		if needReset:
			ser.reset_input_buffer()	
			reset_count+=1
			needReset = False
			pressures = prev_pressure.copy()
		
		prev_pressure = pressures.copy()
		total_count +=1
		print(str(pressures))
		yield pressures
		

def plot_lines(baud, bufWidth, numLines):
	global tstart
	global num_lines
	global total_count
	num_lines = numLines
	tstart = time.time()
			
	if setupSerial(baud):
		plot_floats(num_lines, bufWidth, readSerial)
		ser.close()		
		print("Completed with " + str(reset_count) + " resets")
		print("Total Runs: " + str(total_count))
		print("Elapsed Time(s): " + str(time.time() - tstart))

if __name__ == "__main__":
	params = [460800, 500, 30]
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

