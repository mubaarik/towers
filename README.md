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
To run the scripts please use the following command. The command expects properly installed scripts.

`usrp_rx_command <optional arguments>`

##### OPtional Arguments 

The following are the list arguments you can specify for resired configuration with a fairly detailed discription of their intended influence.
1. **-a**, **--args** 
  - type: string
  - description: specifies the UHD device address. 
  - expected format: -a "addr=<addres>" or --args "addr=<address>
  - example: -a "addr=192.168.10.1" 
  - defualt: 192.168.10.2
2. **-r**, **--samp-rate**
  - type:float 
  - Description: The device sample rate (bandwidth) in samples/second
  - expected format: -r <x> --samp-rate=<x> or --samp-rate <x>. 
  -examples: The following are equivalent: -a 20000000, -a 20M, -a 20e10, --samp-rate=20M, --samp-rate 20M
  - default: 10e6
3. **-z**,**--fft-size**
  - type:int 
  - Description: The number of FFT bins or fft resolution, expected to be power of 2.
  - expected format: -z <x> --fft-size=<x> or --fftt-size <x>. 
  - examples: --fft-size <x>, --fft-size=<x>, -z <x> . <x> should be power of 2 for better performance. 
  - default: 4096
4. **-f**, **--freq**, 
  - type: float
  - Description: Center freq of the samples. 
  - expected format: -f <hz>, --freq=<hz>
  - examples: -f 850M
  - default: 850M
  
5.**-g**, **--gain**
  - type: float
  - Description: Gain of the device in dB(default is midpoint)
  - expected format: -g <float>, --gain=<float>, or --gain <float>
  - examples: -g 25
  - default: 20
6. **--num_ffts**
  - type: int 
  - Description: Number of ffts to collect at current center frequency.
  - expected format: --num_ffts=<int> or --num_ffts <int>
  - examples: --num_ffts=8
  - default: 8
The above parameters are the most the important and relevant arguments but there are many more commands you could specify. To see more detailed list of the optional arguments run `usrp_rx_commannds --help`. 

This program uses the **argparser** module, for better understanding of the command line argument specifications please [see](https://docs.python.org/2/library/argparse.html). Thank you.
### Rerefence  
The above command runs **--towers/towers/uhd_scripts/usrp_commands.sh--**, which runs **--towers/towers/uhd_scripts/usrp_fft.py--** and --**_towers/towers/uhd_scripts/file_processing.py_** as two separate processes. The following two sections.

##### Collecting the FFT Samples

##### Processing the FFT samples 
