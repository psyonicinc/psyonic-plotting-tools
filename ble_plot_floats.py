import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import struct
import sys
import threading
from plot_floats import plot_floats
import time

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

m_name = "PSYONIC-21ABH035"
num_lines = 6
buf_width = 400
gl_ble_data = []
for i in range(0,num_lines):
	gl_ble_data.append(0)
tstart = time.time()

queue = asyncio.Queue()

def detection_callback(device, advertisement_data):
	name = advertisement_data.local_name
	uuid = advertisement_data.service_uuids
	if name:
		queue.put_nowait([name,device.address, uuid])


async def get_address(advert_name):
	scanner = BleakScanner()
	scanner.register_detection_callback(detection_callback)
	await scanner.start()
	await asyncio.sleep(5.0)
	await scanner.stop()
	
	print("Devices Found:")
	address_to_connect = 0
	for i in range(0, queue.qsize()):
		q = await queue.get()
		print(q)
		if(q[0] == advert_name):
			address_to_connect = q[1]
	print("Found address: ", address_to_connect)
	return address_to_connect


async def main():

	def handle_disconnect(_: BleakClient):
		print("Disconnected.")
		for task in asyncio.all_tasks():
			task.cancel()

	def handle_rx(_: int, data: bytearray):
		#print("received:", data)
		global gl_ble_data
		
		datalen = len(data)		
		farr = []
		for i in range(0, datalen // 4):
			farr.append(struct.unpack('f', data[(4*i) : (4*i + 4)])[0])
		#print(farr)
		gl_ble_data = farr
		
	address = await get_address(m_name)
	if(address):	
		client = BleakClient(address, disconnected_callback=handle_disconnect)
				
		try:
			await client.connect()
			print("connected.")
			await client.start_notify(UART_TX_CHAR_UUID, handle_rx)			
			while True:
				await asyncio.sleep(1.0)
		except Exception as e:
			print(e)
		finally:
			await client.disconnect()
	else:
		print("Requested device", m_name ,"not found. leaving")

def ble_thread():
	asyncio.run(main())
	
def expose_points():
	global gl_ble_data
	global tstart
	
	list = []
	t = time.time() - tstart
	list.append(t)
	for d in gl_ble_data:
		list.append(d)
	
	#catch empty list. kludge
	if(len(list) != (num_lines + 1)):
		list = []
		list.append(t)
		for i in range(0,num_lines):
			list.append(0)
	
	yield list

def plot_thread():
	global gl_ble_data
	plot_floats(num_lines, buf_width, expose_points)
	#while True:
	#	print(gl_ble_data)
	
if __name__ == "__main__":

	t1 = threading.Thread(target=ble_thread, args=())
	t2 = threading.Thread(target=plot_thread, args=())
	t2.start()
	t1.start()
	
	#t1.join()
	#t2.join()
	

