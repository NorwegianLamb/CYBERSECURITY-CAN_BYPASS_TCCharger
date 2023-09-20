"""
Author: Flavio Gjoni - Electric QDL
Description: BMS-CAN emulator to deploy 100V/60A of charge
Version: 1.1x
"""
import time
import can
import argparse

# Setting the bmsID, CAN channel and bustype (bitrate is default 250k)
bms_id = 0x1806E5F4
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=250000)
message_data = bytearray([0x03, 0xE8, 0x02, 0x58, 0x00, 0x01, 0x00, 0x00]) #0x01 for HEATING MODE

#heat enable first, then disable:
def enableHeat():
	h = 0
	heat_message = can.Message(arbitration_id=bms_id, data=temp_heat, is_extended_id=True)
	try:
		while (h < 600):
			print(f"Sending CAN message {h+1}: {heat_message}")
			bus.send(heat_message)
			time.sleep(1)
			h = h + 1
	except KeyboardInterrupt:
		print("Terminated by keyboard")
	print("\nExiting heating mode")

# add params to define message types? (if automated charger)
def sendMessage():

	i = 0
	try:
		while (i < 15):
			print(f"Sending CAN message {i+1}: {message}")
			bus.send(message)
			time.sleep(1)
			i = i+1
	except KeyboardInterrupt:
		print("Terminated by keyboard")
		bus.shutdown()
	print("\nexiting sendMessage()")

# entry point from running command?
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Automated scraper for the SISTER framework, it gathers the PDF files for property successions and parses them")
	parser.add_argument("-V", "--voltage", required=True, help="Select the voltage required, eg. '-V 100.0'. (DEFAULT: 100.0V)")
	parser.add_argument("-A", "--amperage", required=True, help="Select the amperage required, eg. '-A 60.0'. (DEFAULT: 60.0A)")
	parser.add_argument("-m", "--mode", required=True, help="Use '-m h' for heating mode or '-m c' for charging mode. (DEFAULT: Heating mode)")
	parser.add_argument("-t", "--time", required=True, help="Choose for how much time (in seconds) to keep the charger active. (DEFAULT: 300s=5m)")
	args = parser.parse_args()
	sendMessage(args.voltage, args.amperage, args.mode, args.time)
	bus.shutdown()
	print("\nBus in shutdown, closing the program...")
