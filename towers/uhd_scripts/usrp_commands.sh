#!/bin/sh
echo "Running the usrp data collection files............"

python uhd_rx_commands.py ${BASH_ARGV[*]} &
python file_processing.py &
