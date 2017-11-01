import argparse
import parameters as prms
from utility_funcs import *
import time
import os

def uhdRxCommands():
	parser = argparse.ArgumentParser(description='uhd_rx_cfile command without the center frequeny');
	parser.add_argument('device_ip', action='store', help='device ip address')
	parser.add_argument('--gain', action='store', help='gain', type=int)
	#parser.add_argument('--samp-rate', action='store', help='set the sample rate or bandwith', type=int)
	#parser.add_argument('filename',acion='store', help='name of the file without the extention')
	args = parser.parse_args()
	return args

if __name__ =="__main__":
	args = uhdRxCommands()
	#
	csv_file = 'csv_files/bands.csv'
	band_segments = band_segmentation()
	
	band_freq_map = {}

	for segment in band_segments:
		addr = ' -a '+ '"'+'addr='+str(args.device_ip)+'"'
		gain = ' -g '+ str(args.gain)
		freq =  ' -f '+str(round(segment.c_freq,3))+'e6'
		samp_rate = ' --samp-rate '+str(round(segment.samp_rate,3))+'e6 '
		num_samples = ' -N '+str(round(segment.samp_rate,3))+'e6 '
		stamp = int(round(time.time()))
		filename = str(stamp)+'_'+segment.band.replace(' ','_')+'_'+str(int(round(segment.c_freq,3)*1000000))+'.32fc'
		segment.filename = filename
		command = 'uhd_rx_cfile'+addr+gain+freq+samp_rate+num_samples+filename
		print command
		os.system(command)
		process_files(segment,band_freq_map)
	band_channels(band_freq_map)



