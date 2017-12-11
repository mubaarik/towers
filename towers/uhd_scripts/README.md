## Module Documentation

### Important Files 
1. **usrp\_fft\_src.py**</br>
   Streams Q/I samples from the USRP device and takes the fft before it saves the samples into a file, the bilow image shows the GNUradio gr-blocks used to assemble this module.</br>
   ![gr-blocks](blocks.png?raw=true "gnuradio gr-blocks")
   ###### **Block descriptions**</br>
    - **UHD: USRP Source** is the USRP device block. It encapsulates the low-level work needed for configuring the device(and potential subdevices) and streaming the raw samples, Q/I. For more on **USRP Source** visit the [gnuradio reference](https://gnuradio.org/doc/doxygen/classgr_1_1uhd_1_1usrp__source.html)</br>  
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
        
   
   
2. **usrp\_fft.py**</br>
   The cammand line interface for **_usrp\_fft\_src.py_**, it accepts numerious command line arguments to set the parameters for streaming  from the USRP, set the fft-size, etc. To view a list of the arguments and their description, run `$ python usrp_fft.py --help`.</br>
   
   Before running the streaming scripts, this module groups the ARFCNs into bands. To see how this grouping is done please take a look at the [utility functions](https://github.com/mubaarik/towers/blob/master/towers/uhd_scripts/utility_funcs.py).
   
   After grouping the ARFCNs into bands it further segments the bands to get a list of sub-bands with width of no greater than the requisted sample rate. After this segmentation, it creates a list of the center frequencies, one for each sub-band. Finally, it goes through each the center frequencies and collects samples for them and saves the to fft\_files/time\_centerFrequency.32fc. where _time_ is the time this sample was collected and _centerFrequency_ is the center frequency of the sub-band this sample corresponds to. 
   
   For each pass through, it also creates a csv file mapping time,center frequency,sample rate, and other parameters to name of the sample file, and saves it to _meta\_files/time.csv_. The file processing modules(next section) use this directory to look for collected samples to process.  
3. **fft\_file\_analizer.py**</br>
   This file contains two classes _Sample_ which represents a sample with given center frequency, time stamp, and filename(where the samples are stored), and _Analizer_ which takes in a meta file as described earlier defines couple of methods for processing the sample file and analyzing.
4. **file\_processing.py**</br>
   This file contains the code that continouosly checks if samples were collected by checking meta files in _meta\_files_. For every meta file it finds, it goes through all the sample files it maps and takes the averages of the ffts stored in the sample file, maps the average samples to the corresponding frequencies, and finally it saves the resulting map to _collected\_data/time\_centerFrequency.csv_, essentially converting the sample file to a csv file. The csv file is in the form (index,power(dB),freq).
3. **usrp\_commands.sh**</br>
   This bash file runs the data streaming and file processing as two seperate processes.It expects the same commandline arguments as the `usrp_fft.py`.<\br>
   
   Run: `./usrp_commands.sh --help` to take a look at the arguments again and `./usrp_commands.sh <optional arguments>` to run it. Make sure that you're in the _uhd\_scripts_ directory(`cd ~/Desktop/towers/towers/uhd_scripts`).

###

