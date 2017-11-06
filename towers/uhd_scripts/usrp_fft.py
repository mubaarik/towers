#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Usrp Fft
# Generated: Mon Nov  6 15:57:06 2017
##################################################
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import sys
import time




class usrp_fft(gr.top_block):

    def __init__(self, options,filename):
        gr.top_block.__init__(self, "Usrp Fft")
        
        try:
            self.channels = [int(x.strip()) for x in options.channels.split(",")]
        except ValueError:
            sys.stderr.write("[UHD_RX] [ERROR] Invalid channel list: {}".format(options.channels))
            exit(1)
        if len(self.channels)==1:
            self.filenames = [filename,]
        else:
            base,ext = os.path(splitext(filename))
            self.filenames = ["{base}.{num}{ext}".format(base=base, num=i, ext=ext) for i in range(len(channels))]



        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.cpu_format = 'fc32'
        self.item_size=gr.sizeof_float
        self.meta_file_type = blocks.GR_FILE_FLOAT



        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp= uhd.usrp_source(
        	device_addr = options.args,
        	stream_args = uhd.stream_args(
        		self.cpu_format,
        		options.wire_format,
                args = options.stream_args,
                channels = self.channels
        	)
        )
        #setting the subdevices
        if options.spec:
            for mb_idx in xrange(self.uhd_usrp.get_num_mboards()):
                self.uhd_usrp.set_subdev_spec(options.spec,mb_idx)
        #set the anthena
        if self.options.anthena is not None:
            self.anthena = [x.strip() for x in options.antenna.split(",")]
            if len(self.antenna) != 1 and len(self.antenna) != len(self.channels):
                sys.stderr.write("[UHD_RX] [ERROR] Invalid antenna setting for {} channels: {}".format(
                    len(self.channels), options.antenna
                ))
                exit(1)
            if len(self.antenna) == 1 and len(self.channels) > 1:
                self.antenna = [self.antenna[0],] * len(self.channels)
            for i, chan in enumerate(self.channels):
                self._u.set_antenna(self.antenna[i], chan)
                if options.verbose:
                    print("[UHD_RX] Channel {chan}: Using antenna {ant}.".format(
                        chan=chan, ant=self._u.get_antenna(chan)
                    ))
        #Set the reciver sample rate
        self.uhd_usrp.set_samp_rate(options.samp_rate)
        samp_rate = self.uhd_usrp.get_samp_rate()
        #Set the recieve daughterboard gain
        if options.gain is None:
            print("[UHD_RX] Defaulting to mid-point gains:")
            for chan in self.channels:
                self._u.set_normalized_gain(.5, chan)
                print("[UHD_RX] Channel {chan} gain: {g} dB".format(chan=chan, g=self._u.get_gain(chan)))
        else:
            for chan in self.channels:
                if options.normalized_gain:
                    self._u.set_normalized_gain(options.gain, chan)
                else:
                    self._u.set_gain(options.gain, chan)
        gain = self.uhd_usrp.get_gain(self.channels[0])
        #set frequency (tune request takes lo_offset):
        if options.lo_offset is not None:
            treq = uhd.tune_request(options.freq,options.lo_offset)
        else:
            treq = uhd.tune_request(options.freq)

        #Make sure tuning is synched
        command_time_set = False
        if len(channels)>1:
            if options.sync == 'pps':
                self.uhd_usrp.set_time_unknown_pps(uhd.time_spec())
            try:
                for mb_idx in xrange(self._u.get_num_mboards()):
                    self._u.set_command_time(cmd_time, mb_idx)
                command_time_set = True
            except RuntimeError:
                sys.stderr.write('[UHD_RX] [WARNING] Failed to set command times.\n')
        for chan in self.channels:
            tr = self._u.set_center_freq(treq, chan)
            if tr == None:
                sys.stderr.write('[UHD_RX] [ERROR] Failed to set center frequency on channel {chan}\n'.format(chan=chan))
                exit(1)
        if command_time_set:
            for mb_idx in xrange(self._u.get_num_mboards()):
                self._u.clear_command_time(mb_idx)
            print("[UHD_RX] Syncing channels...")
            time.sleep(COMMAND_DELAY)
        freq = self.uhd_usrp.get_center_freq(self.channels[0])


        self.fft_vxx_0 = fft.fft_vcc(options.fft_size, True, (), True, 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, options.fft_size)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*options.fft_size, "", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1024)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.uhd_usrp, 0), (self.blocks_stream_to_vector_0, 0))    

    

def get_options():
    usage="%prog: [options] output_filename"
    parser = OptionParser(option_class=eng_option, usage=usage)
    parser.add_option("-a", "--args", type="string", default="",
                      help="UHD device address args , [default=%default]")
    parser.add_option("", "--spec", type="string", default=None,
                      help="Subdevice of UHD device where appropriate")
    parser.add_option("-c", "--channels", type="string", default="0",
                      help="Select receive channels")
    parser.add_option("-A", "--antenna", type="string", default=None,
                      help="Select Rx Antenna(s) where appropriate.\nUse a comma-delimited list if different channels have different antenna ports.")
    parser.add_option("-r", "--samp-rate", type="eng_float", default=1e6,
                      help="Set sample rate (bandwidth) [default=%default]")
    parser.add_option('-z','--fft-size', type="eng_float",default=1024, 
                        help = "Set the FFT bins(defaults to 1024)")
    parser.add_option("-f", "--freq", type="eng_float", default=None,
                      help="Set frequency to FREQ", metavar="FREQ")
    parser.add_option("", "--lo-offset", type="eng_float", default=None,
                      help="Set daughterboard LO offset to OFFSET [default=hw default]")
    parser.add_option("-g", "--gain", type="eng_float", default=None,
                      help="Set gain in dB (default is midpoint)")
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
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        exit(1)
    if options.freq is None:
        parser.print_help()
        sys.stderr.write('You must specify the frequency with -f FREQ\n')
        exit(1)
    return (options, args[0])

if __name__ == '__main__':
    (options,filename) = get_options()
    tb = usrp_fft(options,filename)
    try:
        tb.run()
    except KeyboardInterrupt:
        print('Data terminated')
