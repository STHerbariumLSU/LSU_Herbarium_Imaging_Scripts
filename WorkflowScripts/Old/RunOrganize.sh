#!/bin/bash

# Set error log for debugging
elog=/mnt/c/Users/Image/Documents/WorkflowScriptsWS2/organizeIncomingImages.log

# Write date to error log 
echo "$(date)" &>> $elog

# Path to your python script 
python3 /mnt/c/Users/Image/Documents/WorkflowScriptsWS2/organizeIncomingImages.py &>> $elog

# Add extra wait time, a probably unneeded 
sleep 5m