import usrp_fft_src as src
import utility_funcs as ufcns
import parameters as prms
import time
prms.makedir('fft_files/')
prms.makedir('meta_files/')
prms.makedir('collected_data/')



if __name__ == '__main__':
    (options,filename) = src.get_options()
    options.nsamples = options.fft_size*options.num_ffts
    freq_map = prms.gsm_frequencies
    c_freqs = ufcns.center_freqs(freq_map,options.samp_rate/(1e6), threshold=1.0)
    filemap = []
    for cfrq in c_freqs:
        options.freq = round(cfrq,3)
        _time = int(round(time.time()))
        filename = 'fft_files/'+str(options.freq).replace('.','_')+'.32fc'
        filemap.append({'fft_size':options.fft_size,'samp_rate':options.samp_rate,
            'c_freq':options.freq,'gain':options.gain,'filename':filename,'time': _time})
        tb = src.usrp_fft(options,filename)
        try:
            tb.run()
        except KeyboardInterrupt:
            print('Data terminated')
        if os.path.exists(filename):
            ufcns.save_file(_time,filemap)
        else:
            print "No records collected"
