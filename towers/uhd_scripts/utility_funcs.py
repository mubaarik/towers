import pandas as pd
import numpy as np
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
def designate(samp_rate, c_freq, channel):
    return (channel>=(c_freq-(samp_rate-1.0)/2.0) and channel<=(c_freq+(samp_rate-1.0)/2.0))
def channelMapper(band, samp_rate, freq, channels_map):
    band_channels = []
    for channel in channels_map[band]:
        if designate(samp_rate, freq, channel):
            band_channels.append(channel)
    return band_channels
 
def bandMapp(freqs):
    bandmaps = []
    for band in freqs.keys():
        bandwidth = max(freqs[band])-min(freqs[band])
        c_freq = (max(freqs[band])+min(freqs[band]))/2.0
        if (bandwidth+2.0)/25.0<1:
            sample_rate = bandwidth+2.0
            band_dict = {'band':band,'samp_rate': round(sample_rate,3), 'cntr_freq': round(c_freq,3),
                         'channels':channelMapper(band, sample_rate, c_freq, freqs)}
            bandmaps.append(band_dict)
        elif (bandwidth+3.0)/25<2:
            sample_rate = (bandwidth+3.0)/2.0
            c_f1 = c_freq - (sample_rate-1.0)/2.0
            c_f2 = c_freq +(sample_rate-1.0)/2.0
            band_dict = {'band':band,'samp_rate': round(sample_rate,3), 'cntr_freq': round(c_f1,3),
                        'channels':channelMapper(band, sample_rate, c_f1, freqs)}
            bandmaps.append(band_dict)
            band_dict = {'band':band,'samp_rate': round(sample_rate,3), 'cntr_freq': round(c_f2,3),
                        'channels':channelMapper(band, sample_rate, c_f2, freqs)}
            bandmaps.append(band_dict)
        elif (bandwidth+4.0)/25.0<3:
            sample_rate = (bandwidth+4.0)/3.0
            c_f1 = c_freq - (sample_rate-1.0)
            c_f2 = c_freq 
            c_f3 = c_freq +(sample_rate-1.0)
            band_dict = {'band':band,'samp_rate': round(sample_rate,3), 'cntr_freq': round(c_f1,3),
                        'channels':channelMapper(band, sample_rate, c_f1, freqs)}
            bandmaps.append(band_dict)
            band_dict = {'band':band,'samp_rate': round(sample_rate,3), 'cntr_freq': round(c_f2,3),
                        'channels':channelMapper(band, sample_rate, c_f2, freqs)}
            bandmaps.append(band_dict)
            band_dict = {'band':band,'samp_rate': round(sample_rate,3), 'cntr_freq': round(c_f3,3),
                        'channels':channelMapper(band, sample_rate, c_f3, freqs)}
            bandmaps.append(band_dict)
        else:
            sample_rate = (bandwidth+5.0)/4.0
            c_f1 = c_freq-(sample_rate*3/2.0-1.5)
            c_f2 = c_freq-(sample_rate-1.0)/2.0
            c_f3 = c_freq+(sample_rate-1.0)/2.0
            c_f4 = c_freq+(sample_rate*3/2.0-1.5)
            band_dict = {'band':band,'samp_rate': round(sample_rate,3), 'cntr_freq': round(c_f1,3),
                        'channels':channelMapper(band, sample_rate, c_f1, freqs)}
            bandmaps.append(band_dict)
            band_dict = {'band':band,'samp_rate': round(sample_rate,3), 'cntr_freq': round(c_f2,3),
                        'channels':channelMapper(band, sample_rate, c_f2, freqs)}
            bandmaps.append(band_dict)
            band_dict = {'band':band,'samp_rate': round(sample_rate,3), 'cntr_freq': round(c_f3,3),
                        'channels':channelMapper(band, sample_rate, c_f3, freqs)}
            bandmaps.append(band_dict)
            band_dict = {'band':band,'samp_rate': round(sample_rate,3), 'cntr_freq': round(c_f4,3),
                        'channels':channelMapper(band, sample_rate, c_f4, freqs)}
            bandmaps.append(band_dict)
    return bandmaps
def band_sampRate_freq(csv_file):
    df = pd.read_csv(csv_file)
    triple = zip(df['band'], df['samp_rate'],df['cntr_freq'])
    return triple
def dfRow_to_bandSegmentObj(row):
    return BandSegment(row.band,row.channels,row.cntr_freq, row.samp_rate)
def band_segmentation():
    return pd.read_csv('csv_files/band_chan_freq_smpRate.csv').apply(dfRow_to_bandSegmentObj,1)

