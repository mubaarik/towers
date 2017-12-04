## Module Documentation

### Important Files 
1. **usrp_fft_src.py**</br>
   Streams Q/I samples from the USRP device and takes the fft before it saves the samples into a file, the bilow image shows the GNUradio gr-blocks used to assemble this module.</br>
   ![gr-blocks](blocks.png?raw=true "gnuradio gr-blocks")
   ###### **Block descriptions**</br>
    - **UHD: USRP Source** is the USRP device block. It encapsolutes the low-level work needed for configuring the device(and potential subdevices) and streaming the raw samples, Q/I. For more on **USRP Source** visit the [gnuradio reference](https://gnuradio.org/doc/doxygen/classgr_1_1uhd_1_1usrp__source.html)</br>  
    - **stream to vector**: The **USRP Source** block spits out the data one-by-one(stream), but the **FFT** block expects vectors to take the ffts of. This module groups the stream from the **USRP Source** into vectors of size the number of fft bins.
    - The **FFT** block takes the [Fast Fourier Transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform) of the vectors from the **stream to vector** block.
    - **Complex to mag^2** computes the power from the output of the **FFT** block outputting floats.
    - Finally **File Sink** block sames the output of the **Complex to mag^2** block to a file.
   ###### **Important parts of the code for modifications**
      a. **Initializing the blocks**
         
         ```python
         self.fft_vxx_0 = fft.fft_vcc(options.fft_size, True, (), True, 1)
         self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, options.fft_size)
         self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*options.fft_size,self.filenames[0])
         self.blocks_file_sink_0.set_unbuffered(False)
         self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(options.fft_size)
         ```
      b. Connecting the blocks
      ```python
      self.fft_vxx_0 = fft.fft_vcc(options.fft_size, True, (), True, 1)
      self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, options.fft_size)
      self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*options.fft_size,self.filenames[0])
      self.blocks_file_sink_0.set_unbuffered(False)
      self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(options.fft_size)
      ```
        
   
   
1. **usrp_fft.py**</br>
   It uses **_usrp_fft_scr.py_** to stream ftt the samples from the USRP device using the bilow GNURADIO blocks. </br>
   - Source block -> Repesenting the USRP device in this case.</br>
   - stream_to_vector block -> To convert the streams to vectors. </br>
   - fft block -> To take the ffts of the vectors from the stream_to_vector block.</br>
   - complex_to_mag_squared block -> To get power from the Q/I samples from the fft block .</br>
   - file_sink block -> to write the samples into a file using a float32 .</br>
   
   
   The module groups the ARFCNs into bands using the provided sample rate(from `usrp_rx_commands <optional arguments>` or the defualt value). For each band it takes **_fft_size*num_ffts_** of samples at the given sample rate before it moves on to the next band. For each iteration, it creates a meta files mapping the center frequencies and time stamps to stream files and saves them to _meta_files/_ and stream files are saved to _fft_files/_. Those meta files are used to later process the data.</br>
2. **file_processing.py**
3. **usrp_commands.sh**

###

