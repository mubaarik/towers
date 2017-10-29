import agrparse
import parameters as prms
import utility
import os
frequencies = prms.gsm_frequencies

def uhdRxCommands():
	parser = agrparse.ArgumentParser(description='uhd_rx_cfile command without the center frequeny');
	parser.add_argument('device_ip', action='store', help='device ip address')
	parser.add_argument('--gain', action='store', help='gain', type=int)
	#parser.add_argument('--samp-rate', action='store', help='set the sample rate or bandwith', type=int)
	#parser.add_argument('filename',acion='store', help='name of the file without the extention')
	args = parser.parse_args()
	return args
x=12
if __name__ == "__main__":
	args = uhdRxCommands()
	#
	csv_file = pd.read_csv('csv_files/bands.csv')
	band_samp_rate_freq = utility.band_sampRate_freq(csv_file)
	files_to_process=[]
	for triple in band_sampRate_freq:
		addr = ' -a '+ '"'+'addr='+str(args.device_ip)+'"'
		gain = ' -g '+ str(args.gain)+
		freq =  ' -f '+str(round(triple[-1],3))+'e6'
		samp_rate = ' --samp-rate '+str(round(triple[1],3))+'e6 '
		num_samples = ' -N '+str(round(triple[1],3))+'e6 '
		stamp = int(round(time.time()))
		filename = triple.replace(' ','_')+'_'+str(round(triple[-1],3)*1000000)+'_'+str(stamp)+'.32fc'
		command = 'uhd_rx_cfile'+addr+gain+freq+samp_rate+num_samples+filename
		print command
		#os.system(command)



