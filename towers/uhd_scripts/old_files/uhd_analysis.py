
# coding: utf-8

# In[3]:

import scipy as scp
import numpy as np
import matplotlib.pyplot as plt


# In[19]:

#GNU radio command
#uhd_rx_cfile -a "addr=192.168.10.2" -A TX/RX -s 20e6 -g 25 -f 850e6 --samp_rate=500k -N 5M secondSample.32fc
    #agr:
        #-s-> use shorts instead of complex float
        #-gain->gain in dB
        #-f -> Center frequency 
        #--samp_rate > sample rate
        #-N ->number of samples to be recorded
        #-A -> recieve, transmit, or both
sample_file = scp.fromfile(open('secondSample.32fc'), dtype = scp.int16)
to_float = sample_file.astype(np.float32)
complex_sampls = sample_file.astype(np.float32).view(np.complex64)
complex_sample_set = scp.fromfile(open('thirdSample.32fc'), dtype = scp.complex64)
cut_offs = 10000
length = len(complex_sample_set)

complex_samples = complex_sample_set[cut_offs:length-cut_offs]



# In[15]:

complex_samples[0:30]


# In[ ]:

to_float.shape


# In[ ]:

freq_distr = np.arange(len(sample_file))
plt.plot(freq_distr, sample_file)
plt.show()


# In[20]:

#reading indexes
freq_dist= np.arange(len(complex_samples))

#plotting the imaginary components
f_imag, ax_imag = plt.subplots(figsize = (14,7))
ax_imag.plot(freq_dist, complex_samples.imag)
ax_imag.set_title('imaginary parts')

#save images 
f_imag.savefig('images/raw_imaginaries.png')
f_imag.savefig('images/raw_imaginaries.jpg')

#Plotting the real components 
f_real, ax_real = plt.subplots(figsize = (14,7))
ax_real.plot(freq_dist,complex_samples.real, label = "real parts")
ax_real.set_title('Real parts')

#save plots
f_real.savefig('images/raw_reals.png')
f_real.savefig('images/raw_reals.jpg')


#Plotting magnitudes
f, ax = plt.subplots(figsize = (14,7))
ax.plot(freq_dist, np.absolute(complex_samples), label = "magnitudes")
ax.set_title('magnitudes')

#save images
f.savefig('images/raw_magnitudes.png')
f.savefig('images/raw_magnitudes.jpg')

plt.show()


# In[21]:

#Taking the fft with numpy
cmplx_samples_fft = np.fft.fft(complex_samples)
cmplx_samples_fft


# In[23]:

#Plotting fft results of the samples 

#reading indexes
freq = 850000000
N = len(complex_samples)
sample_spacing = 2e-06
freq_dist = np.fft.fftfreq(N,d= sample_spacing)
freq_dist = np.add(freq_dist, freq)

#plotting the imaginary components
f_imag, ax_imag = plt.subplots(figsize = (8,7))
ax_imag.plot(freq_dist, cmplx_samples_fft.imag)
ax_imag.set_title('fft imaginary parts')

#save images 
#f_imag.savefig('images/fft_imaginaries.png')
#f_imag.savefig('images/fft_imaginaries.jpg')

#Plotting the real components 
f_real, ax_real = plt.subplots(figsize = (8,7))
ax_real.plot(freq_dist,cmplx_samples_fft.real, label = "real parts")
ax_real.set_title('fft Real parts')

#save plots
#f_real.savefig('images/fft_reals.png')
#f_real.savefig('images/fft_reals.jpg')

#Plotting magnitudes
f, ax = plt.subplots(figsize = (8,7))
ax.plot(freq_dist, np.absolute(cmplx_samples_fft))
ax.set_title('fft magnitudes')

#save images
#f.savefig('images/fft_magnitudes.png')
#f.savefig('images/fft_magnitudes.jpg')


plt.show()


# In[210]:

import time
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
class SampleFileAnalysis:
    def __init__(self, filename, center_freq=850e6, sample_rate=5e5, file_datatype = np.complex64):
        self.filename = filename;
        self.freq = center_freq;
        self.samp_rate = sample_rate
        self.cmplx_data = scipy.fromfile(open(filename), dtype = file_datatype)
        self.n = len(self.cmplx_data)
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
    def plot(self, segment, fft = False, indices = None, title = 'data segment', save_plot = False, save_to_as = 'segment'):
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
            filename = self.filename.split('.')[0].strip()+"freq_pow_pairs"+'.csv'
        df = self.freq_pow_pairs_map(fft = fft)
        df.to_csv(filename)
        
        
            
        
            
    
        


# In[ ]:




# In[208]:

samp_analizer = SampleFileAnalysis('thirdSample.32fc')


# In[209]:

samp_analizer.freq_pow_pairs_map()


# In[203]:

samp_analizer.freq_pow_pairs_to_csv()


# In[161]:

segements = samp_analizer.segments_to_db()


# In[162]:

segment_ffts = samp_analizer.segments_to_db(fft=True)
print segment_ffts.shape


# In[197]:

