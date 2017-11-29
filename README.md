## About this repository
Contains repository contains the python scripts and other files for collecting spectrum data with the USRP N200 device. For instructions concerning running the scripts please keep reading.

## Running the command 

### Check USRP connection 
Before you run the scripts, please make sure that the device is connected via ethernet or USB3 port. You will need to specify the device ip address to run the scripts. 

To assign an ip address to the device please run the following command.

`sudo ifconfig <interface> <ip address> netmask <net mask>`
for example
`sudo ifconfig eth0 192.168.10.1 netmask 255.255.255.0` (recommended method)
### Run the data collection scripts 

## Modules 

#### Collecting the FFT Samples

#### Processing the FFT samples 
