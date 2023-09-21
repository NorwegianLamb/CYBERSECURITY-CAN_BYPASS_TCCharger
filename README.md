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

## Examples
//
