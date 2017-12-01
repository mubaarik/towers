import usrp_fft_src as src
import utility_funcs as ufcns
import parameters as prms
import time
import os
prms.makedir('fft_files/')
prms.makedir('meta_files/')
prms.makedir('collected_data/')



if __name__ == '__main__':
    ##process the command line arguments
    (options,filename) = src.get_options()
    #set the number of samples to be collected 
    options.nsamples = options.fft_size*options.num_ffts
    #Get the ARFCNs
    freq_map = prms.gsm_frequencies
    #Map the ARFCNs to center frequencies
    c_freqs = ufcns.center_freqs(freq_map,options.samp_rate/(1e6), threshold=1.0)
    #initialize a map for generating the meta file
    filemap = []
    for cfrq in c_freqs:
        #assign the center frequencies
        options.freq = round(cfrq,3)
        _time = int(round(time.time()))
        #Generate the name of the file to save the streamed data to  
        filename = 'fft_files/'+str(_time)+'_'+str(options.freq).replace('.','_')+'.32fc'
        #Update the map for this stream
        filemap.append({'fft_size':options.fft_size,'samp_rate':options.samp_rate,
            'c_freq':options.freq,'gain':options.gain,'filename':filename, 'remove': options.remove,'time': _time})
        tb = src.usrp_fft(options,filename)
        try:
            tb.run()
        except KeyboardInterrupt:
            print('Data terminated')
    _time = int(round(time.time()))
    if os.path.exists(filename):
        ufcns.save_file(_time,filemap)
    else:
        print "No records collected"
