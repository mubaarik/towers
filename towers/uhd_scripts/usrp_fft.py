import usrp_fft_src as src
import utility_funcs as ufcns
import parameters as prms
import time
prms.makedir('fft_files/')



if __name__ == '__main__':
    (options,filename) = src.get_options()
    options.nsamples = options.fft_size*options.num_ffts
    freq_map = prms.gsm_frequencies
    c_freqs = ufcns.center_freqs(freq_map,options.samp_rate, threshold=1.0)
    for cfrq in c_freqs:
        options.freq = round(cfrq,3)
        filename = 'fft_files/'+str(int(time.time()))+'_'+str(options.freq).replace('.','_')+'.32fc'

        tb = src.usrp_fft(options,filename)
        try:
            tb.run()
        except KeyboardInterrupt:
            print('Data terminated')
