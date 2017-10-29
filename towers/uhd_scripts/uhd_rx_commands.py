import argparse
import parameters as prms
import utility_funcs
import time
from uhd_processor import SampleFileAnalysis as sfa 

import os
frequencies = prms.gsm_frequencies
band_segments = utility_funcs.band_segmentation()
#Extract mapped dp_freq
#extract the specified frequencies 
#save the maps to a csv file
def process_files():
	for segment in band_segments:
		analizer = sfa(segment.filename, center_freq=segment.c_freq*1e6, sample_rate=segment.samp_rate*1e6)
		freq_dB = analizer.freq_pow_pairs_map()
		f_freq_dB = freq_dB[freq_dB['Freq'].isin(segment.channels*1e6)]
		csv_file = segment.filename.split('.')[0].strip()+'.csv'
		f_freq_dB.to_csv(csv_file)
		os.remove(segment.filename)
		segment.filename = None


	return None
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
	band_samp_rate_freq = utility_funcs.band_sampRate_freq(csv_file)
	
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
	#process_files()



