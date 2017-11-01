import pandas as pd
import numpy as np
import os
import ast

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
def process_files(segment, filemap):
    #for segment in band_segments:
    analizer = sfa(segment.filename, center_freq=segment.c_freq*1e6, sample_rate=segment.samp_rate*1e6)
    freq_dB = analizer.freq_pow_pairs_map(segmented=False)
    channels = np.array(ast.literal_eval(segment.channels))*1e6
    f_freq_dB = freq_dB[freq_dB['Freq'].isin(channels)]
    csv_file = segment.filename.split('.')[0].strip()+'.csv'
    f_freq_dB.to_csv(csv_file)
    os.remove(segment.filename)
    segment.filename = None
    if segment.band in band_freq_map:
        filemap[band].append(csv_file)
    else:
        filemap[band]=[csv_file]

    return None
def band_channels(filemap):
    for band in filemap.keys():
        df = pd.concat([pd.read_csv(filename) for filename in filemap[band]])
        df=df.reset_index().drop(['index'], axis=1)
        csv_file = 'data_files/'+band.replace(' ','_')+'_'+str(int(round(time.time())))+'.csv'
        df.to_csv(csv_file)
        for filename in filemap[band]:
            os.remove(filename)




