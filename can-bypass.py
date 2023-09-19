"""
Author: Flavio Gjoni - Electric QDL
Description: BMS-CAN emulator to deploy 100V/60A of charge
Version: 1.0x
"""
import time
import can

# ID gathered from DOCs
charger_id = 0x18FF50E5
bms_id = 0x1806E5F4
# CAN bus interface
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=250000)
# define data, to choose in sendMessage param? (so we can switch signals)
message_data_heat = bytearray([0x03, 0xE8, 0x02, 0x58, 0x00, 0x01, 0x00, 0x00])
message_data_charge = bytearray([0x03, 0xE8, 0x02, 0x58, 0x00, 0x00, 0x00, 0x00])
temp_heat = bytearray([0x03,0xE8,0x02,0x58,0x00,0x01,0x00,0x00])
message = can.Message(arbitration_id=bms_id, data=message_data_charge, is_extended_id=True)

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
	enableHeat()
	time.sleep(3)
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
	print("\n")
	sendMessage()
	bus.shutdown()
	print("\nExiting code...")
