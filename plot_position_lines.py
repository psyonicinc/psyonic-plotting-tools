import serial
from serial.tools import list_ports
from plot_floats_pos import plot_floats
from abh_api_core import farr_to_barr
import time
import numpy as np
import struct
import sys
import math
import keyboard

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
	
	dummymsg = [];
	dummymsg.append( (struct.pack('<B',0x50))[0] );	#device ID
	dummymsg.append( (struct.pack('<B',0xAD))[0] );	#control mode
	sum = 0
	for b in dummymsg:
		sum = sum + b
	chksum = (-sum) & 0xFF;
	dummymsg.append(chksum)

	print("********************************************")
	print("*  Press Space for Finger Wave             *")
	print("*  Hold UP or W to Open Hand              *")
	print("*  Hold DOWN or S to Close Hand           *")
	print("*  Press Escape to Stop Movement           *")
	print("********************************************")

	send_pos = [15., 15., 15., 15., 15., -15.]
	last_send_pos = send_pos.copy()
	receive_pos = [0] * 7
	last_receive_pos = receive_pos.copy()
	fingerwave = False
	up = False
	down = False
	space_once = True
	rate = 0
	while 1:
		## Check for keyboard
		if keyboard.is_pressed('space'):
			fingerwave = True
			up = False
			down = False
			rate = 0
		elif keyboard.is_pressed('esc'):
			fingerwave = False
			up = False
			down = False
			rate = 0
		elif keyboard.is_pressed('up') or keyboard.is_pressed('w'):
			fingerwave = False
			up = True
			down = False
			rate = rate + 1
		elif keyboard.is_pressed('down') or keyboard.is_pressed('s'):
			fingerwave = False
			up = False
			down = True
			rate = rate + 1
		else:
			rate = 0
			up = False
			down = False
	
		t = time.time() - tstart	
		if fingerwave:
			for i in range(0, len(send_pos)):
				ft = time.time()*3 + i
				send_pos[i] = (.5*math.sin(ft)+.5)*45+15
			send_pos[5] = -send_pos[5]
		elif up:
			for i in range(0, len(send_pos)):
				send_pos[i] = last_send_pos[i] - max((0.1 * rate / 10), 1)
				if send_pos[i] < 5:
					send_pos[i] = 5
			send_pos[5] = -send_pos[5]
		elif down:
			for i in range(0, len(send_pos)):
				send_pos[i] = last_send_pos[i] + max((0.1 * rate / 10), 1)
				if send_pos[i] > 90:
					send_pos[i] = 90
					
			if send_pos[4] > 50:
				send_pos[4] = 50
			if send_pos[5] > 50:
				send_pos[5] = 50
			send_pos[5] = -send_pos[5]
			
			
		msg = farr_to_barr(send_pos)

		#print(str(send_pos))
		ser.write(msg)
		data = ser.read(71)
		receive_pos[0] = t
		needReset = False
		if len(data) == (71):
			sum = 0
			for byte in data: 
				sum = (sum + byte)%256
			
			if sum != 0:
				needReset = 0
			else:
				for i in range(0,int(num_lines)):
					receive_pos[i+1] = abs(struct.unpack('f', data[(4*i):(4*i + 4)])[0])
					if (receive_pos[i+1] > 100):
						needReset = True
						
		else: 
			needReset = True
			
		if needReset:
			ser.reset_input_buffer()	
			reset_count+=1
			needReset = False
			receive_pos = last_receive_pos.copy()
		
		last_send_pos = send_pos.copy()
		last_send_pos[5] = -last_send_pos[5]
		last_receive_pos = receive_pos.copy()
		total_count +=1
		ser.reset_input_buffer()
		#print(str(receive_pos))
		yield receive_pos
		

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
	params = [460800, 500, 6]
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

