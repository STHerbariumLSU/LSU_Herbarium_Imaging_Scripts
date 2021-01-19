#!/bin/bash
# Path to your python script and output log to capture errors, even though you shouldn't need it. 
python3 /mnt/c/Users/Image/Documents/WorkflowScriptsWS2/organizeIncomingImages.py &>> log.log
# Add extra wait time, also probably unneeded 
sleep 1m