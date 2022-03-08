import serial
from serial.tools import list_ports
from plot_floats import plot_floats
import time
import numpy as np
import math
import struct
import sys
import argparse
import platform

num_lines = 0
ser = []
reset_count = 0
tstart = 0
scaler = "none"
parser = "float"

scalingPresets = ["none", "cal", "peu", "fsr"]
parsingPresets = ["float", "12bit"]

def setupSerial(baud_set, timeout_set):
	global ser
	global num_lines
	
	print("Searching for serial ports...")
	com_ports_list = list(list_ports.comports())
	port = ""

	for p in com_ports_list:
		if(p):
			if platform.system() != 'Linux' or "USB" in p[0]:
				port = p
				print("Found:", port)
			break
	if not port:
		print("No port found")
		quit()
		
	try: 
		print("Connecting...")
		ser = serial.Serial(port[0], baud_set, timeout = timeout_set)
		print("Connected!")
	except: 
		print("Failed to Connect!")
		return False
		
	return True
		
		
def scaleData(data):
	global scaler
	reset = False
	ret_data = data.copy()
	
	if scaler == "cal":
		for i in range(0, len(data)):
			ret_data[i] = ((data[i] + math.pi) % (2 * math.pi)) - math.pi
			if abs(ret_data[i]) > 1.0:
				reset = True
	elif scaler == "peu":
		for i in range(0, len(data)):
			if i == 1:
				ret_data[i] = 2.25*(30.0/32.0)*data[i]
			elif i == 2:
				ret_data[i] = 2.25*(30.0/30.5)*data[i]
			elif i == 3:
				ret_data[i] = 2.25*(30.0/26.0)*data[i]
			elif i == 4:
				ret_data[i] = 2.25*(30.0/28.0)*data[i]
			else:
				ret_data[i] = 2.25 * data[i]
				
			if abs(ret_data[i]) > 1000:
				reset = True
	elif scaler == "fsr":
		for num in data:
			if num < 0 or num > 4100:
				reset = True
	else:
		for num in data:
			if abs(num) > 1000 or abs(num) < 0.000001:
				reset = True
				
	return reset, ret_data
			

def readSerial():
	global num_lines
	global tstart
	global reset_count
	global parser
	global dummy_reads
	
	parsed_data = [0.0] * (num_lines)
	final_data = [0.0] * (1+num_lines)
	
	# Default for floats
	bufferLength = int(4 * num_lines)
	if parser == "12bit":
		bufferLength = int(math.ceil((1.5 * num_lines)) + 1)
	
	print("Read Length: " + str(bufferLength))
	
	while 1:
	
		t = time.time() - tstart
		for i in range(0,dummy_reads + 1):
			data = ser.read(bufferLength)
		final_data[0] = t
		needReset = False
		if len(data) == (bufferLength):
			if parser == float:
				for i in range(0, num_lines):
					parsed_data[i]=struct.unpack('f', data[(4*i):(4*i + 4)])[0]
			elif parser == "12bit":
				for i in range(0, int(math.ceil(num_lines/2))):
					dualData = data[i * 3:(i + 1) * 3]
					data1 = struct.unpack('H', dualData[0:2])[0] & 0x0FFF
					data2 = (struct.unpack('H', dualData[1:3])[0] & 0xFFF0) >> 4
					parsed_data[2*i] =  int(data1)
					parsed_data[(2*i)+1] = int(data2)
			
			needReset, ret_data = scaleData(parsed_data)
		else:
			print("Data len: " + str(len(data)))
			needReset = True
			ret_data = parsed_data.copy()
	
		
		for i in range(0, num_lines):
			final_data[i+1] = ret_data[i]
		
		if needReset:
			ser.reset_input_buffer()
			reset_count+=1
			needReset = False
			
		print(str(final_data))
		yield final_data
		

def plot_lines(baud, timeout, bufWidth, numLines, xmax, ylims, scaling, parsing, discard):
	global tstart
	global num_lines
	global scaler
	global parser
	global dummy_reads
	num_lines = numLines
	tstart = time.time()
	scaler = scaling
	parser = parsing
	dummy_reads = discard
			
	if setupSerial(baud, timeout):
		ser.reset_input_buffer()
		plot_floats(num_lines, bufWidth, xmax, ylims, readSerial)
		ser.close()		
		print("Completed with " + str(reset_count) + " resets")


if __name__ == "__main__":

	# Define All Args
	parser = argparse.ArgumentParser(description='Psyonic Serial Line Plotter')
	parser.add_argument('-b', '--baud', type=int, help="Serial Baud Rate", default=460800)
	parser.add_argument('--buffer', type=int, help="Data Buffer Size", default=500)
	parser.add_argument('-n', '--number', type=int, help="Number of Lines", default=3)
	parser.add_argument('-w', '--width', type=float, help="X Width of Plot (s)", default = 50)
	parser.add_argument('-t', '--timeout', type=int, help="Serial Timeout (ms)", default = 0)
	parser.add_argument('--ymin', type=float, help="Y Scale Minimum", default = -1.0)
	parser.add_argument('--ymax', type=float, help="Y Scale Maximum", default = 1.0)
	parser.add_argument('--scaler', help="Prescaling to do on data", choices=scalingPresets, default="none")
	parser.add_argument('--parser' , help="How to parse raw serial data", choices=parsingPresets, default="float")
	parser.add_argument('--discard', type=int, help="Number of Dummy Reads to do to discard data", default=0)
	args = parser.parse_args()
	
	## Check Validity
	#With must be at least 1
	if args.baud < 100:
		sys.exit("Invalid Baud")
	if args.number < 1:
		sys.exit("Must be at least one line")
	if args.width < 1:
		sys.exit("Width must be at least 1 second")
	if args.ymin >= args.ymax:
		sys.exit("Ymin must be less than Ymax")
			
	
	timeout = args.timeout / 1000.0
	if args.timeout < 1:
		timeout = args.number * 0.02
	
	ytuple = tuple((args.ymin, args.ymax))
	print("Baud Rate: " + str(args.baud))
	print("Buffer Width: " + str(args.buffer))
	print("Number of Lines: " + str(args.number))
	print("Number of Seconds to show: " + str(args.width))
	print("Y values in range: " + str(ytuple))
	print("Using Scaler: " + str(args.scaler))
	print("Using Parser: " + str(args.parser))
	print("Serial Timeout: " + str(timeout))
	
	print("Starting", end="")
	for i in range(0,4):
		print(".", end="", flush=True)
		time.sleep(0.5)
	print(".")
	
	
	plot_lines(args.baud, timeout, args.buffer, args.number, args.width, ytuple, args.scaler, args.parser, args.discard)  
