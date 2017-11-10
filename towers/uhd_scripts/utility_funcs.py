import pandas as pd
import numpy as np
import os
import ast
import glob
import time



from uhd_processor import SampleFileAnalysis as sfa
class BandSegment:
    def __init__(self, band, channels, c_freq, samp_rate, filename=None):
        self.band = band;
        self.channels = channels;
        self.c_freq = c_freq;
        self.samp_rate = samp_rate
        self.filename = filename
    def get_band(self):
        return self.band 
    def get_channels(self):
        assert isinstance(band, numpy.ndarray)
        return self.channels
    def get_freq(self):
        return self.c_freq
    def get_samp_rate(self):
        return self.samp_rate
    def get_file(self):
        return self.filename
def designate(samp_rate, c_freq, channel,overlap):
    return (channel>=(c_freq-(samp_rate-overlap)/2.0) and channel<=(c_freq+(samp_rate-overlap)/2.0))
def channelMapper(band, samp_rate, freq, channels_map,overlap):
    band_channels = []
    for channel in channels_map[band]:
        if designate(samp_rate, freq, channel,overlap):
            band_channels.append(channel)
    return band_channels
def freqMap(freqs,band, low, high, segment_width, overlap):
    freq_map = []
    c_freq = low+(segment_width/2.0 - overlap)
    band_dict = {'band':band,'samp_rate': segment_width, 'cntr_freq': round(c_freq,3),
                        'channels':channelMapper(band, segment_width, c_freq, freqs,overlap)}
    freq_map.append(band_dict)
    while (segment_width/2.0<(high-c_freq)):
        c_freq = c_freq+(segment_width-overlap)
        band_dict = {'band':band,'samp_rate': segment_width, 'cntr_freq': round(c_freq,3),
                        'channels':channelMapper(band, segment_width, c_freq, freqs,overlap)}
        freq_map.append(band_dict)
    return freq_map
        
    
def bandMap(freqs, segment_width=4.0,overlap=.5):
    bandmaps = []
    for band in freqs.keys():
        high= max(freqs[band])
        low = min(freqs[band])
        _map=freqMap(freqs,band, low, high, segment_width, overlap)
        bandmaps.extend(_map)
    return bandmaps

def band_sampRate_freq(csv_file):
    df = pd.read_csv(csv_file)
    triple = zip(df['band'], df['samp_rate'],df['cntr_freq'])
    return triple
def dfRow_to_bandSegmentObj(row):
    return BandSegment(row.band,row.channels,row.cntr_freq, row.samp_rate)
def band_segmentation():
    return pd.read_csv('csv_files/band_chan_freq_smpRate.csv').apply(dfRow_to_bandSegmentObj,1)
#Extract mapped dp_freq
#extract the specified frequencies 
#save the maps to a csv file
def process_files(segment, filemap, output_dir):
    #for segment in band_segments:
    input_file = segment.filename
    output_file = output+'/'+segment.filename.split('.')[0].strip()+'.csv'
    analizer = sfa(segment.filename, center_freq=segment.c_freq*1e6, sample_rate=segment.samp_rate*1e6)
    freq_dB = analizer.freq_pow_pairs_map(segmented=False)
    channels = np.array(ast.literal_eval(segment.channels))*1e6
    f_freq_dB = freq_dB[freq_dB['Freq'].isin(channels)]
    #csv_file = segment.filename.split('.')[0].strip()+'.csv'
    f_freq_dB.to_csv(output_file)
    os.remove(segment.filename)
    segment.filename = None
    if segment.band in filemap:
        filemap[segment.band].append(output_file)
    else:
        filemap[segment.band]=[output_file]

    return None
def band_channels(filemap,time, out_dir):
    for band in filemap.keys():
        df = pd.concat([pd.read_csv(filename) for filename in filemap[band]])
        df=df.reset_index().drop(['index'], axis=1)
        csv_file = out_dir+'/'+band.replace(' ','_')+'_'+time+'.csv'
        df.to_csv(csv_file)
        for filename in filemap[band]:
            os.remove(filename)
def qi_files_to_csv():
    return None
def filemap_to_df(filemap):
    data_map = [{'band':obj.band,'samp_rate': obj.samp_rate, 'cntr_freq': obj.c_freq,'channels':obj.channels, 'filename': obj.filename} for obj in filemap]
    return pd.DataFrame(data_map)



def filemap_to_csv(filemap,out_dir):
    df = filemap_to_df(filemap)
    stamp=str(int(round(time.time())))+'.csv'
    df.to_csv(out_dir+'/'+stamp)
def row_to_object(row):
    obj = dfRow_to_bandSegmentObj(row)
    obj.filename = row.filename
    return obj
def df_to_bandsegment(file_name):
    return pd.read_csv(file_name).apply(row_to_object,1)
def directory_parser(directory, extension = '.csv'):
    return glob.glob(directory+'/'+'*'+extension)

def master_processor(dirc,ouput_dir ,ext='.csv'):
    files = directory_parser(dirc, extension=ext)
    for _file_ in files:
        object_map = df_to_bandsegment(_file_)
        filemap = {}
        time = _file_.spilt('/')[0].split('.')[0]
        for segment in object_map:
            process_files(segment, filemap,output_dir)
        os.remove(_file_)
        band_channels(filemap,time,output_dir)



def unionizer(freq_map):
    union = reduce(np.union1d,freq_map.values())
    return union
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
def arrange(freq_map, threshold=1.0):
    arry = unionizer(freq_map)
    return segmenter(arry,[], threshold)
def cFrqs(band, samp_rate, overlap=.5):
    
    c_frqs = []
    high = max(band)
    low = min(band)
    if (high-low)<samp_rate:
        return [(low+high)/2.0]
    c_freq = low+(samp_rate/2.0 - overlap)
    while (samp_rate/2.0<(high-c_freq)):
        c_frqs.append(c_freq)
        c_freq = c_freq+(samp_rate-overlap)
        if (samp_rate/2.0>(high-c_freq)):
            c_frqs.append(c_freq)
            #print "c_freq: ",c_freq
    #print c_frqs
    h_f = c_frqs[-1]
    l_diff = overlap
    h_diff = high-(h_f+samp_rate/2.0-overlap)
    if h_diff<0:
        h_diff = overlap+abs(h_diff)
    #print h_diff, l_diff
    diff = (h_diff-l_diff)/2.0
    frqs = [c_frq-diff for c_frq in c_frqs]
    #print "high low: ", high, low
    
    return frqs
        
    
    
def mapper(freqs, samp_rate):
    mapps = []
    for band in freqs:
        mapps.extend(cFrqs(band,samp_rate))
    return mapps
def center_freqs(freq_map,samp_rate, threshold=1.0):
    freqs = arrange(freq_map,threshold)
    return mapper(freqs,samp_rate)




