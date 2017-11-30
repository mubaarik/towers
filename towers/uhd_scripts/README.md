## Module Documentation

### Important Files 

1. **usrp_fft.py**
It uses **_usrp_fft_scr.py_** to stream ftt the samples from the USRP device using the bilow GNUradio blocks with the following congiguration. 
  -- Source block -> Repesenting the USRP device in this case.
  -- stream_to_vector block -> To convert the streams to vectors
  -- fft block -> To take the ffts of the vectors from the stream_to_vector block.
  -- complex_to_mag_squared block -> To get power from the Q/I samples from the fft block 
  -- file_sink block -> to write the samples into a file using a float32 .
2. **file_processing.py**
3. **usrp_commands.sh**

###

