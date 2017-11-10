from optparse import OptionParser
import sys
def get_options():
  usage="%prog: [options] output_filename"
  parser = OptionParser(usage=usage)
  parser.add_option("-a", "--args", type="string", default="",
                help="UHD device address args , [default=%default]")
  parser.add_option("", "--spec", type="string", default=None,
                help="Subdevice of UHD device where appropriate")
  parser.add_option("-c", "--channels", type="string", default="0",
                help="Select receive channels")
  parser.add_option("-A", "--antenna", type="string", default=None,
                help="Select Rx Antenna(s) where appropriate.\nUse a comma-delimited list if different channels have different antenna ports.")
  parser.add_option("-r", "--samp-rate", type=float, default=10e6,
                help="Set sample rate (bandwidth) [default=%default]")
  parser.add_option('-z','--fft-size', type=int,default=1024, 
                  help = "Set the FFT bins(defaults to 1024)")
  parser.add_option("-f", "--freq", type=float, default=8000000,
                help="Set frequency to FREQ", metavar="FREQ")
  parser.add_option('--num_ftts',type=int, default=8,help="number of ffts for averaging")
  parser.add_option('--collect', action='store_true',default=False,
                  help="if true saves the writes data to given filename with given center frequency")
  parser.add_option("", "--lo-offset", type=float, default=None,
                help="Set daughterboard LO offset to OFFSET [default=hw default]")
  parser.add_option("-g", "--gain", type=float, default=None,
                help="Set gain in dB (default is midpoint)")
  parser.add_option("--normalized-gain", action="store_true",
                help="Specify gain as normalized value (in [0, 1])")
  parser.add_option( "-m","--metafile", action="store_true", default=False,
                help="output metadata to file [default=%default]")
  parser.add_option( "-s","--output-shorts", action="store_true", default=False,
                help="Output interleaved shorts instead of complex floats")
  parser.add_option("-N", "--nsamples", type=float, default=None,
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
if __name__ =="__main__":
  (options, filename) = get_options()
  #options.samp_rate=2000000
  print options.samp_rate
  print options