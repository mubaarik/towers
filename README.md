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
1. **-a** or **--args** 
  - type: string
  - description: specifies the UHD device address. 
  - expected format: -a "addr=<addres>" or --args "addr=<address>
  - example: -a "addr=192.168.10.1" 
  - defualt: 192.168.10.2
2. **-r**, **--samp-rate**
  - type:float, default=10e6,
                      help="Set sample rate (bandwidth) [default=%default]")
    parser.add_option('-z','--fft-size', type=int,default=4092, 
                        help = "Set the FFT bins(defaults to 1024)")
    parser.add_option("-f", "--freq", type="eng_float", default=None,
                      help="Set frequency to FREQ", metavar="FREQ")
    parser.add_option("", "--lo-offset", type="eng_float", default=None,
                      help="Set daughterboard LO offset to OFFSET [default=hw default]")
    parser.add_option("-g", "--gain", type="eng_float", default=None,
                      help="Set gain in dB (default is midpoint)")
    parser.add_option('--num_ffts',type=int, default=8,help="number of ffts for averaging")
    parser.add_option("--normalized-gain", action="store_true",
                      help="Specify gain as normalized value (in [0, 1])")
    parser.add_option( "-m","--metafile", action="store_true", default=False,
                      help="output metadata to file [default=%default]")
    parser.add_option( "-s","--output-shorts", action="store_true", default=False,
                      help="Output interleaved shorts instead of complex floats")
    parser.add_option("-N", "--nsamples", type="eng_float", default=None,
                      help="Number of samples to collect [default=+inf]")
    parser.add_option("-v", "--verbose", action="store_true", default=False,
                      help="verbose output")
    parser.add_option("", "--wire-format", type="string", default="sc16",
                      help="Set wire format from USRP [default=%default")
    parser.add_option("", "--stream-args", type="string", default="",
                      help="Set additional stream arguments")
    parser.add_option("", "--show-async-msg", action="store_true", default=False,
                      help="Show asynchronous message notifications from UHD [default=%default]")
    parser.add_option("", "--sync", type="choice", choices=('default', 'pps'),
                      default='default', help="Set to 'pps' to sync devices to PPS instead of internal.")

### Rerefence  

##### Collecting the FFT Samples

##### Processing the FFT samples 
