# CyberSecurity Project: BYPASS CAN Protocol in a TC Charger
<p align="center">
  <img src="https://github.com/user-attachments/assets/92f92f68-73cb-4e8f-9d7c-70c58feead5b" />
</p>

In the image we can see a **Smart TC Charger**, which follows the **Standard CAN Protocol**.

In the scenario where your Battery Management System **(BMS)** is having trouble communicating with the charger, it will not start and thus not charge the battery.

The solution is to **force that communication** with an external device and this project is meant to unset the safety protocols of the charger and give the Battery a static charge of 100 Volts and 60 Amperes but it can be changed to your own preferences.

## Code explaination
<p align="center">
  <img src="https://github.com/user-attachments/assets/a6d62f13-05bd-4602-8e1e-35362f9fb004" />
</p>

These are the instructions that our TC Charger uses to get inputs from the BMS. 

We can take the **BMS ID 0x1806E5F4** and use it to fake the communication.

There is a linux package called *can-utils* that uses the **CANSEND command** to send CAN packets, On the raspberry (or whatever you're using to communicate with the TC Charger), you could write:
```
cansend can0 1806E5F4#03E8025800010000
```
We can do the same in a python environment using the **python-can** module, this will help us by simplyfing the VOLTAGE/AMPERAGE conversion process and emulate the smart charging process.

## Setting up the VCAN and the CAN pins:
Before testing our code, we have to manually connect the **CAN pins** to our raspberry; in the following photo we can see the instructions given to choose the right pins.
<p align="center">
  <img src="https://github.com/user-attachments/assets/19bd59d7-617e-4dd1-af7f-3de7137f3d1d" />
</p>

In this case **CAN High** and **CAN Low** are the ones that are gonna be connected to our raspberry to enable the communication (see the first photo of the TC Charger for reference).
On the Raspberry PI (or any other linux environment), you can setup a VCAN by typing the following commands:
```
sudo modprobe vcan
sudo ip link add dev can0 type vcan
sudo ip link set up can0
```
You should be able to see the newly created VCAN by typing "ifconfig" on the terminal, to delete it you just need to use:
```
sudo ip link set down can0
sudo ip link delete can0
```

## Examples
You can try running default values for voltage, amperage and time in order to check if everything works properly:
(100V, 60A and 5 minutes of charging)
```
python3 can-bypass.py -V 100 -A 60 -m h -t 300
```
If you want to check if the messages are being sent on the CAN bus, run the following command:
```
candump can0
```
You should be able to see the packets that the code is sending with the desired values.
