import time
import pandas as pd
import numpy as np
import scipy
import scipy.signal
import matplotlib.pyplot as plt
class SampleFileAnalysis:
    def __init__(self, filename, center_freq=850e6, sample_rate=5e5,decimation = 1, file_datatype = np.complex64):
        self.filename = filename;
        self.freq = center_freq;
        self.samp_rate = sample_rate
        self.cmplx_data = scipy.fromfile(open(filename), dtype = file_datatype)
        self.decimation=decimation
        if self.decimation>1:
            self.cmplx_data = scipy.signal.resample(scipy.fromfile(open(filename), dtype = file_datatype), self.samp_rate/self.decimation)
            self.samp_rate = sample_rate/self.decimation
        self.n = len(self.cmplx_data)
        print 'self.n: ',self.n
        self.samp_spacing = 1.0/self.samp_rate
    #Return the complex data from the provided file
    def raw_dataSegment(self, strt_cut = 0, end_cut = 0):
        return self.cmplx_data[strt_cut:self.n-end_cut];
    #Return the fft of a segment of the data
    def fftSegment(self, strt_cut = 0, end_cut = 0):
        cmplx_samples = self.cmplx_data[strt_cut:self.n-end_cut];
        return np.fft.ftt(cmplx_samples)
    
    #time series of the window sampling scans
    def time_segments(self):
        remains = self.n%self.samp_rate
        num_segments = self.n/self.samp_rate
        return self.cmplx_data[remains:].reshape(num_segments,self.samp_rate)
    #FFTs of the time series of the window sampling scans
    def time_segments_fft(self):
        segments = self.time_segments()
        return np.apply_along_axis(np.fft.fft, 1, segments)
    #Complex number to dB
    def complex_to_db(self,cmplx):
        return 20*np.log(np.absolute(cmplx))
    #Map Q,I to dB
    def segments_to_db(self, fft=False):
        segments = self.time_segments()
        if fft:
            segments = self.time_segments_fft()
        return np.apply_along_axis(self.complex_to_db, 0,segments)
    #Plots a segment of data using the specified file sample rate and center freq
    #Inputs:
        #segment-> 1d numpy array to be plotted
        #fft -> if True: calculates the corresponding frequencies using the sample rate and center frequency
                #otherwise uses the length of the segment to time index the data
        #indices: if not None use them as the x-coordinates 
        #title: The title of the figugre to be plotted
        #save_plot: if True saves the plot to save_to_as
        #save_to_as: expected: path/filename. defualts to current directory
    #output:
        #plots the segment provided
        #saves the plots to the specified file 
    def plot(self, segment, fft = True, indices = None, title = 'data segment', save_plot = False, save_to_as = 'segment',term=False):
        samp_spacing = 1.0/self.samp_rate
        n = len(segment)
        h_data = indices
        if indices==None:
            if fft:
                h_data = np.add(np.fft.fftfreq(len(segment), d = samp_spacing), self.freq)
            else:
                h_data = np.arange(n)
        fig, ax = plt.subplots(figsize = (12,8))
        ax.plot(h_data, segment)
        ax.set_title(title)
        if save_to_as=='segment':
            save_to_as = save_to_as+'_'+str(int(time.time()))+'.jpg'
        if save_plot:
            fig.savefig(save_to_as)
        #plt.ion()
        # fig.draw()
        # print "plotting!"
        # plt.show()
        if term:
            def onclose(event):
                fig.canvas.stop_event_loop()
            fig.canvas.mpl_connect('key_press_event', onclose)

            fig.show() # this call does not block on my system
            fig.canvas.start_event_loop_default() # block here until window closed
        else:
            plt.show()

        
    #Converts from segment to frequency,power pairs
    def freq_to_power(self, segment):
        freq = np.add(np.fft.fftfreq(len(segment), d = self.samp_spacing),self.freq)
        pairs = np.vstack((segment.T,freq.T)).T
        return pd.DataFrame(pairs, columns=['Power(dB)','Freq'])
    #Map the windows of sample scans to dataframes
    def freq_pow_pairs_map(self, fft = True):
        segs = self.segments_to_db(fft=fft)
        
        dfs = pd.concat([self.freq_to_power(seg) for seg in segs])
        return dfs
    #Write the paired frequency, power components to a csv file
    def freq_pow_pair_to_csv(self,filename=None, fft=True):
        if filename==None:
            filename = self.filename.split('.')[0].strip()+"_freq_pow_pairs_"+str(self.decimation)+'.csv'
        df = self.freq_pow_pairs_map(fft = fft)
        df.to_csv(filename)
