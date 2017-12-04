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
      b. **Connecting the blocks**
      ```python
      if options.nsamples is None:
            	self.connect((self.fft_vxx_0, 0), (self.blocks_file_sink_0, 0))
    else:
        self._head = blocks.head(gr.gr.sizeof_gr_complex*options.fft_size, int(options.nsamples)/options.fft_size)
        self.connect((self.fft_vxx_0, 0), self._head,(self.blocks_file_sink_0, 0))    
      self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
      #self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
      self.connect((self.uhd_usrp, 0), (self.blocks_stream_to_vector_0, 0)) 
      ```
      Refer to the GNU Radio [wiki](https://wiki.gnuradio.org/index.php/Main_Page) and the GNU Radio [reference documentation](https://gnuradio.org/doc/doxygen/) for detailed documentation of gr-blocks and other modules used here.
        
   
   
2. **usrp_fft.py**</br>
   The cammand line interface for **_usrp_fft_src.py__**, it accepts numerious command line arguments to set the parameters for streaming  from the USRP, set the fft-size, etc. To view a list of the arguments and their description, run `$ python usrp_fft.py --help`.</br>
   Before running the steaming scripts, this module groups the ARFCNs into bands. To see how this grouping is done please take a look at the [utility functions](https://github.com/mubaarik/towers/blob/master/towers/uhd_scripts/utility_funcs.py).
3. **fft_analizer.py**
4. **file_processing.py**
3. **usrp_commands.sh**

###

