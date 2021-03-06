import scipy as scp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

class Sample:
	def __init__(self,time_stamp, center_freq,filename):
		self.time_stamp = time_stamp
		self.center_freq = center_freq
		self.filename = filename
	def get_freq(self):
		return self.center_freq
	def get_time(self):
		return self.time_stamp
	def get_file(self):
		return self.filename
class Analizer:
	def __init__(self,filename):
		self.samp_rate = None 
		self.fft_size = None
		self.gain = None
		self.row_map = None
		self.remove = None
		self.filename = filename
		self.row_mapper()
		self.freq = sorted(np.fft.fftfreq(self.fft_size, d = 1.0/self.samp_rate))
	'''
	'''
	def decompose(self):
		parts = self.filename.split('_')
		samp_rate = parts[0].strip()
		stamp = parts[1].strip()
		frequency = parts[2].strip()
		assert parts[3]==parts[-1], "expected length of 4"
		extension = parts[-1].strip().split('.')[-1]
		fileparts = FileParts(samp_rate,stamp,frequency,extension)
		self.fileparts = fileparts
		return fileparts
	'''
	converts a row of meta file data to a sample object
	'''
	def row_converter(self,row):
		if self.samp_rate is None:
			self.samp_rate = row.samp_rate
		if self.fft_size is None:
			self.fft_size = row.fft_size
		if self.gain is None:
			self.gain = row.gain
		if self.remove is None:
			self.remove = row.remove
		return Sample(row.time,row.c_freq,row.filename)
	'''
	converts meta file to series of Sample object 
	'''
	def row_mapper(self):
		data = pd.read_csv(self.filename).apply(self.row_converter,1)
		os.remove(self.filename)
		self.filename= None
		self.row_map = data
		return data
	'''
	takes in complex numpy array and multiples complex conjugates
	'''
	def multiply_conj(self,cmplx):
		return abs(cmplx*np.conjugate(cmplx))
	'''
	Averages all the fft samples in a sample data
	'''
	def fft_average(self,sample):
		filename = sample.filename
		vect = np.vectorize(self.multiply_conj)
		data = scp.fromfile(open(filename), dtype = scp.complex64)
		data = vect(data)
		number_of_ffts = len(data)/self.fft_size
		segments = data.reshape(number_of_ffts,self.fft_size)
		means = np.average(segments,axis=0)
		return means
	'''
	Maps frequencies to samples, returning a array of shape (2,fft-size)
	'''
	def freq_map(self,sample):
		freq = np.add(self.freq, sample.center_freq)
		segment = self.fft_average(sample)
		return np.vstack((segment.T,freq.T)).T
	'''
	Averages the ffts and saves them to a file
	'''
	def pw_frq_pair_to_csv(self, sample):
		f = str(sample.time_stamp)+'_'+str(int(sample.center_freq))+'.csv'
		pd.DataFrame(self.freq_map(sample),columns=['Power(dB)','Freq']).to_csv('collected_data/'+f)
		if self.remove:
			os.remove(sample.filename)
	'''
	'''
	def analyze(self,filename):
		return None
	'''
	'''
	def plot_average(self,sample_index = 0):
		sample = self.row_map[sample_index]
		means = self.fft_average(sample)
		freqs= np.add(self.freq, sample.center_freq)
		plt.plot(freqs,means)
		plt.show()