s1 =samp_analizer.freq_to_power(segment_ffts[0])
s2 =samp_analizer.freq_to_power(segment_ffts[1])
s1
#np.apply_along_axis(samp_analizer.freq_to_power, 0, [segment_ffts[0],segment_ffts[1]])


# In[147]:

for segment in segements:
    samp_analizer.plot(segment)


# In[163]:

for segment in segment_ffts:
  
    samp_analizer.plot(segment, fft=True)


# In[ ]:

def generatePlots(data, ftt = False, imag_labels = ['Imaginary Parts','Real Parts','Magnitudes'],
                  image_names = ['imaginaries', 'reals','magnitudes']):
    #Plotting fft results of the samples 

    #reading indexes
    freq_dist= np.arange(len(complex_samples))
    

    #plotting the imaginary components
    f_imag, ax_imag = plt.subplots(figsize = (14,7))
    ax_imag.plot(freq_dist, cmplx_samples_fft.imag)
    image_title = 'Imaginary parts'
    image_name = 'imaginaries'
    if fft:
        image_title = 'fft imaginary parts'
        image_name = 'fft_imaginaries'
    ax_imag.set_title('fft imaginary parts')

    #save images 
    f_imag.savefig('images/fft_imaginaries.png')
    f_imag.savefig('images/fft_imaginaries.jpg')

    #Plotting the real components 
    f_real, ax_real = plt.subplots(figsize = (14,7))
    ax_real.plot(freq_dist,cmplx_samples_fft.real, label = "real parts")
    ax_real.set_title('fft Real parts')
    
    image_title = 'Real Parts'
    image_name = 'reals'
    if fft:
        image_title = 'ftt Real Parts'
        image_name = 'fft_reals'
    #save plots
    f_real.savefig('images/fft_reals.png')
    f_real.savefig('images/fft_reals.jpg')

    #Plotting magnitudes
    f, ax = plt.subplots(figsize = (14,7))
    ax.plot(freq_dist, np.absolute(cmplx_samples_fft))
    
    ax.set_title('fft magnitudes')
    
    image_title = 'magnitudes'
    image_name = 'magnitudes'
    if fft:
        image_title = 'fft magnitudes'
        image_name = 'fft_magnitudes'
    #save images
    f.savefig('images/fft_magnitudes.png')
    f.savefig('images/fft_magnitudes.jpg')


    plt.show()


# In[ ]:

sample_compl[0:30]


# In[ ]:

low = 0
high = 10000
for i in range(len(sample_file)/10000):
    plt.plot(range(len(np.absolute(sample_file)[low:high])),np.absolute(sample_file.real[low:high]))
    low+=10000
    high+=10000
#plt.plot(range(len(np.absolute(sample_file)[low:high])),sample_file.real[low:high])
#plt.plot(range(len(np.absolute(sample_file)[low:high])),np.absolute(sample_file)[low:high])
    plt.show()


# In[ ]:

from gnuradio.blocks import file_meta_source


# In[ ]:

If you want to use the GNU tools by default, add this directory to the front of your PATH environment variable:
        opt(/local/libexec/gnubin/)


# In[ ]:

sample_part = sample_file[0:5000100]
print "sample_part: ", sample_part, "sample_part_len: ",len(sample_part) 
print "samples_file: ", sample_file, "sample_file_len: ",len(sample_file)
fft = np.fft.fft(sample_part, n = 2*len(sample_part))


# In[ ]:

fft


# In[ ]:

freq = range(len(fft))
#freq = np.fft.fftfreq(freq)
#plt.plot(freq, fft.real, freq, fft.imag, freq, np.absolute(fft))
low = 0
high = 1000
chuck = high-low
for i in range(len(freq)/chuck):
    plt.plot(freq[low:high], np.absolute(fft[low:high]))
    low+=chuck
    high+=chuck
    plt.show()
    


# In[ ]:

def compute(string_freq, sample_rate, num_samples)


# In[ ]:

#freq taken parameters
freq = 850000000
sample_rate = 500000
num_samples = 5000000
low = 0
high = 1000


# In[ ]:

low = 0
high = 100
for i in range(len(sample_file)/10000):
    plt.plot(range(len(np.absolute(sample_file)[low:high])),np.absolute(sample_file.real[low:high]))
    low+=100
    high+=100
#plt.plot(range(len(np.absolute(sample_file)[low:high])),sample_file.real[low:high])
#plt.plot(range(len(np.absolute(sample_file)[low:high])),np.absolute(sample_file)[low:high])
    plt.show()


# In[ ]:

arange = np.arange(100).shape[-1]
arange


# In[ ]:

#!/opt/local/bin/python2.7
import gnuradio


# In[70]:

a = np.arange(6)
b = np.arange(6)*8
c = np.vstack((a.T,b.T))
d = np.vstack((c,a*3))
a.reshape(2,3)


# In[167]:

import pandas as pd
pd.DataFrame(c.T)


# In[120]:

x = np.complex64(4+2j)


# In[124]:

np.apply_along_axis(np.sqrt,0,d)


# In[ ]:

np.

