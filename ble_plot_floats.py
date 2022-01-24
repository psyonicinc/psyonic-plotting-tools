import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import struct
import sys
import threading
from plot_floats import plot_floats

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

m_name = "PSYONIC-GANGGANG"
num_lines = 4
buf_width = 400

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
		farr = []
		for i in range(0, len(data) // 4):
			farr.append(struct.unpack('f', data[(4*i) : (4*i + 4)]))
		print("received", farr)
		
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
	
	
if __name__ == "__main__":

	t1 = threading.Thread(target=ble_thread, args=())
	#t2 = threading.Thread(target=plot_floats, args=(num_lines, buf_width, 
	t1.start()
	t1.join()

