## Module Documentation

### Important Files 

1. **usrp_fft.py**</br>
   It uses **_usrp_fft_scr.py_** to stream ftt the samples from the USRP device using the bilow GNURADIO blocks. </br>
   - Source block -> Repesenting the USRP device in this case.</br>
   - stream_to_vector block -> To convert the streams to vectors. </br>
   - fft block -> To take the ffts of the vectors from the stream_to_vector block.</br>
   - complex_to_mag_squared block -> To get power from the Q/I samples from the fft block .</br>
   - file_sink block -> to write the samples into a file using a float32 .</br>
The module groups the ARFCNs into bands using the provided sample rate(from `usrp_rx_commands <optional arguments>` or the defualt value). For each band it takes **_fft_size*num_ffts_** of samples at the given sample rate before it moves on to the next band. For each iteration, it creates a meta files mapping the center frequencies and time stamps to stream files and saves them in _meta_files/_. 
2. **file_processing.py**
3. **usrp_commands.sh**

###

