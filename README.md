### About this repository
Contains repository contains the python scripts and other files for collecting spectrum data with the USRP N200 device. For instructions concerning running the scripts please keep reading.

### Running the command 

#### Check USRP connection 
Before you run the scripts, please make sure that the device is connected via ethernet or USB3 port. You will need to specify the device ip address to run the scripts. 

To assign an ip address to the device please run the following command.

`sudo ifconfig <interface> <ip address> netmask <net mask>`

Following is an example using the recommended configurations.

`sudo ifconfig eth0 192.168.10.1 netmask 255.255.255.0` (recommended method)

for more informations regarding the USRP networking configuration, please visit the USRP [hardware manual](https://files.ettus.com/manual/page_usrp2.html).
#### Run the data collection scripts 
To run the scripts please use the following command. The command expects that the scripts are properly installed.

`usrp_rx_command <optional arguments>`

#####OPtional Arguments 

The following are the list arguments you can specify for resired configuration.


### Rerefence  

##### Collecting the FFT Samples

##### Processing the FFT samples 
