"""
Author: Flavio Gjoni - Electric QDL
Description: BMS-CAN emulator to deploy, by default, 100V/60A of charge (or custom values)
Version: 1.1x
"""
import time
import can
import argparse

# Setting the bmsID, CAN channel and bustype (bitrate is default 250k)
bms_id = 0x1806E5F4
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=250000)
data_message = bytearray([0x03, 0xE8, 0x02, 0x58, 0x00, 0x01, 0x00, 0x00]) #0x01 for HEATING MODE
can_message = can.Message(arbitration_id=bms_id, data=data_message, is_extended_id=True)

#heat enable first, then disable:
def startCharging(voltage=1000, amperage=600, mode='h', time=300):
	if(mode == 'c'):
		data_message[5] = 0x00
	# Start the charging mode
	try:
		for i in range(time):
			print(f"Sending CAN message {i+1}: {can_message}")
			bus.send(can_message)
			time.sleep(1)
	# In case the code was interrupted by keyboard (eg. CTRL+C):
	except KeyboardInterrupt:
		print("Terminated by keyboard")
		bus.shutdown()
	print(f"\nExiting {'charging' if mode == 'c' else 'heating'} mode")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Python code to bypass CAN protocol requirements for smart chargers, thought for TC Chargers.")
	parser.add_argument("-V", "--voltage", required=True, help="Select the voltage required (it will be divided by 10), eg. '-V 1000' will equal 100.0V. (DEFAULT: 1000)")
	parser.add_argument("-A", "--amperage", required=True, help="Select the amperage required (it will be divided by 10), eg. '-A 600' will equal 60.0A. (DEFAULT: 600)")
	parser.add_argument("-m", "--mode", required=True, help="Use '-m h' for heating mode or '-m c' for charging mode. (DEFAULT: Heating mode)")
	parser.add_argument("-t", "--time", required=True, help="Choose for how much time (in seconds) to keep the charger active. (DEFAULT: 300s=5m)")
	args = parser.parse_args()
	startCharging(args.voltage, args.amperage, args.mode, args.time)
	bus.shutdown()
	print("\nBus in shutdown, closing the program...")
