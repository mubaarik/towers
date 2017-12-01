## Running the scripts 

I am in the process of developing more detailed documentations but for the time being follow the bilow instrutions to run the scripts.

### Where and to run?
To collect fft samples type the following commands

- To navigate into the scripts directory type: `$ cd ~/Desktop/towers/towers/uhd_scripts`</br>

- To collect samples without extracting power,freq pairs type: `python usrp_fft.py <optional parameters>`</br>

- To see what the optional parameters are type: `python usrp_fft.py --help` </br>

- To the csv files showing the collected files type: `cd fft_files/` and also see `meta_files/`</br>
----------------------------------------------------------------------------</br>
- To collect samples and extract the power,freq pairs run: `./usrp_commands.sh <optional parameters>` the optional parameters are same as the before(as _usrp_fft.py <optional parameters>_).



