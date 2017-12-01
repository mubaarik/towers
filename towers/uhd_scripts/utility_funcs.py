import pandas as pd
import numpy as np
import os
import ast
import glob
import time
'''
$ ls directory/*extension

'''
def directory_parser(directory, extension = '.csv'):
    return glob.glob(directory+'/'+'*'+extension)
'''
The set union function. Intended to produce a set of the ARFCNs(remove repitition)
'''
def unionizer(freq_map):
    union = reduce(np.union1d,freq_map.values())
    return union
'''
Divides the an array based on values gaps jumps 
'''
def segmenter(arry,out, threshold):
    i =0
    n = len(arry)-1
    while i<n:
        assert arry[i]<=arry[i+1],"expected sorted array!"
        diff = (arry[i+1]-arry[i])
        if diff>threshold:
            out.append(arry[0:i+1])
            arry = arry[i+1:]
            i =0
            n = len(arry)-1
            
    
        i+=1
    out.append(arry)
    return out
'''
Divides the union of the ARFCNs into bands using segmenter
'''
def arrange(freq_map, threshold=1.0):
    arry = unionizer(freq_map)
    return segmenter(arry,[], threshold)
'''
Takes a band of frequencies divides into segments that can be covered by the given 
sample rate. It returns a list of center frequencies for this given band of ARFCNs. 
'''
def cFrqs(band, samp_rate, overlap=.5):
    
    c_frqs = []
    high = max(band)
    low = min(band)
    if (high-low)<samp_rate:
        return [round((low+high)/2.0,3)*1e6]
    c_freq = low+(samp_rate/2.0 - overlap)
    while (samp_rate/2.0<(high-c_freq)):
        c_frqs.append(c_freq)
        c_freq = c_freq+(samp_rate-overlap)
        if (samp_rate/2.0>(high-c_freq)):
            c_frqs.append(c_freq)
            
    
    h_f = c_frqs[-1]
    l_diff = overlap
    h_diff = high-(h_f+samp_rate/2.0-overlap)
    if h_diff<0:
        h_diff = overlap+abs(h_diff)
    
    diff = (h_diff-l_diff)/2.0
    frqs = [round(c_frq-diff,3)*1e6 for c_frq in c_frqs]
    
    return frqs
        
'''
applies cFreqs to all the bands produce
'''    
def mapper(freqs, samp_rate):
    mapps = []
    for band in freqs:
        mapps.extend(cFrqs(band,samp_rate))
    return mapps
'''
gets the union of the all the ARFCNs, segments them, and then calculates center frequencies for them.
'''
def center_freqs(freq_map,samp_rate, threshold=1.0):
    freqs = arrange(freq_map,threshold)
    return mapper(freqs,samp_rate)
'''
takes in a file name and file map(list of dictionaries) and saves to a file
'''
def save_file(name,filemap,dirc = 'meta_files'):
    pd.DataFrame(filemap).to_csv(dirc+'/'+str(name)+'.csv')




