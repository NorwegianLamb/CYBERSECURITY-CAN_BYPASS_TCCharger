# CyberSecurity Project: BYPASS CAN Protocol in a TC Charger
You can use this code to bypass the CAN protocol of a TC charger, it will erogate as much VOLTAGE/AMPERAGE as required (within, of course, the limit of the charger)
This can be useful in case you need to use it as a normal charger, without having the need of setting up the CAN communication between the components.

- [] add table content

## Code explaination
This code does what the **CANSEND** command do (from the *can-utils* linux package), but in a python environment.
On the raspberry (or whatever you're using to communicate with the TC Charger), you could write:
```
cansend can0 1806E5F4#03E8025800010000
```
And this is what I used to do in order to test the charger, but decided to opt for the **python-can** module on python to automate charging mode, time and simplyfing the VOLTAGE/AMPERAGE conversion process.

## Setting up the VCAN:
You can setup a VCAN on a linux machine (in case you want to test the code) by typing the following commands:
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