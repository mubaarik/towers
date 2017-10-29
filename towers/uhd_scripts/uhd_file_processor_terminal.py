import argparse as argp
from uhd_processor import SampleFileAnalysis as sfa 


if __name__ == "__main__":
	prsr=argp.ArgumentParser(description = 'Running the program to manupilate streamed file data')
	prsr.add_argument('filename', action = 'store', 
		help = 'name of file generated with uhd_rx_cfile for processing. You have to specify this.')

	prsr.add_argument('--decimator', action= 'store', default=1,type=int, 
		help='downsampling factor. See scipy.signal.decimate')
	prsr.add_argument('--center_freq', action='store', default=850e6, type = int, 
		help = 'The center frequency of the streamed samples. It is should be same as'+ 
		'the -f argument provided to the uhd_rx_cfile command.'+
		'Note: this argument defaults to 850e6')
	prsr.add_argument('--sample_rate', action='store', default=5e5, type=int,
		help='The sample rate of the streamed data, should be same as the --samp_rate argument'+
		'passed to the uhd_rx_cfile command.'+' Warning: You have to specify this argument unless your sample_is exactly 5e5')
	prsr.add_argument('--fft', action='store_false', default=True,
		help='If provided the plots and graphs are on the data before fast fourier transform is applied')
	prsr.add_argument('--func_call', action='store', choices=('plot','write_to_csv_file','segment','time_segments'), default='plot',
		help = 'Specifies a function to call. \n'+'Choices:\n'+'plot: generates the plots for each time segment of the streamed data(default function call)'+
		'\n write_to_csv_file: writes the data freq, power(dB) pairs to a csv file. You can specify the file to write with the --outputfile option'+
		' Otherwise to <inputfile name>_freq_pow_pairs.csv\n'+
		'segment: Outputs the Q/I data. If --low_cutOff, --high_cutOff or both are specified, it outputs the data with low_cutOff'+
		' removed at the beginning'+ 'high_cutOff removed at the end.'+'\n'+
		'time_segments: returns when second segment of the data specified by --segment_index. --segment_index is greater than the length'+
		' the last segment is returned')
	prsr.add_argument('--outputfile', action='store', default='segment',
		help ='File to write if --func_call=write_to_csv_file')
	prsr.add_argument('--high_cutOff', action='store', default=0,type=int, 
		help='how many data points to remove at the beginning when --func_call==segment')
	prsr.add_argument('--low_cutOff', action='store', default=0,type=int, 
		help='how many data points to remove at the end when --func_call==segment')
	prsr.add_argument('--segment_index', action='store', type=int,
		help='Integer to specify the index of the time segment to output or when --func_call=time_segments or plot. If not provided all of them are outputed')
	prsr.add_argument('--plotname', action='store', default='data segment',help='name of the plot to be saved')

	args = prsr.parse_args()
	save_plot = False
	if args.outputfile!=None:
		save_plot = True
	smple_file_obj = sfa(str(args.filename), center_freq=args.center_freq, sample_rate=args.sample_rate,decimation=args.decimator)

	segments = smple_file_obj.segments_to_db(fft=args.fft)
	print "args.fft: ",args.fft
	n = len(segments)
	segment_index = args.segment_index
	if args.segment_index>=n:
		segment_index=-1

	if args.func_call=='write_to_csv_file':
		smple_file_obj.freq_pow_pair_to_csv(self,filename=args.outputfile, fft=args.fft)
	elif args.func_call=='segment':
		if args.fft:
			smple_file_obj.fftSegment(strt_cut = args.low_cutOff, end_cut = args.high_cutOff)
		else:
			smple_file_obj.raw_dataSegment(strt_cut = args.low_cutOff, end_cut = args.high_cutOff)
	elif args.func_call=='time_segments':
		if args.fft:
			smple_file_obj.time_segments_fft()
		else:
			smple_file_obj.time_segments()
	else:
		smple_file_obj.plot(smple_file_obj.segments_to_db(fft=args.fft)[0], fft=args.fft,term=True,title=args.plotname, save_plot=save_plot,save_to_as=args.outputfile)
		



